# Feedback, Evaluation, Evidence Log & Monetization

Owner: Member E - Trảo An Huy

## What This Adds

- Feedback persistence in `data/feedback.sqlite`.
- Post-suggestion feedback widget in `web/feedback-widget.js`.
- Analytics report generation via `scripts/generate_report.py`.
- Automatic evaluation logging via `scripts/run_evaluation.py`.
- Automatic evidence collection via `scripts/collect_evidence.py`.
- Optional FastAPI request/response logging via `api/request_logger.py`.
- Transparent partner metrics and sponsorship hooks in `api/monetization.py`.

## Run Feedback DB

```bash
python api/feedback_db.py
```

## Generate Analytics Report

```bash
python scripts/generate_report.py
```

Output: `artifacts/weekly_feedback_report.json`

## Run Evaluation And Evidence Logging

Start the API first if available, then:

```bash
python scripts/run_evaluation.py
python scripts/collect_evidence.py --deploy-url https://your-project.pages.dev
```

Outputs:

- `artifacts/evaluation_log.md`
- `artifacts/evidence_log.md`
- `artifacts/request_response_log.jsonl` when API middleware is installed

## Add Request Logger To FastAPI

```python
from request_logger import install_request_logger

install_request_logger(app)
```

The logger redacts obvious PII and does not store headers, cookies, IP addresses, phone numbers, emails, device identifiers, or addresses.

## Frontend Widget

Include `web/feedback-widget.js`, then mount it after rendering a suggestion:

```html
<script src="feedback-widget.js"></script>
```

```javascript
OceanParkFeedback.mount("#feedback", {
  endpoint: "/api/feedback",
  query: currentQuery,
  location: "Ocean Park 1",
  suggestion: selectedSuggestion
});
```

## Monetization Guardrails

- Sponsored recommendations must be clearly labeled.
- Sponsorship cannot promote low-confidence suggestions.
- Partner stats are exposed through the intended API contract: `GET /api/partner-stats?partner=GrabFood`.
- No PII is used for monetization metrics.
