#!/usr/bin/env bash
set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WEB_DIR="$ROOT_DIR/web"
ARTIFACT_DIR="$ROOT_DIR/artifacts"
LOG_FILE="$ARTIFACT_DIR/deploy_log.md"
SUCCESS_FILE="$ARTIFACT_DIR/deploy_success.md"

if [ -f "$ROOT_DIR/.env" ]; then
    set -a
    # shellcheck disable=SC1091
    . "$ROOT_DIR/.env"
    set +a
fi

PROJECT_NAME="${CF_PAGES_PROJECT:-ocean-park-1-eats}"
BRANCH_NAME="${CF_PAGES_BRANCH:-main}"
STARTED_AT="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
TMP_LOG="$(mktemp)"

mkdir -p "$ARTIFACT_DIR"

if [ ! -f "$LOG_FILE" ]; then
    printf "# Cloudflare Pages Deploy Log\n\n" > "$LOG_FILE"
fi

append_log() {
    {
        printf -- "## %s\n" "$STARTED_AT"
        printf -- "- Project: \`%s\`\n" "$PROJECT_NAME"
        printf -- "- Directory: \`web/\`\n"
        printf -- "- Branch: \`%s\`\n" "$BRANCH_NAME"
        printf -- "- Commit: \`%s\`\n" "$(git -C "$ROOT_DIR" rev-parse --short HEAD 2>/dev/null || printf "unknown")"
        printf -- "- Status: %s\n" "$1"
        printf -- "- Finished at: \`%s\`\n" "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
        printf -- "- Public URL: %s\n" "$2"
        printf -- "- Notes: %s\n\n" "$3"
        printf "<details><summary>Deploy output</summary>\n\n"
        printf '```text\n'
        tail -n 120 "$TMP_LOG" | sed -E $'s/\x1b\\[[0-9;]*[[:alpha:]]//g'
        printf '\n```\n'
        printf "</details>\n\n"
    } >> "$LOG_FILE"
}

if [ ! -d "$WEB_DIR" ]; then
    printf "Missing web directory: %s\n" "$WEB_DIR" | tee "$TMP_LOG"
    append_log "failed" "n/a" "Create web/ before deploying."
    exit 1
fi

if command -v wrangler >/dev/null 2>&1; then
    DEPLOY_CMD=(wrangler pages deploy "$WEB_DIR" --project-name "$PROJECT_NAME" --branch "$BRANCH_NAME" --commit-dirty=true)
else
    DEPLOY_CMD=(npx wrangler pages deploy "$WEB_DIR" --project-name "$PROJECT_NAME" --branch "$BRANCH_NAME" --commit-dirty=true)
fi

if [ -n "${CLOUDFLARE_API_TOKEN:-}" ]; then
    printf "Using CLOUDFLARE_API_TOKEN from environment/.env.\n" | tee "$TMP_LOG"
else
    printf "No CLOUDFLARE_API_TOKEN found; using Wrangler OAuth login session.\n" | tee "$TMP_LOG"
fi
printf "Deploying %s to Cloudflare Pages project %s...\n" "$WEB_DIR" "$PROJECT_NAME" | tee -a "$TMP_LOG"
"${DEPLOY_CMD[@]}" 2>&1 | tee -a "$TMP_LOG"
STATUS=${PIPESTATUS[0]}

PUBLIC_URL="$(grep -Eo 'https://[^[:space:]]+\.pages\.dev[^[:space:]]*' "$TMP_LOG" | tail -n 1 || true)"
if [ -z "$PUBLIC_URL" ]; then
    PUBLIC_URL="n/a"
fi

if [ "$STATUS" -eq 0 ]; then
    append_log "success" "$PUBLIC_URL" "Cloudflare Pages deploy completed."
    {
        printf "# Deploy Success\n\n"
        printf -- "- Status: success\n"
        printf -- "- Public URL: %s\n" "$PUBLIC_URL"
        printf -- "- Platform: Cloudflare Pages\n"
        printf -- "- Project: \`%s\`\n" "$PROJECT_NAME"
        printf -- "- Source directory: \`web/\`\n"
        printf -- "- Deploy time: \`%s\`\n\n" "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
        printf "Run again:\n"
        printf '```bash\n'
        printf "bash scripts/deploy_cloudflare.sh\n"
        printf '```\n'
    } > "$SUCCESS_FILE"
    printf "Deploy success: %s\n" "$PUBLIC_URL"
else
    if grep -q "Authentication error" "$TMP_LOG"; then
        append_log "failed" "$PUBLIC_URL" "Cloudflare token was loaded, but API authentication failed. Create a fresh token with Cloudflare Pages edit permissions, or run \`npx wrangler login\` interactively."
    else
        append_log "failed" "$PUBLIC_URL" "Run \`npx wrangler login\` or set \`CLOUDFLARE_API_TOKEN\`, then rerun this script."
    fi
    printf "Deploy failed. See %s\n" "$LOG_FILE"
fi

rm -f "$TMP_LOG"
exit "$STATUS"
