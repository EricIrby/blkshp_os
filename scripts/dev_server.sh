#!/usr/bin/env bash

set -euo pipefail

# Helper to run the BLKSHP bench development stack in the background.
# Usage:
#   ./scripts/dev_server.sh start|stop|restart|status|logs
# Environment overrides:
#   BENCH_ROOT  (defaults to auto-detected bench root)
#   BENCH_CLI   (defaults to bench from PATH or $BENCH_ROOT/env/bin/bench)
#   BENCH_ENV   (defaults to $BENCH_ROOT/env or the bench CLI parent env)
#   HONCHO_BIN  (defaults to honcho inside BENCH_ENV or discovered on PATH)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
find_bench_root() {
	local current="${SCRIPT_DIR}"
	while [[ "${current}" != "/" ]]; do
		if [[ -f "${current}/Procfile" && -d "${current}/sites" ]]; then
			printf "%s" "${current}"
			return 0
		fi
		current="$(dirname "${current}")"
	done
	printf "%s" "${SCRIPT_DIR}"
	return 0
}

DEFAULT_BENCH_ROOT="$(find_bench_root)"

BENCH_ROOT="${BENCH_ROOT:-$DEFAULT_BENCH_ROOT}"

if [[ -z "${BENCH_CLI:-}" ]]; then
	if command -v bench >/dev/null 2>&1; then
		BENCH_CLI="$(command -v bench)"
	elif [[ -x "${BENCH_ROOT}/env/bin/bench" ]]; then
		BENCH_CLI="${BENCH_ROOT}/env/bin/bench"
	else
		BENCH_CLI=""
	fi
fi

CLI_BIN_DIR=""
if [[ -n "${BENCH_CLI}" ]]; then
	CLI_BIN_DIR="$(dirname "${BENCH_CLI}")"
fi

if [[ -z "${BENCH_ENV:-}" ]]; then
	if [[ -d "${BENCH_ROOT}/env" ]]; then
		BENCH_ENV="${BENCH_ROOT}/env"
	elif [[ -n "${CLI_BIN_DIR}" ]]; then
		if BENCH_ENV="$(cd "${CLI_BIN_DIR}/.." >/dev/null 2>&1 && pwd)"; then
			:
		else
			BENCH_ENV=""
		fi
	else
		BENCH_ENV=""
	fi
fi

if [[ -z "${HONCHO_BIN:-}" && -n "${BENCH_ENV}" ]]; then
	HONCHO_BIN="${BENCH_ENV}/bin/honcho"
fi

PID_FILE="${BENCH_ROOT}/config/dev_server.pid"
LOG_FILE="${BENCH_ROOT}/logs/dev-server.log"

ensure_requirements() {
	if [[ -z "${BENCH_CLI}" || ! -x "${BENCH_CLI}" ]]; then
		echo "bench executable not found. Set BENCH_CLI or ensure bench is on PATH." >&2
		exit 1
	fi

	if [[ -z "${HONCHO_BIN:-}" || ! -x "${HONCHO_BIN}" ]]; then
		if command -v honcho >/dev/null 2>&1; then
			HONCHO_BIN="$(command -v honcho)"
		else
			if [[ -n "${BENCH_ENV}" ]]; then
				echo "honcho executable not found (looked for ${HONCHO_BIN:-${BENCH_ENV}/bin/honcho})." >&2
				echo "Install it with: ${BENCH_ENV}/bin/pip install honcho (or ensure honcho is on PATH)." >&2
			else
				echo "honcho executable not found. Install it with: pip install honcho (or set HONCHO_BIN)." >&2
			fi
			exit 1
		fi
	fi

	mkdir -p "$(dirname "${LOG_FILE}")"
}

is_running() {
	local pid
	if [[ -f "${PID_FILE}" ]]; then
		pid="$(cat "${PID_FILE}")"
		if [[ -n "${pid}" && "${pid}" =~ ^[0-9]+$ ]]; then
			if kill -0 "${pid}" >/dev/null 2>&1; then
				return 0
			fi
		fi
	fi

	if pgrep -f "frappe.utils.bench_helper frappe" >/dev/null 2>&1; then
		return 0
	fi

	return 1
}

start() {
	if is_running; then
		echo "Bench dev server already running."
		return
	fi

	ensure_requirements

	echo "Starting bench dev server..."
	cd "${BENCH_ROOT}"

	local path_prefix=""
	if [[ -n "${BENCH_ENV}" ]]; then
		path_prefix="${BENCH_ENV}/bin"
	fi
	if [[ -n "${CLI_BIN_DIR}" ]]; then
		if [[ -n "${path_prefix}" ]]; then
			path_prefix="${path_prefix}:${CLI_BIN_DIR}"
		else
			path_prefix="${CLI_BIN_DIR}"
		fi
	fi
	if [[ -n "${path_prefix}" ]]; then
		path_prefix="${path_prefix}:${PATH}"
	else
		path_prefix="${PATH}"
	fi

	nohup env \
		PATH="${path_prefix}" \
		"${BENCH_CLI}" start -m "${HONCHO_BIN}" \
		>>"${LOG_FILE}" 2>&1 &

	local pid=$!
	echo "${pid}" > "${PID_FILE}"

	echo "Bench dev server started (PID ${pid}). Logs: ${LOG_FILE}"
}

stop() {
	echo "Stopping bench dev server..."

	if [[ -f "${PID_FILE}" ]]; then
		local pid
		pid="$(cat "${PID_FILE}")"
		if [[ -n "${pid}" && "${pid}" =~ ^[0-9]+$ ]]; then
			if kill -0 "${pid}" >/dev/null 2>&1; then
				kill "${pid}" >/dev/null 2>&1 || true
				wait "${pid}" 2>/dev/null || true
			fi
		fi
		rm -f "${PID_FILE}"
	fi

	# Clean up any stray helpers from previous runs.
	pkill -f "frappe.utils.bench_helper frappe" >/dev/null 2>&1 || true
	pkill -f "node esbuild --watch --live-reload" >/dev/null 2>&1 || true
	pkill -f "honcho start" >/dev/null 2>&1 || true

	echo "Bench dev server stopped."
}

status() {
	if is_running; then
		echo "Bench dev server appears to be running."
		ps aux | grep -E "bench_helper|honcho start" | grep -v grep || true
	else
		echo "Bench dev server is not running."
	fi
}

logs() {
	if [[ -f "${LOG_FILE}" ]]; then
		tail -n 100 -f "${LOG_FILE}"
	else
		echo "No log file found at ${LOG_FILE}" >&2
		exit 1
	fi
}

usage() {
	cat <<EOF
Usage: $(basename "$0") {start|stop|restart|status|logs}
EOF
	exit 1
}

main() {
	case "${1:-}" in
		start)
			start
			;;
		stop)
			stop
			;;
		restart)
			stop
			start
			;;
		status)
			status
			;;
		logs)
			logs
			;;
		*)
			usage
			;;
	esac
}

main "$@"

