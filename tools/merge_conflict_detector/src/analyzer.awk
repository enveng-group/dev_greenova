#!/usr/bin/awk -f
#
# analyzer.awk - AWK script for detailed conflict analysis
#
# POSIX AWK implementation for data processing and pattern matching
# Data-driven approach to Git repository analysis

BEGIN {
    # Load database integration module
    if (DATA_MANAGER_PATH == "") {
        DATA_MANAGER_PATH = "src/data_manager.awk"
    }

    # Initialize data structures
    total_files = 0
    total_hunks = 0
    total_additions = 0
    total_deletions = 0
    conflict_score = 0

    # Load patterns from database
    load_database_patterns()

    # Initialize file type weights (fallback values)
    type_weights["c"] = 1.5
    type_weights["h"] = 1.5
    type_weights["cpp"] = 1.5
    type_weights["cxx"] = 1.5
    type_weights["java"] = 1.3
    type_weights["py"] = 1.2
    type_weights["js"] = 1.2
    type_weights["ts"] = 1.2
    type_weights["sh"] = 1.1
    type_weights["mk"] = 2.0
    type_weights["makefile"] = 2.0
    type_weights["cmake"] = 1.8
    type_weights["xml"] = 1.1
    type_weights["json"] = 1.0
    type_weights["yaml"] = 1.0
    type_weights["yml"] = 1.0
    type_weights["md"] = 0.5
    type_weights["txt"] = 0.3

    # Risk patterns that increase conflict probability
    risk_patterns["ifdef"] = 1.3
    risk_patterns["ifndef"] = 1.3
    risk_patterns["#if"] = 1.3
    risk_patterns["TODO"] = 1.1
    risk_patterns["FIXME"] = 1.2
    risk_patterns["XXX"] = 1.2
    risk_patterns["main("] = 1.5
    risk_patterns["int main"] = 1.5
    risk_patterns["class "] = 1.3
    risk_patterns["function "] = 1.2
    risk_patterns["def "] = 1.2
    risk_patterns["import "] = 1.1
    risk_patterns["include "] = 1.4

    # Field separator for numstat format (tab-separated)
    FS = "\t"
}

# Load conflict patterns from database
function load_database_patterns(    cmd, line, fields, n) {
    # For now, just return without loading - use the fallback patterns
    # cmd = "awk -v OPERATION=load_patterns -f " DATA_MANAGER_PATH " /dev/null"
    # Comment out database loading temporarily to avoid syntax errors
    return
}

# Process Git diff --numstat output
# Format: additions	deletions	filename
/^[0-9]+\s+[0-9]+\s+/ {
    additions = $1
    deletions = $2
    filename = $3

    # Handle case where filename contains spaces - take everything after second field
    if (NF > 3) {
        filename = ""
        for (i = 3; i <= NF; i++) {
            filename = filename (i > 3 ? " " : "") $i
        }
    }

    # Extract file extension
    extension = ""
    if (match(filename, /\.([^.\/]+)$/, ext_match)) {
        extension = tolower(ext_match[1])
    }

    # Calculate base conflict score for this file
    file_score = calculate_file_score(additions, deletions, filename, extension)

    # Store file data
    files[total_files] = filename
    file_additions[total_files] = additions
    file_deletions[total_files] = deletions
    file_scores[total_files] = file_score
    file_extensions[total_files] = extension

    total_files++
    total_additions += additions
    total_deletions += deletions
    conflict_score += file_score
}

# Process Git diff output for detailed analysis
/^diff --git/ {
    current_file = ""
    if (match($0, /b\/(.+)$/, file_match)) {
        current_file = file_match[1]
    }
    current_hunks = 0
}

