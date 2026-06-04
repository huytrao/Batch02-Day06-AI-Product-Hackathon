const API_BASE_URL = window.OP_EATS_API_BASE_URL || "http://127.0.0.1:8001";

const els = {
    form: document.getElementById("searchForm"),
    query: document.getElementById("queryInput"),
    location: document.getElementById("locationInput"),
    loading: document.getElementById("loadingIndicator"),
    empty: document.getElementById("emptyState"),
    results: document.getElementById("resultsArea"),
    latency: document.getElementById("latencyBadge"),
    confidenceMix: document.getElementById("confidenceMix"),
    monetization: document.getElementById("monetizationSignal"),
    traceToggle: document.getElementById("traceToggle"),
    traceBody: document.getElementById("traceBody"),
};

function setLoading(isLoading) {
    els.loading.hidden = !isLoading;
    els.empty.hidden = true;
    els.results.hidden = isLoading;
}

function toggleTrace() {
    const nextExpanded = els.traceBody.hidden;
    els.traceBody.hidden = !nextExpanded;
    els.traceToggle.setAttribute("aria-expanded", String(nextExpanded));
    els.traceToggle.textContent = nextExpanded ? "Ẩn trace" : "Xem trace";
}

function toggleFeedback(suggestionId) {
    const widget = document.getElementById(`fb-widget-${suggestionId}`);
    if (widget) widget.hidden = !widget.hidden;
}

function selectStar(suggestionId, rating) {
    const container = document.getElementById(`stars-${suggestionId}`);
    if (!container) return;

    const stars = Array.from(container.getElementsByClassName("star"));
    container.setAttribute("data-rating", rating);
    stars.forEach((star, index) => {
        star.classList.toggle("active", index < rating);
    });
}

function skipFeedback(suggestionId) {
    const widget = document.getElementById(`fb-widget-${suggestionId}`);
    if (widget) widget.hidden = true;
}

async function requestJson(url, options) {
    const response = await fetch(url, options);
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }
    return response.json();
}

function normalizeApiData(data) {
    const suggestions = data.suggestions || data.results || data.items || data || [];
    const actionTrace = data.action_trace || data.trace || data.agent_trace || [
        { step: 1, type: "api", thought: "Backend trả về gợi ý mà không có trace cụ thể." },
    ];

    return {
        execution_time_ms: data.execution_time_ms || data.latency_ms || data.elapsed_ms,
        suggestions: Array.isArray(suggestions) ? suggestions : [],
        action_trace: Array.isArray(actionTrace) ? actionTrace : [],
    };
}

async function fetchSuggestions(query, location) {
    try {
        const data = await requestJson(`${API_BASE_URL}/api/query`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query, location }),
        });
        return normalizeApiData(data);
    } catch (postError) {
        const params = new URLSearchParams({ location, q: query, limit: "3" });
        const data = await requestJson(`${API_BASE_URL}/suggestions?${params.toString()}`);
        return normalizeApiData(data);
    }
}

function renderResult(data, query, startedAt, sourceLabel) {
    const renderStart = performance.now();

    window.OPEatsComponents.renderTrace(data.action_trace);
    window.OPEatsComponents.renderSuggestions(data.suggestions, query);

    const renderMs = Math.round(performance.now() - renderStart);
    const totalMs = Math.round(performance.now() - startedAt);
    const apiMs = data.execution_time_ms ? `${data.execution_time_ms}ms API` : `${totalMs}ms total`;

    els.latency.textContent = `${apiMs} / render ${renderMs}ms${sourceLabel ? ` (${sourceLabel})` : ""}`;
    els.confidenceMix.textContent = window.OPEatsComponents.summarizeConfidence(data.suggestions);
    els.monetization.textContent = data.suggestions.some((item) => item.sponsored || item.is_partner)
        ? "Đối tác hiển thị"
        : "Chỉ có tín hiệu đối tác";

    els.loading.hidden = true;
    els.empty.hidden = true;
    els.results.hidden = false;
}

async function submitQuery(event) {
    if (event) event.preventDefault();

    const query = els.query.value.trim();
    const location = els.location.value.trim() || "Ocean Park 1";

    if (!query) {
        els.empty.hidden = false;
        els.empty.innerHTML = "<h2>Cần thêm thông tin</h2><p>Nhập món ăn, ngân sách hoặc mục tiêu thời gian để agent xếp hạng quán.</p>";
        return;
    }

    const startedAt = performance.now();
    setLoading(true);

    try {
        const data = await fetchSuggestions(query, location);
        renderResult(data, query, startedAt, "");
    } catch (error) {
        console.warn("Backend unavailable, using local demo data.", error);
        const mockData = generateMockData(query, location);
        renderResult(mockData, query, startedAt, "demo");
    }
}

