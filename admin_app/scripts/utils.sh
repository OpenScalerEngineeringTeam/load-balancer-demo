#!/bin/bash
# -------------------------------------------------------------------------------------------------
#   Colorful logs
# -------------------------------------------------------------------------------------------------
GRAY='\e[90m'
RED='\e[31m'
GREEN='\e[32m'
YELLOW='\e[33m'
BLUE='\e[34m'
ECLR='\e[0m' # END COLOR
log() {
    local level="$1"
    local message="$2"
    case "$level" in
        "error") echo -e "${RED}$message${ECLR}" ;;
        "warning") echo -e "${YELLOW}$message${ECLR}" ;;
        "info") echo -e "${BLUE}$message${ECLR}" ;;
        "success") echo -e "${GREEN}$message${ECLR}" ;;
        "debug") echo -e "${GRAY}$message${ECLR}" ;;
        "fatal") echo -e "${RED}$message${ECLR}"; exit 1 ;;
        *) echo "$level: $message";;
    esac
}
