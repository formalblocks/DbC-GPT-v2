#!/bin/bash

# Verification Process Startup Script
# This script manages the startup and monitoring of verification processes

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="/tmp/verification_logs"
MONITOR_LOG="$LOG_DIR/monitor.log"
PROCESS_LOG="$LOG_DIR/process.log"

# Create log directory
mkdir -p "$LOG_DIR"

# Function to log messages with timestamps
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$PROCESS_LOG"
}

# Function to check if a process is running
is_process_running() {
    local process_name="$1"
    pgrep -f "$process_name" > /dev/null 2>&1
}

# Function to start the process monitor
start_monitor() {
    log "Starting process monitor..."
    cd "$SCRIPT_DIR/experiments"
    nohup python3 process_monitor.py > "$MONITOR_LOG" 2>&1 &
    local monitor_pid=$!
    log "Process monitor started with PID: $monitor_pid"
    echo $monitor_pid > /tmp/monitor.pid
}

# Function to start verification with resource management
start_verification() {
    local mode="$1"
    local requested="$2"
    local contexts="$3"
    local assistant="$4"
    local runs="${5:-10}"
    local max_iterations="${6:-10}"
    local max_workers="${7:-2}"
    
    log "Starting verification process..."
    log "Mode: $mode, Requested: $requested, Contexts: $contexts"
    log "Assistant: $assistant, Runs: $runs, Max Iterations: $max_iterations"
    
    cd "$SCRIPT_DIR/experiments"
    
    # Use smaller batches and thread executor for stability
    python3 run_assistants_parallel.py \
        --mode "$mode" \
        --requested "$requested" \
        --contexts "$contexts" \
        --assistant "$assistant" \
        --runs "$runs" \
        --max-iterations "$max_iterations" \
        --max-workers "$max_workers" \
        --executor-type "process" \
        --batch-size "$BATCH_SIZE" \
        2>&1 | tee -a "$PROCESS_LOG"
}

# Function to clean up processes
cleanup() {
    log "Cleaning up processes..."
    
    # Kill monitor if running
    if [ -f /tmp/monitor.pid ]; then
        local monitor_pid=$(cat /tmp/monitor.pid)
        if kill -0 "$monitor_pid" 2>/dev/null; then
            log "Stopping process monitor (PID: $monitor_pid)"
            kill "$monitor_pid"
        fi
        rm -f /tmp/monitor.pid
    fi
    
    # Kill any running verification processes
    pkill -f "run_assistants_parallel.py" || true
    pkill -f "func_by_func_verifier.py" || true
    
    log "Cleanup completed"
}

# Function to check system resources before starting
check_resources() {
    log "Checking system resources..."
    
    # Check available memory
    local mem_available=$(free -m | awk 'NR==2{printf "%.1f", $7/1024}')
    log "Available memory: ${mem_available}GB"
    
    # Convert to integer for comparison (multiply by 10 to handle one decimal place)
    local mem_int=$(echo "$mem_available" | awk '{printf "%.0f", $1*10}')
    if [ "$mem_int" -lt 40 ]; then
        log "WARNING: Low available memory (${mem_available}GB). Consider freeing up memory."
    fi
    
    # Check CPU load
    local load_avg=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
    log "Current load average: $load_avg"
    
    # Check disk space
    local disk_usage=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
    log "Disk usage: ${disk_usage}%"
    
    if [ "$disk_usage" -gt 85 ]; then
        log "WARNING: High disk usage (${disk_usage}%). Consider freeing up disk space."
    fi
}

# Function to show usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

OPTIONS:
    -m, --mode              Verification mode: entire_contract or func_by_func
    -r, --requested         Contract type: erc20, erc721, erc1155, ercx
    -c, --contexts          Context types (comma-separated): erc20,erc721,erc1155
    -a, --assistant         Assistant key (default: all)
    -n, --runs              Number of runs (default: 10)
    -i, --max-iterations    Maximum iterations (default: 10)
    -w, --max-workers       Maximum workers (default: 2)
    -b, --batch-size        Batch size (default: 2)
    --monitor-only          Only start the process monitor
    --cleanup               Clean up running processes
    --check-resources       Only check system resources
    -h, --help              Show this help message

EXAMPLES:
    $0 -m func_by_func -r erc20 -c "erc721,erc1155" -a 4o-mini -n 3 -i 5 -w 2
    $0 --monitor-only
    $0 --cleanup
    $0 --check-resources

EOF
}

# Parse command line arguments
TEMP=$(getopt -o m:r:c:a:n:i:w:b:h --long mode:,requested:,contexts:,assistant:,runs:,max-iterations:,max-workers:,batch-size:,monitor-only,cleanup,check-resources,help -n "$0" -- "$@")

if [ $? != 0 ]; then
    echo "Error parsing arguments" >&2
    exit 1
fi

eval set -- "$TEMP"

# Default values
MODE=""
REQUESTED=""
CONTEXTS=""
ASSISTANT="all"
RUNS=10
MAX_ITERATIONS=10
MAX_WORKERS=2
MONITOR_ONLY=false
CLEANUP_ONLY=false
CHECK_RESOURCES_ONLY=false
BATCH_SIZE=2

while true; do
    case "$1" in
        -m|--mode)
            MODE="$2"
            shift 2
            ;;
        -r|--requested)
            REQUESTED="$2"
            shift 2
            ;;
        -c|--contexts)
            CONTEXTS="$2"
            shift 2
            ;;
        -a|--assistant)
            ASSISTANT="$2"
            shift 2
            ;;
        -n|--runs)
            RUNS="$2"
            shift 2
            ;;
        -i|--max-iterations)
            MAX_ITERATIONS="$2"
            shift 2
            ;;
        -w|--max-workers)
            MAX_WORKERS="$2"
            shift 2
            ;;
        -b|--batch-size)
            BATCH_SIZE="$2"
            shift 2
            ;;
        --monitor-only)
            MONITOR_ONLY=true
            shift
            ;;
        --cleanup)
            CLEANUP_ONLY=true
            shift
            ;;
        --check-resources)
            CHECK_RESOURCES_ONLY=true
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Internal error!" >&2
            exit 1
            ;;
    esac
done

# Set up signal handlers for graceful shutdown
trap cleanup EXIT INT TERM

# Main execution
log "=== Verification Startup Script Started ==="

if [ "$CLEANUP_ONLY" = true ]; then
    cleanup
    exit 0
fi

if [ "$CHECK_RESOURCES_ONLY" = true ]; then
    check_resources
    exit 0
fi

# Check system resources
check_resources

# Start monitor if not running
if ! is_process_running "process_monitor.py"; then
    start_monitor
else
    log "Process monitor already running"
fi

if [ "$MONITOR_ONLY" = true ]; then
    log "Monitor-only mode. Process monitor is running."
    wait
    exit 0
fi

# Validate required parameters
if [ -z "$MODE" ] || [ -z "$REQUESTED" ]; then
    echo "Error: --mode and --requested are required" >&2
    usage
    exit 1
fi

# Start verification process
start_verification "$MODE" "$REQUESTED" "$CONTEXTS" "$ASSISTANT" "$RUNS" "$MAX_ITERATIONS" "$MAX_WORKERS"

log "=== Verification Process Completed ===" 