async function submitFeedback(suggestionId, query) {
    const stars = document.getElementById(`stars-${suggestionId}`);
    const text = document.getElementById(`text-${suggestionId}`);
    const rating = Number(stars?.getAttribute("data-rating") || 0);

    if (!rating) {
        alert("Vui lòng chọn số sao trước khi gửi.");
        return;
    }

    const payload = {
        query,
        suggestion_id: suggestionId,
        rating,
        text: text?.value.trim() || "",
    };

    try {
        await requestJson(`${API_BASE_URL}/api/feedback`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });
    } catch (error) {
        console.warn("Feedback API unavailable; keeping demo confirmation.", error);
    }

    const widget = document.getElementById(`fb-widget-${suggestionId}`);
    if (widget) {
        widget.innerHTML = '<p class="notice">Cảm ơn góp ý của bạn.</p>';
        widget.hidden = false;
    }
}

function generateMockData(query, location) {
    const cleanQuery = query.replace(/\s+/g, " ").trim();
    const lowIntent = /chay|khong chac|gia|30-50|re/i.test(cleanQuery);

    return {
        execution_time_ms: 186,
        action_trace: [
            {
                step: 1,
                type: "search",
                thought: `Tìm quán gần ${location} phù hợp yêu cầu: "${cleanQuery}".`,
            },
            {
                step: 2,
                type: "estimate_eta",
                thought: "Ước tính ETA từ tín hiệu GrabFood, ShopeeFood, khoảng cách tòa nhà và báo cáo gần đây.",
            },
            {
                step: 3,
                type: "rank",
                thought: "Chọn các lựa chọn có ETA tốt nhất nhưng không đẩy độ tin cậy thấp lên hàng đầu nếu có xung đột nguồn.",
            },
        ],
        suggestions: [
            {
                id: "grab-a",
                name: lowIntent ? "Bún Chay An Nhiên" : "Phở Bò S1 Express",
                vendor: "GrabFood",
                predicted_eta: lowIntent ? "35-50" : "28-35",
                confidence: lowIntent ? 0.62 : 0.85,
                sponsored: true,
                rationale: lowIntent
                    ? "Có thực đơn phù hợp nhưng nguồn giá cập nhật chưa đồng nhất, nên xem thực đơn trước khi đặt."
                    : "ETA ổn định trong khung 30-40 phút, gần tòa S1 và có nguồn giao hàng gần đây.",
                evidence_links: ["https://www.grab.com/vn/food/", "https://www.google.com/maps/search/Ocean+Park+1+pho"],
                menu_url: "https://www.grab.com/vn/food/",
            },
            {
                id: "shopee-b",
                name: lowIntent ? "Cơm Thố Anh Nguyễn" : "Cơm Tấm Sài Gòn OP1",
                vendor: "ShopeeFood",
                predicted_eta: lowIntent ? "40-60" : "34-42",
                confidence: lowIntent ? 0.32 : 0.74,
                rationale: lowIntent
                    ? "Tín hiệu giá và thời gian giao mâu thuẫn; nên gọi/xem thực đơn vì có báo cáo cũ về giá."
                    : "Nguồn giao hàng phù hợp, ETA thấp hơn ngưỡng 45 phút và ít báo cáo trễ gần đây.",
                evidence_links: ["https://shopeefood.vn/", "https://www.google.com/maps/search/Ocean+Park+1+com+tam"],
                menu_url: "https://shopeefood.vn/",
            },
            {
                id: "local-c",
                name: "Bánh Mì Anh Đông",
                vendor: "Community report",
                predicted_eta: "25-35",
                confidence: 0.56,
                rationale: "Tốc độ nhanh theo báo cáo cộng đồng nhưng nguồn không phải nền tảng giao hàng trực tiếp.",
                evidence_links: ["https://www.google.com/maps/search/Ocean+Park+1+banh+mi"],
            },
        ],
    };
}

els.form.addEventListener("submit", submitQuery);
els.traceToggle.addEventListener("click", toggleTrace);
document.querySelectorAll("[data-query]").forEach((button) => {
    button.addEventListener("click", () => {
        els.query.value = button.dataset.query;
        submitQuery();
    });
});

window.submitQuery = submitQuery;
window.toggleTrace = toggleTrace;
window.toggleFeedback = toggleFeedback;
window.selectStar = selectStar;
window.skipFeedback = skipFeedback;
window.submitFeedback = submitFeedback;
