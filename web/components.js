(function () {
    const fallbackSources = ["https://www.google.com/maps/search/Ocean+Park+1+food"];

    function escapeHtml(value) {
        return String(value ?? "")
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#039;");
    }

    function normalizeConfidence(value) {
        if (typeof value === "string") {
            const lowered = value.toLowerCase();
            if (lowered === "high") return 0.85;
            if (lowered === "medium") return 0.6;
            if (lowered === "low") return 0.3;
            const parsed = Number(value);
            return Number.isFinite(parsed) ? parsed : 0;
        }

        return Number.isFinite(value) ? value : 0;
    }

    function getConfidenceMeta(value) {
        const score = Math.max(0, Math.min(1, normalizeConfidence(value)));

        if (score >= 0.7) {
            return { score, label: "High", className: "badge-high", text: "Cao" };
        }

        if (score >= 0.4) {
            return { score, label: "Medium", className: "badge-medium", text: "Vừa" };
        }

        return { score, label: "Low", className: "badge-low", text: "Thấp" };
    }

    function getEta(item) {
        return item.predicted_eta_range || item.eta_range || item.predicted_eta || item.pred_eta || item.eta || "30-45";
    }

    function getSources(item) {
        return item.evidence_links || item.source_links || item.sources || fallbackSources;
    }

    function getMenuLink(item) {
        return item.menu_url || item.menu_link || item.deep_link || getSources(item)[0] || "#";
    }

    function getReason(item) {
        if (item.rationale) return item.rationale;
        if (item.reason) return item.reason;
        if (Array.isArray(item.reasons)) return item.reasons.join("; ");
        return "Được xếp hạng dựa trên ETA, khoảng cách, độ mới của nguồn và báo cáo cộng đồng.";
    }

    function renderTrace(trace = []) {
        const traceBody = document.getElementById("traceBody");
        const traceCount = document.getElementById("traceCount");
        const traceTitle = document.getElementById("traceTitle");
        const steps = Array.isArray(trace) ? trace : [];

        traceCount.textContent = `${steps.length} bước`;
        traceTitle.textContent = `Chi tiết quyết định (${steps.length} bước)`;

        if (!steps.length) {
            traceBody.innerHTML = '<div class="trace-step"><span class="trace-index">-</span><p class="trace-text">Không có trace từ API.</p></div>';
            return;
        }

        traceBody.innerHTML = steps.map((step, index) => {
            const label = step.type || step.label || step.name || "decision";
            const text = step.thought || step.action || step.result || step.message || step.description || step;
            const tool = step.tool ? ` Tool: ${step.tool}.` : "";
            const params = step.params ? ` Params: ${JSON.stringify(step.params)}.` : "";

            return `
                <div class="trace-step">
                    <span class="trace-index">${escapeHtml(step.step || index + 1)}</span>
                    <div>
                        <span class="trace-label">${escapeHtml(label)}</span>
                        <p class="trace-text">${escapeHtml(text)}${escapeHtml(tool)}${escapeHtml(params)}</p>
                    </div>
                </div>
            `;
        }).join("");
    }

    function renderSuggestions(suggestions = [], originalQuery = "") {
        const listContainer = document.getElementById("suggestionsList");
        const items = Array.isArray(suggestions) ? suggestions : [];

        if (!items.length) {
            listContainer.innerHTML = '<div class="notice warn">Không tìm thấy quán phù hợp. Hãy thử mở rộng vị trí hoặc bớt ràng buộc.</div>';
            return;
        }

        listContainer.innerHTML = items.map((item, index) => {
            const confidence = getConfidenceMeta(item.confidence);
            const sources = getSources(item);
            const id = escapeHtml(item.id || `suggestion-${index + 1}`);
            const itemName = item.name || item.restaurant_name || "Quán ăn phù hợp";
            const vendor = item.vendor || item.platform || item.source || "Local source";
            const sponsored = item.sponsored || item.is_partner || index === 0;
            const imageUrl = `https://loremflickr.com/500/300/food,dish,restaurant/all?lock=${index + id.length}`;
            const sourceLinks = sources.slice(0, 3).map((source, sourceIndex) => `
                <a class="source-pill" href="${escapeHtml(source)}" target="_blank" rel="noreferrer">
                    Link nguồn ${sourceIndex + 1}
                </a>
            `).join("");
            const lowConfidenceWarning = confidence.label === "Low"
                ? '<p class="notice warn">Độ tin cậy thấp: nên gọi/xem thực đơn trước khi đặt.</p>'
                : "";

            return `
                <article class="suggestion-card">
                    <img src="${imageUrl}" class="card-media" alt="${escapeHtml(itemName)}" loading="lazy">
                    <div class="card-header">
                        <div>
                            <h3 class="card-title">${escapeHtml(itemName)} (${escapeHtml(vendor)})</h3>
                            <p class="vendor-line">Hạng #${index + 1} trong khu Ocean Park 1</p>
                        </div>
                        ${sponsored ? '<span class="sponsor-chip">Partner signal</span>' : ""}
                    </div>

                    <div class="card-body">
                        <div class="fact-row">
                            <span class="fact">ETA: ${escapeHtml(getEta(item))} phút</span>
                            <span class="confidence-badge ${confidence.className}">
                                Độ tin cậy: ${confidence.text} (${Math.round(confidence.score * 100)}%)
                            </span>
                        </div>

                        <p class="rationale">${escapeHtml(getReason(item))}</p>
                        ${lowConfidenceWarning}

                        <div class="source-row">${sourceLinks}</div>

                        <div class="card-actions">
                            <a href="${escapeHtml(sources[0] || "#")}" target="_blank" rel="noreferrer" class="btn-action">Xem nguồn</a>
                            <a href="${escapeHtml(getMenuLink(item))}" target="_blank" rel="noreferrer" class="btn-action primary">Mở thực đơn</a>
                            <button type="button" class="btn-action" onclick="toggleFeedback('${id}')">Xem chi tiết</button>
                        </div>

                        <div class="feedback-widget" id="fb-widget-${id}" hidden>
                            <p class="feedback-title">Gợi ý này có hữu ích không?</p>
                            <div class="stars" id="stars-${id}" data-rating="0">
                                ${[1, 2, 3, 4, 5].map((rating) => `
                                    <button type="button" class="star" aria-label="${rating} sao" onclick="selectStar('${id}', ${rating})">*</button>
                                `).join("")}
                            </div>
                            <textarea class="feedback-input" id="text-${id}" rows="2" placeholder="Báo sai ETA, quán đông, giá không đúng..."></textarea>
                            <div class="feedback-buttons">
                                <button type="button" class="btn-fb" onclick="skipFeedback('${id}')">Bỏ qua</button>
                                <button type="button" class="btn-fb btn-fb-submit" onclick="submitFeedback('${id}', '${escapeHtml(originalQuery)}')">Gửi góp ý</button>
                            </div>
                        </div>
                    </div>
                </article>
            `;
        }).join("");
    }

    function summarizeConfidence(suggestions = []) {
        const counts = { High: 0, Medium: 0, Low: 0 };
        suggestions.forEach((item) => {
            counts[getConfidenceMeta(item.confidence).label] += 1;
        });
        return `H:${counts.High} M:${counts.Medium} L:${counts.Low}`;
    }

    window.OPEatsComponents = {
        getConfidenceMeta,
        renderSuggestions,
        renderTrace,
        summarizeConfidence,
    };
})();
