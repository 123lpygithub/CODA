#!/usr/bin/env bash

set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
API_HOST="${CODA_API_HOST:-127.0.0.1}"
API_PORT="${CODA_API_PORT:-8003}"
FRONTEND_HOST="${CODA_FRONTEND_HOST:-127.0.0.1}"
FRONTEND_PORT="${CODA_FRONTEND_PORT:-5173}"
RUNS_ROOT="${CODA_RUNS_ROOT:-runs/web}"
API_URL="http://${API_HOST}:${API_PORT}"

command -v python >/dev/null || {
    printf '错误：未找到 python。\n'
    exit 1
}
command -v npm >/dev/null || {
    printf '错误：未找到 npm。\n'
    exit 1
}
command -v curl >/dev/null || {
    printf '错误：未找到 curl，无法检查后端是否启动成功。\n'
    exit 1
}

cd "$ROOT_DIR"

# Resolve all role-specific credentials through the same configuration as the
# API. Print configuration and missing variable names, never credential values.
python scripts/check_llm_config.py --require-keys

backend_pid=''
frontend_pid=''

cleanup() {
    trap - EXIT INT TERM
    if [[ -n "$frontend_pid" ]] && kill -0 "$frontend_pid" 2>/dev/null; then
        kill "$frontend_pid" 2>/dev/null || true
    fi
    if [[ -n "$backend_pid" ]] && kill -0 "$backend_pid" 2>/dev/null; then
        kill "$backend_pid" 2>/dev/null || true
    fi
    wait 2>/dev/null || true
}
trap cleanup EXIT INT TERM

printf '启动 CODA 后端：%s\n' "$API_URL"
python scripts/run_web_api.py \
    --host "$API_HOST" \
    --port "$API_PORT" \
    --runs-root "$RUNS_ROOT" &
backend_pid=$!

health_ready=0
for _ in $(seq 1 60); do
    if curl --fail --silent --show-error "$API_URL/api/health" >/dev/null 2>&1; then
        health_ready=1
        break
    fi
    if ! kill -0 "$backend_pid" 2>/dev/null; then
        printf '错误：后端启动失败。\n'
        exit 1
    fi
    sleep 1
done

if [[ "$health_ready" -ne 1 ]]; then
    printf '错误：后端在 60 秒内没有通过健康检查：%s/api/health\n' "$API_URL"
    exit 1
fi

printf '后端已就绪，模型配置见上方检查结果。\n'
printf '启动前端：http://%s:%s\n' "$FRONTEND_HOST" "$FRONTEND_PORT"
cd "$ROOT_DIR/frontend"
VITE_API_BASE_URL="$API_URL" npm run dev -- \
    --host "$FRONTEND_HOST" \
    --port "$FRONTEND_PORT" &
frontend_pid=$!

printf '\n浏览器打开：http://%s:%s\n' "$FRONTEND_HOST" "$FRONTEND_PORT"
printf '按 Ctrl+C 同时停止前后端。\n\n'

wait "$frontend_pid"