# Count diff hunks
/^@@/ {
    current_hunks++
    total_hunks++

    # Extract line numbers for proximity analysis
    if (match($0, /@@ -([0-9]+),?([0-9]*) \+([0-9]+),?([0-9]*) @@/, hunk_match)) {
        old_start = hunk_match[1]
        old_count = (hunk_match[2] ? hunk_match[2] : 1)
        new_start = hunk_match[3]
        new_count = (hunk_match[4] ? hunk_match[4] : 1)

        # Analyze hunk proximity for increased conflict risk
        if (current_file in hunk_data_end) {
            previous_end = hunk_data_end[current_file]
            if (old_start - previous_end < 10) {
                # Close proximity increases conflict risk
                proximity_factor = 1.3
                if (current_file in file_proximity) {
                    file_proximity[current_file] *= proximity_factor
                } else {
                    file_proximity[current_file] = proximity_factor
                }
            }
        }

        hunk_data_start[current_file] = old_start
        hunk_data_end[current_file] = old_start + old_count
    }
}

# Analyze code content for risk patterns
/^[+-]/ && current_file != "" {
    line_content = substr($0, 2)  # Remove +/- prefix

    # Check for high-risk patterns
    for (pattern in risk_patterns) {
        if (index(tolower(line_content), pattern) > 0) {
            if (current_file in pattern_risks) {
                pattern_risks[current_file] += risk_patterns[pattern]
            } else {
                pattern_risks[current_file] = risk_patterns[pattern]
            }
        }
    }

    # Analyze line complexity
    complexity = calculate_line_complexity(line_content)
    if (current_file in line_complexities) {
        line_complexities[current_file] += complexity
    } else {
        line_complexities[current_file] = complexity
    }
}

# Calculate conflict score for a single file
function calculate_file_score(additions, deletions, filename, extension) {
    local_score = 0
    change_volume = additions + deletions

    # Base score from change volume
    if (change_volume > 100) {
        local_score = 0.8
    } else if (change_volume > 50) {
        local_score = 0.6
    } else if (change_volume > 20) {
        local_score = 0.4
    } else if (change_volume > 5) {
        local_score = 0.2
    } else {
        local_score = 0.1
    }

    # Apply file type weight
    if (extension in type_weights) {
        local_score *= type_weights[extension]
    }

    # Special handling for critical files
    filename_lower = tolower(filename)
    if (match(filename_lower, /(makefile|cmake|configure|setup)/) ||
        match(filename_lower, /\.(mk|am|in)$/)) {
        local_score *= 2.0
    }

    # Cap the score
    return (local_score > 1.0 ? 1.0 : local_score)
}

