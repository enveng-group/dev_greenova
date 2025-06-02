#!/usr/bin/awk -f
#
# data_manager.awk - Data management module for whitespace-delimited databases
#
# POSIX AWK implementation for managing the tool's data storage
# Provides functions for reading, writing, and querying the databases

BEGIN {
    # Database file paths
    PATTERNS_DB = "data/conflict_patterns.dat"
    CONFIG_DB = "data/repository_config.dat"
    HISTORY_DB = "data/analysis_history.dat"
    RULES_DB = "data/risk_rules.dat"

    # Field separators and data structures
    FS = " "
    OFS = " "

    # Initialize arrays
    delete patterns
    delete configs
    delete history
    delete rules

    # Operation mode
    if (OPERATION == "") OPERATION = "query"
}

# Load conflict patterns database
function load_patterns(    line, fields, n) {
    while ((getline line < PATTERNS_DB) > 0) {
        # Skip comments and empty lines
        if (line ~ /^#/ || line ~ /^[[:space:]]*$/) continue

        # Parse fields
        n = split(line, fields, /[[:space:]]+/)
        if (n >= 6) {
            # Simplified pattern storage without multi-dimensional arrays
            pattern_key = fields[1] "_id"
            patterns[pattern_key] = fields[1]
            pattern_key = fields[1] "_extension"
            patterns[pattern_key] = fields[2]
            pattern_key = fields[1] "_probability"
            patterns[pattern_key] = fields[3]
            pattern_key = fields[1] "_base_score"
            patterns[pattern_key] = fields[4]
            pattern_key = fields[1] "_modifiers"
            patterns[pattern_key] = fields[5]
            pattern_key = fields[1] "_description"
            patterns[pattern_key] = ""
            for (i = 6; i <= n; i++) {
                patterns[pattern_key] = patterns[pattern_key] (i > 6 ? " " : "") fields[i]
            }
        }
    }
    close(PATTERNS_DB)
}

# Load repository configuration database
function load_configs(    line, fields, n) {
    while ((getline line < CONFIG_DB) > 0) {
        # Skip comments and empty lines
        if (line ~ /^#/ || line ~ /^[[:space:]]*$/) continue

        # Parse fields
        n = split(line, fields, /[[:space:]]+/)
        if (n >= 6) {
            configs[fields[1]]["path"] = fields[1]
            configs[fields[1]]["branch_pattern"] = fields[2]
            configs[fields[1]]["exclude_patterns"] = fields[3]
            configs[fields[1]]["priority_files"] = fields[4]
            configs[fields[1]]["check_frequency"] = fields[5]
            configs[fields[1]]["last_check"] = fields[6]
        }
    }
    close(CONFIG_DB)
}

# Load analysis history database
function load_history(    line, fields, n) {
    while ((getline line < HISTORY_DB) > 0) {
        # Skip comments and empty lines
        if (line ~ /^#/ || line ~ /^[[:space:]]*$/) continue

        # Parse fields
        n = split(line, fields, /[[:space:]]+/)
        if (n >= 7) {
            history[fields[1]]["timestamp"] = fields[1]
            history[fields[1]]["repo_path"] = fields[2]
            history[fields[1]]["branch_name"] = fields[3]
            history[fields[1]]["conflict_score"] = fields[4]
            history[fields[1]]["files_analyzed"] = fields[5]
            history[fields[1]]["conflicts_found"] = fields[6]
            history[fields[1]]["status"] = fields[7]
            history[fields[1]]["report_file"] = (n >= 8) ? fields[8] : ""
        }
    }
    close(HISTORY_DB)
}

# Load risk rules database
function load_rules(    line, fields, n) {
    while ((getline line < RULES_DB) > 0) {
        # Skip comments and empty lines
        if (line ~ /^#/ || line ~ /^[[:space:]]*$/) continue

        # Parse fields
        n = split(line, fields, /[[:space:]]+/)
        if (n >= 6) {
            rules[fields[1]]["id"] = fields[1]
            rules[fields[1]]["condition_type"] = fields[2]
            rules[fields[1]]["condition_value"] = fields[3]
            rules[fields[1]]["risk_multiplier"] = fields[4]
            rules[fields[1]]["severity"] = fields[5]
            rules[fields[1]]["description"] = ""
            for (i = 6; i <= n; i++) {
                rules[fields[1]]["description"] = rules[fields[1]]["description"] (i > 6 ? " " : "") fields[i]
            }
        }
    }
    close(RULES_DB)
}

# Get conflict pattern by file extension
function get_pattern_by_extension(ext,    pattern_id) {
    load_patterns()

    # First try exact match
    for (pattern_id in patterns) {
        if (patterns[pattern_id]["extension"] == ext) {
            return pattern_id
        }
    }

    # Fall back to wildcard
    for (pattern_id in patterns) {
        if (patterns[pattern_id]["extension"] == "*") {
            return pattern_id
        }
    }

    return ""
}

# Get repository configuration
function get_repo_config(repo_path,    config_path) {
    load_configs()

    # Try exact match first
    if (repo_path in configs) {
        return repo_path
    }

    # Try partial matches
    for (config_path in configs) {
        if (index(repo_path, config_path) == 1) {
            return config_path
        }
    }

    return ""
}

# Calculate risk score for a file
function calculate_risk_score(filename, file_size, change_freq, author_count,    ext, pattern_id, base_score, multiplier, rule_id) {
    # Get file extension
    if (match(filename, /\.([^.]+)$/)) {
        ext = "." substr(filename, RSTART + 1)
    } else {
        ext = "*"
    }

    # Get base pattern score
    pattern_id = get_pattern_by_extension(ext)
    if (pattern_id != "") {
        base_score = patterns[pattern_id]["base_score"] / 100.0
    } else {
        base_score = 0.4  # Default score
    }

    # Apply risk rules
    load_rules()
    multiplier = 1.0

    for (rule_id in rules) {
        if (rules[rule_id]["condition_type"] == "FILE_SIZE" && file_size > rules[rule_id]["condition_value"]) {
            multiplier *= rules[rule_id]["risk_multiplier"]
        } else if (rules[rule_id]["condition_type"] == "CHANGE_FREQUENCY" && change_freq > rules[rule_id]["condition_value"]) {
            multiplier *= rules[rule_id]["risk_multiplier"]
        } else if (rules[rule_id]["condition_type"] == "AUTHOR_COUNT" && author_count > rules[rule_id]["condition_value"]) {
            multiplier *= rules[rule_id]["risk_multiplier"]
        }
    }

    return base_score * multiplier
}

# Add analysis record to history
function add_history_record(repo_path, branch_name, conflict_score, files_analyzed, conflicts_found, status, report_file,    timestamp) {
    timestamp = systime()

    # Append to history file
    printf "%d %s %s %.2f %d %d %s %s\n", timestamp, repo_path, branch_name, conflict_score, files_analyzed, conflicts_found, status, report_file >> HISTORY_DB
    close(HISTORY_DB)

    return timestamp
}

# Update repository configuration
function update_repo_config(repo_path, last_check_time,    temp_file, line) {
    temp_file = CONFIG_DB ".tmp"

    # Read and update configuration
    while ((getline line < CONFIG_DB) > 0) {
        if (line ~ /^#/ || line ~ /^[[:space:]]*$/) {
            print line >> temp_file
        } else if (index(line, repo_path) == 1) {
            # Update last check time
            sub(/[0-9]+$/, last_check_time, line)
            print line >> temp_file
        } else {
            print line >> temp_file
        }
    }
    close(CONFIG_DB)
    close(temp_file)

    # Replace original file
    system("mv " temp_file " " CONFIG_DB)
}

# Query functions for external use
function query_patterns(ext) {
    pattern_id = get_pattern_by_extension(ext)
    if (pattern_id != "") {
        printf "Pattern: %s, Extension: %s, Probability: %s, Score: %s\n", \
               pattern_id, patterns[pattern_id]["extension"], \
               patterns[pattern_id]["probability"], patterns[pattern_id]["base_score"]
    }
}

function query_recent_history(repo_path, limit,    timestamp, count) {
    load_history()
    count = 0

    # Sort by timestamp (descending) and show recent entries
    for (timestamp in history) {
        if (history[timestamp]["repo_path"] == repo_path || repo_path == "") {
            printf "Time: %s, Repo: %s, Branch: %s, Score: %s, Status: %s\n", \
                   timestamp, history[timestamp]["repo_path"], \
                   history[timestamp]["branch_name"], history[timestamp]["conflict_score"], \
                   history[timestamp]["status"]
            count++
            if (limit > 0 && count >= limit) break
        }
    }
}

# Main processing
{
    if (OPERATION == "query_pattern") {
        query_patterns(QUERY_PARAM)
    } else if (OPERATION == "query_history") {
        query_recent_history(QUERY_PARAM, LIMIT)
    } else if (OPERATION == "calculate_risk") {
        score = calculate_risk_score(FILENAME, FILE_SIZE, CHANGE_FREQ, AUTHOR_COUNT)
        printf "%.3f\n", score
    } else if (OPERATION == "add_record") {
        timestamp = add_history_record(REPO_PATH, BRANCH_NAME, CONFLICT_SCORE, FILES_ANALYZED, CONFLICTS_FOUND, STATUS, REPORT_FILE)
        printf "%d\n", timestamp
    }
}

END {
    # Cleanup
    if (OPERATION == "load_all") {
        load_patterns()
        load_configs()
        load_history()
        load_rules()
        print "All databases loaded successfully"
    }
}
