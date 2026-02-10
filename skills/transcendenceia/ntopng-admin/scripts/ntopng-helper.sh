#!/bin/bash
# ntopng Admin Helper
# Handles authentication and data retrieval from ntopng 6.4 Community

# Configuration - set via environment variables or credentials file
NTOP_URL="${NTOP_URL:-}"
NTOP_USER="${NTOP_USER:-admin}"
NTOP_PASS="${NTOP_PASS:-}"
NTOP_INSECURE="${NTOP_INSECURE:-false}"

# Load credentials from file if not set
if [[ -z "$NTOP_URL" || -z "$NTOP_PASS" ]]; then
    if [[ -f ~/.ntopng/credentials ]]; then
        source ~/.ntopng/credentials
    fi
fi

# Parse arguments for --insecure flag
while [[ $# -gt 0 ]]; do
    case $1 in
        --insecure|-k)
            NTOP_INSECURE="true"
            shift
            ;;
        *)
            break
            ;;
    esac
done

# Set curl flags based on security preference
INSECURE_FLAG=""
if [[ "$NTOP_INSECURE" == "true" ]]; then
    INSECURE_FLAG="-k"
fi

# Validate configuration
if [[ -z "$NTOP_URL" ]]; then
    echo "Error: NTOP_URL not configured"
    echo "Set NTOP_URL environment variable or create ~/.ntopng/credentials"
    exit 1
fi

if [[ -z "$NTOP_PASS" ]]; then
    echo "Error: NTOP_PASS not configured"
    echo "Set NTOP_PASS environment variable or create ~/.ntopng/credentials"
    exit 1
fi

# Cookie file for session persistence
COOKIE_FILE="/tmp/ntop_cookie_$(id -u).txt"

show_help() {
    cat << EOF
ntopng Admin Helper

Usage: $0 [options] <command>

Options:
    --insecure, -k    Disable SSL certificate validation (NOT recommended)

Commands:
    flows     Get active network flows
    hosts     List hosts by bandwidth usage
    alerts    View security alerts
    status    Check if ntopng is online
    help      Show this help

Environment Variables:
    NTOP_URL          ntopng URL (required)
    NTOP_USER         Username (default: admin)
    NTOP_PASS         Password (required)
    NTOP_INSECURE     Set to 'true' to disable SSL verification (default: false)

Credentials File:
    Create ~/.ntopng/credentials:
    NTOP_URL=https://ntopng.example.com
    NTOP_USER=admin
    NTOP_PASS=your_password

Security Note:
    By default, SSL certificate validation is ENABLED.
    Use --insecure or set NTOP_INSECURE=true only for development
    or when using self-signed certificates in internal networks.

Examples:
    $0 status
    $0 flows
    $0 --insecure flows
    NTOP_URL=https://ntopng.example.com NTOP_PASS=secret $0 hosts
EOF
}

# Login and get session token
get_session() {
    local response
    response=$(curl -s $INSECURE_FLAG -i -X POST "$NTOP_URL/authorize.html" \
        -d "user=$NTOP_USER" \
        -d "password=$NTOP_PASS" \
        -d "referer=/")
    
    if [[ $? -ne 0 ]]; then
        echo "Error: Failed to connect to ntopng" >&2
        return 1
    fi
    
    echo "$response" | grep -i "set-cookie" | awk -F'=' '{print $2}' | awk -F';' '{print $1}' | head -1
}

# Run a query against ntopng
query() {
    local endpoint="$1"
    local session
    
    session=$(get_session)
    
    if [[ -z "$session" ]]; then
        echo "Error: Failed to authenticate with ntopng"
        return 1
    fi
    
    curl -s $INSECURE_FLAG -b "session_3000_0=$session" "$NTOP_URL/lua/$endpoint"
}

# Main command handler
case "${1:-}" in
    flows)
        result=$(query "get_flows_data.lua?ifid=0")
        if [[ -n "$result" ]]; then
            echo "$result" | jq '.' 2>/dev/null || echo "$result"
        else
            echo "Error: No data returned"
            exit 1
        fi
        ;;
    hosts)
        result=$(query "get_hosts_data.lua?ifid=0")
        if [[ -n "$result" ]]; then
            echo "$result" | jq '.' 2>/dev/null || echo "$result"
        else
            echo "Error: No data returned"
            exit 1
        fi
        ;;
    alerts)
        result=$(query "get_alerts_data.lua?ifid=0")
        if [[ -n "$result" ]]; then
            echo "$result" | jq '.' 2>/dev/null || echo "$result"
        else
            echo "Error: No data returned"
            exit 1
        fi
        ;;
    status)
        if query "index.lua" | grep -q "ntopng"; then
            echo "ntopng is ONLINE"
            exit 0
        else
            echo "ntopng is OFFLINE or unreachable"
            exit 1
        fi
        ;;
    help|--help|-h)
        show_help
        exit 0
        ;;
    *)
        echo "Unknown command: ${1:-}"
        show_help
        exit 1
        ;;
esac
