#!/bin/sh

set -e

# Save current state
save_state() {
    # Save Git stash if needed
    git stash push -m "Dev container shutdown $(date +%Y%m%d_%H%M%S)" || true
}

# Main
save_state