# Calculate line complexity based on syntax elements
function calculate_line_complexity(line) {
    complexity = 0

    # Count syntax elements that increase complexity
    complexity += gsub(/[{}()[\]]/, "", line) * 0.1
    complexity += gsub(/[;&|]/, "", line) * 0.2
    complexity += gsub(/if|else|for|while|switch|case/, "", line) * 0.3
    complexity += gsub(/#ifdef|#ifndef|#if|#else|#elif/, "", line) * 0.4

    return complexity
}

# Generate intelligent recommendations based on analysis
function generate_recommendations() {
    recommendations = ""

    # Overall risk assessment
    avg_score = (total_files > 0 ? conflict_score / total_files : 0)

    if (avg_score > 0.7) {
        recommendations = recommendations "HIGH RISK: Consider splitting this merge into smaller parts. "
    } else if (avg_score > 0.4) {
        recommendations = recommendations "MEDIUM RISK: Review changes carefully before merging. "
    } else {
        recommendations = recommendations "LOW RISK: Standard merge procedures should be sufficient. "
    }

    # Volume-based recommendations
    if (total_additions + total_deletions > 1000) {
        recommendations = recommendations "Large changeset detected - run comprehensive tests. "
    }

    if (total_files > 20) {
        recommendations = recommendations "Many files affected - consider incremental integration. "
    }

    # File-specific recommendations
    critical_files = 0
    for (i = 0; i < total_files; i++) {
        if (file_scores[i] > 0.8) {
            critical_files++
        }
    }

    if (critical_files > 0) {
        recommendations = recommendations sprintf("Monitor %d high-risk files closely. ", critical_files)
    }

    # Hunk density recommendations
    if (total_files > 0 && total_hunks / total_files > 3) {
        recommendations = recommendations "High change density - consider interactive rebase. "
    }

    return recommendations
}

# Output results in specified format
END {
    recommendations = generate_recommendations()
    overall_probability = (total_files > 0 ? conflict_score / total_files : 0)

    if (output_format == "json") {
        print "{"
        print "  \"summary\": {"
        printf "    \"totalFiles\": %d,\n", total_files
        printf "    \"totalHunks\": %d,\n", total_hunks
        printf "    \"totalAdditions\": %d,\n", total_additions
        printf "    \"totalDeletions\": %d,\n", total_deletions
        printf "    \"overallProbability\": %.3f,\n", overall_probability
        printf "    \"riskLevel\": \"%s\",\n", (overall_probability > 0.7 ? "HIGH" : overall_probability > 0.4 ? "MEDIUM" : "LOW")
        printf "    \"recommendations\": \"%s\"\n", recommendations
        print "  },"
        print "  \"files\": ["

        for (i = 0; i < total_files; i++) {
            print "    {"
            printf "      \"path\": \"%s\",\n", files[i]
            printf "      \"additions\": %d,\n", file_additions[i]
            printf "      \"deletions\": %d,\n", file_deletions[i]
            printf "      \"conflictScore\": %.3f,\n", file_scores[i]
            printf "      \"extension\": \"%s\",\n", file_extensions[i]
            printf "      \"proximityFactor\": %.3f,\n", (files[i] in file_proximity ? file_proximity[files[i]] : 1.0)
            printf "      \"patternRisk\": %.3f,\n", (files[i] in pattern_risks ? pattern_risks[files[i]] : 1.0)
            printf "      \"complexity\": %.3f\n", (files[i] in line_complexities ? line_complexities[files[i]] : 0.0)
            printf "    }%s\n", (i < total_files - 1 ? "," : "")
        }

        print "  ]"
        print "}"

    } else if (output_format == "csv") {
        print "file,additions,deletions,conflict_score,extension,proximity_factor,pattern_risk,complexity"
        for (i = 0; i < total_files; i++) {
            printf "%s,%d,%d,%.3f,%s,%.3f,%.3f,%.3f\n",
                   files[i], file_additions[i], file_deletions[i], file_scores[i], file_extensions[i],
                   (files[i] in file_proximity ? file_proximity[files[i]] : 1.0),
                   (files[i] in pattern_risks ? pattern_risks[files[i]] : 1.0),
                   (files[i] in line_complexities ? line_complexities[files[i]] : 0.0)
        }

    } else {
        # Default text output
        print "=== Merge Conflict Analysis ==="
        printf "Files analyzed: %d\n", total_files
        printf "Total hunks: %d\n", total_hunks
        printf "Lines added: %d\n", total_additions
        printf "Lines deleted: %d\n", total_deletions
        printf "Overall conflict probability: %.1f%%\n", overall_probability * 100
        printf "Risk level: %s\n", (overall_probability > 0.7 ? "HIGH" : overall_probability > 0.4 ? "MEDIUM" : "LOW")
        print ""

        if (total_files > 0) {
            print "File Analysis:"
            print "=============="
            for (i = 0; i < total_files; i++) {
                printf "%-40s %3d/%-3d lines  Risk: %5.1f%%", files[i], file_additions[i], file_deletions[i], file_scores[i] * 100

                # Add risk factors if present
                risk_factors = ""
                if (files[i] in file_proximity && file_proximity[files[i]] > 1.0) {
                    risk_factors = risk_factors " [PROXIMITY]"
                }
                if (files[i] in pattern_risks && pattern_risks[files[i]] > 1.0) {
                    risk_factors = risk_factors " [PATTERNS]"
                }
                if (files[i] in line_complexities && line_complexities[files[i]] > 1.0) {
                    risk_factors = risk_factors " [COMPLEX]"
                }

                printf "%s\n", risk_factors
            }
            print ""
        }

        print "Recommendations:"
        print "================"
        print recommendations
    }
}
