(function () {
  const DEFAULT_ENDPOINT = "/api/feedback";

  function clampRating(value) {
    const rating = Number(value);
    if (!Number.isInteger(rating) || rating < 1 || rating > 5) return 0;
    return rating;
  }

  function confidenceLabel(confidence) {
    return String(confidence || "UNKNOWN").toUpperCase();
  }

  function createButton(label, className) {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = label;
    button.className = className;
    return button;
  }

  function buildWidget(options) {
    const endpoint = options.endpoint || DEFAULT_ENDPOINT;
    const suggestion = options.suggestion || {};
    const query = options.query || "";
    const location = options.location || "Ocean Park 1";

    const root = document.createElement("section");
    root.className = "feedback-widget";
    root.setAttribute("aria-label", "Feedback");

    const title = document.createElement("h3");
    title.textContent = "Kết quả có hữu ích không?";
    root.appendChild(title);

    const stars = document.createElement("div");
    stars.className = "feedback-stars";
    stars.setAttribute("role", "radiogroup");
    stars.setAttribute("aria-label", "Rating");

    let selectedRating = 0;
    const starButtons = [];
    for (let index = 1; index <= 5; index += 1) {
      const star = createButton("★", "feedback-star");
      star.setAttribute("aria-label", `${index} sao`);
      star.setAttribute("role", "radio");
      star.setAttribute("aria-checked", "false");
      star.addEventListener("click", () => {
        selectedRating = index;
        starButtons.forEach((button, buttonIndex) => {
          const active = buttonIndex < selectedRating;
          button.classList.toggle("is-active", active);
          button.setAttribute("aria-checked", active ? "true" : "false");
        });
      });
      starButtons.push(star);
      stars.appendChild(star);
    }
    root.appendChild(stars);

    const outcome = document.createElement("select");
    outcome.className = "feedback-outcome";
    [
      ["unknown", "Chưa đặt món"],
      ["ordered", "Đã đặt thành công"],
      ["skipped", "Không chọn gợi ý"],
      ["delayed", "Giao chậm"],
      ["closed", "Quán đóng cửa"],
      ["unavailable", "Món không có sẵn"],
    ].forEach(([value, label]) => {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = label;
      outcome.appendChild(option);
    });
    root.appendChild(outcome);

    const comment = document.createElement("textarea");
    comment.className = "feedback-comment";
    comment.placeholder = "Bình luận tùy chọn";
    comment.maxLength = 500;
    root.appendChild(comment);

    const actions = document.createElement("div");
    actions.className = "feedback-actions";
    const submit = createButton("Gửi", "feedback-submit");
    const skip = createButton("Bỏ qua", "feedback-skip");
    actions.appendChild(submit);
    actions.appendChild(skip);
    root.appendChild(actions);

    const status = document.createElement("p");
    status.className = "feedback-status";
    status.setAttribute("aria-live", "polite");
    root.appendChild(status);

    skip.addEventListener("click", () => {
      root.classList.add("is-dismissed");
      status.textContent = "";
    });

    submit.addEventListener("click", async () => {
      const rating = clampRating(selectedRating);
      if (!rating) {
        status.textContent = "Vui lòng chọn rating 1-5 sao.";
        return;
      }

      submit.disabled = true;
      status.textContent = "Đang gửi...";
      const payload = {
        query,
        location,
        suggestion_id: String(suggestion.id || suggestion.restaurant_id || ""),
        suggestion_name: suggestion.name || suggestion.restaurant_name || "",
        partner: suggestion.partner || suggestion.vendor || "",
        predicted_eta_min: suggestion.predicted_eta_min || suggestion.eta || null,
        confidence: confidenceLabel(suggestion.confidence),
        user_rating: rating,
        outcome: outcome.value,
        feedback_text: comment.value.trim(),
        source_context: "post_suggestion_widget",
      };

      try {
        const response = await fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        status.textContent = "Đã ghi nhận feedback.";
        root.classList.add("is-submitted");
      } catch (error) {
        status.textContent = "Không gửi được feedback. Hãy thử lại.";
        submit.disabled = false;
      }
    });

    return root;
  }

  window.OceanParkFeedback = {
    mount(container, options) {
      const target = typeof container === "string" ? document.querySelector(container) : container;
      if (!target) throw new Error("Feedback container not found");
      const widget = buildWidget(options || {});
      target.appendChild(widget);
      return widget;
    },
  };
})();
