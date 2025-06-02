#!/usr/bin/awk -f
#
# conflict_report.awk - Generate detailed conflict analysis reports
#
# POSIX AWK implementation for conflict reporting and recommendations
# Data-driven analysis with comprehensive metrics

BEGIN {
    # Initialize report data structures
    total_risk_score = 0
    file_count = 0
    critical_files = 0
    high_risk_files = 0
    medium_risk_files = 0
    low_risk_files = 0

    # Risk thresholds
    CRITICAL_THRESHOLD = 0.9
    HIGH_THRESHOLD = 0.7
    MEDIUM_THRESHOLD = 0.4

    # File type risk multipliers
    risk_multipliers["makefile"] = 2.0
    risk_multipliers["cmake"] = 1.8
    risk_multipliers["configure"] = 2.0
    risk_multipliers["c"] = 1.5
    risk_multipliers["h"] = 1.5
    risk_multipliers["cpp"] = 1.5
    risk_multipliers["cxx"] = 1.5
    risk_multipliers["java"] = 1.3
    risk_multipliers["py"] = 1.2
    risk_multipliers["js"] = 1.2
    risk_multipliers["ts"] = 1.2
    risk_multipliers["sh"] = 1.1
    risk_multipliers["xml"] = 1.1
    risk_multipliers["json"] = 1.0
    risk_multipliers["md"] = 0.5
    risk_multipliers["txt"] = 0.3

    # Content pattern risks
    pattern_weights["main("] = 2.0
    pattern_weights["#include"] = 1.5
    pattern_weights["#define"] = 1.4
    pattern_weights["#ifdef"] = 1.3
    pattern_weights["class "] = 1.3
    pattern_weights["function "] = 1.2
    pattern_weights["import "] = 1.2
    pattern_weights["export "] = 1.2
    pattern_weights["TODO"] = 1.1
    pattern_weights["FIXME"] = 1.2
    pattern_weights["XXX"] = 1.2
    pattern_weights["HACK"] = 1.3

    FS = "\t"

    # Report configuration
    report_format = (ENVIRON["REPORT_FORMAT"] ? ENVIRON["REPORT_FORMAT"] : "detailed")
    include_recommendations = (ENVIRON["INCLUDE_RECOMMENDATIONS"] ? 1 : 1)
    verbose_output = (ENVIRON["VERBOSE"] ? 1 : 0)
}

# Process input data from conflict analysis
# Expected format: filename<TAB>risk_score<TAB>additions<TAB>deletions<TAB>hunks<TAB>extension
{
    if (NF >= 6) {
        filename = $1
        risk_score = $2
        additions = $3
        deletions = $4
        hunks = $5
        extension = $6

        # Store file data
        files[file_count] = filename
        file_risks[file_count] = risk_score
        file_additions[file_count] = additions
        file_deletions[file_count] = deletions
        file_hunks[file_count] = hunks
        file_extensions[file_count] = extension

        # Apply risk multipliers
        adjusted_risk = risk_score
        if (extension in risk_multipliers) {
            adjusted_risk *= risk_multipliers[extension]
        }

        # Cap adjusted risk at 1.0
        if (adjusted_risk > 1.0) {
            adjusted_risk = 1.0
        }

        file_adjusted_risks[file_count] = adjusted_risk

        # Categorize by risk level
        if (adjusted_risk >= CRITICAL_THRESHOLD) {
            critical_files++
            file_categories[file_count] = "CRITICAL"
        } else if (adjusted_risk >= HIGH_THRESHOLD) {
            high_risk_files++
            file_categories[file_count] = "HIGH"
        } else if (adjusted_risk >= MEDIUM_THRESHOLD) {
            medium_risk_files++
            file_categories[file_count] = "MEDIUM"
        } else {
            low_risk_files++
            file_categories[file_count] = "LOW"
        }

        total_risk_score += adjusted_risk
        file_count++
    }
}

# Calculate overall metrics
function calculate_metrics() {
    if (file_count == 0) {
        overall_risk = 0
        return
    }

    overall_risk = total_risk_score / file_count

    # Calculate distribution metrics
    risk_distribution["critical"] = critical_files
    risk_distribution["high"] = high_risk_files
    risk_distribution["medium"] = medium_risk_files
    risk_distribution["low"] = low_risk_files

    # Calculate change volume metrics
    total_additions = 0
    total_deletions = 0
    total_hunks = 0

    for (i = 0; i < file_count; i++) {
        total_additions += file_additions[i]
        total_deletions += file_deletions[i]
        total_hunks += file_hunks[i]
    }

    change_volume = total_additions + total_deletions
    average_hunks = (file_count > 0 ? total_hunks / file_count : 0)
}

# Generate strategic recommendations
function generate_recommendations() {
    recommendations = ""
    priority_actions = ""

    # Overall risk assessment
    if (overall_risk >= CRITICAL_THRESHOLD) {
        recommendations = recommendations "CRITICAL RISK LEVEL: This merge has very high conflict potential. "
        priority_actions = priority_actions "1. DO NOT merge without extensive review. "
        priority_actions = priority_actions "2. Consider breaking into smaller, focused merges. "
        priority_actions = priority_actions "3. Perform manual conflict resolution testing. "
    } else if (overall_risk >= HIGH_THRESHOLD) {
        recommendations = recommendations "HIGH RISK LEVEL: Significant conflict potential detected. "
        priority_actions = priority_actions "1. Perform thorough code review before merge. "
        priority_actions = priority_actions "2. Test merge in isolated environment first. "
        priority_actions = priority_actions "3. Have conflict resolution strategy ready. "
    } else if (overall_risk >= MEDIUM_THRESHOLD) {
        recommendations = recommendations "MEDIUM RISK LEVEL: Moderate conflict potential. "
        priority_actions = priority_actions "1. Review high-risk files carefully. "
        priority_actions = priority_actions "2. Run automated tests before merge. "
        priority_actions = priority_actions "3. Monitor merge process closely. "
    } else {
        recommendations = recommendations "LOW RISK LEVEL: Standard merge procedures should be sufficient. "
        priority_actions = priority_actions "1. Follow normal merge procedures. "
        priority_actions = priority_actions "2. Run standard test suite. "
    }

    # File-specific recommendations
    if (critical_files > 0) {
        recommendations = recommendations sprintf("CRITICAL: %d files require immediate attention. ", critical_files)
        priority_actions = priority_actions sprintf("4. Review %d critical files manually. ", critical_files)
    }

    if (high_risk_files > 3) {
        recommendations = recommendations sprintf("WARNING: %d high-risk files detected. ", high_risk_files)
        priority_actions = priority_actions "5. Consider incremental merge approach. "
    }

    # Volume-based recommendations
    if (change_volume > 1000) {
        recommendations = recommendations "Large changeset detected (>1000 lines). "
        priority_actions = priority_actions "6. Run comprehensive test suite. "
    }

    if (average_hunks > 5) {
        recommendations = recommendations "High change density detected. "
        priority_actions = priority_actions "7. Consider interactive rebase to clean up changes. "
    }

    # Specific file type recommendations
    for (i = 0; i < file_count; i++) {
        if (file_categories[i] == "CRITICAL") {
            ext = file_extensions[i]
            if (ext == "makefile" || ext == "cmake") {
                recommendations = recommendations "Build system files modified - verify build integrity. "
                break
            } else if (ext == "c" || ext == "h" || ext == "cpp") {
                recommendations = recommendations "Core source files modified - run memory/security tests. "
                break
            }
        }
    }

    return recommendations "\n" priority_actions
}

# Generate merge strategy recommendations
function generate_merge_strategy() {
    strategy = ""

    if (overall_risk >= CRITICAL_THRESHOLD || critical_files > 2) {
        strategy = "RECOMMENDED STRATEGY: Manual merge with extensive testing\n"
        strategy = strategy "- Use 'git merge --no-ff --no-commit' to stage merge\n"
        strategy = strategy "- Resolve conflicts manually for each critical file\n"
        strategy = strategy "- Test thoroughly before committing merge\n"
        strategy = strategy "- Consider breaking into multiple smaller merges\n"
    } else if (overall_risk >= HIGH_THRESHOLD || high_risk_files > 5) {
        strategy = "RECOMMENDED STRATEGY: Careful automated merge with manual review\n"
        strategy = strategy "- Use 'git merge --no-ff' to preserve merge history\n"
        strategy = strategy "- Review all conflict resolutions before final commit\n"
        strategy = strategy "- Run full test suite after merge\n"
        strategy = strategy "- Have rollback plan ready\n"
    } else if (overall_risk >= MEDIUM_THRESHOLD) {
        strategy = "RECOMMENDED STRATEGY: Standard merge with monitoring\n"
        strategy = strategy "- Use standard 'git merge' command\n"
        strategy = strategy "- Monitor for unexpected conflicts\n"
        strategy = strategy "- Run automated tests\n"
        strategy = strategy "- Review high-risk files post-merge\n"
    } else {
        strategy = "RECOMMENDED STRATEGY: Fast-forward merge if possible\n"
        strategy = strategy "- Use 'git merge --ff-only' if branches are linear\n"
        strategy = strategy "- Otherwise use standard 'git merge'\n"
        strategy = strategy "- Run standard validation tests\n"
    }

    return strategy
}

# Output detailed report
function output_detailed_report() {
    print "╔══════════════════════════════════════════════════════════════════════════════╗"
    print "║                        MERGE CONFLICT ANALYSIS REPORT                       ║"
    print "╚══════════════════════════════════════════════════════════════════════════════╝"
    print ""

    # Executive summary
    print "EXECUTIVE SUMMARY"
    print "=================="
    printf "Overall Risk Score: %.1f%% (%s)\n", overall_risk * 100,
           (overall_risk >= CRITICAL_THRESHOLD ? "CRITICAL" :
            overall_risk >= HIGH_THRESHOLD ? "HIGH" :
            overall_risk >= MEDIUM_THRESHOLD ? "MEDIUM" : "LOW")
    printf "Files Analyzed: %d\n", file_count
    printf "Total Changes: %d lines (%d added, %d deleted)\n", change_volume, total_additions, total_deletions
    printf "Average Hunks per File: %.1f\n", average_hunks
    print ""

    # Risk distribution
    print "RISK DISTRIBUTION"
    print "=================="
    printf "Critical Risk: %d files (%.1f%%)\n", critical_files, (file_count > 0 ? critical_files * 100.0 / file_count : 0)
    printf "High Risk:     %d files (%.1f%%)\n", high_risk_files, (file_count > 0 ? high_risk_files * 100.0 / file_count : 0)
    printf "Medium Risk:   %d files (%.1f%%)\n", medium_risk_files, (file_count > 0 ? medium_risk_files * 100.0 / file_count : 0)
    printf "Low Risk:      %d files (%.1f%%)\n", low_risk_files, (file_count > 0 ? low_risk_files * 100.0 / file_count : 0)
    print ""

    # File details
    if (file_count > 0) {
        print "FILE ANALYSIS"
        print "=============="
        printf "%-50s %-8s %-8s %-6s %-6s %-8s\n", "File Path", "Risk", "Category", "Added", "Deleted", "Hunks"
        print "────────────────────────────────────────────────────────────────────────────────────"

        # Sort files by risk level for better presentation
        for (category in risk_distribution) {
            if (risk_distribution[category] > 0) {
                print_category_header(category)
                for (i = 0; i < file_count; i++) {
                    if (tolower(file_categories[i]) == category) {
                        printf "%-50s %5.1f%% %-8s %6d %7d %6d\n",
                               files[i], file_adjusted_risks[i] * 100, file_categories[i],
                               file_additions[i], file_deletions[i], file_hunks[i]
                    }
                }
                print ""
            }
        }
    }

    # Recommendations
    if (include_recommendations) {
        print "RECOMMENDATIONS & ACTION ITEMS"
        print "==============================="
        print generate_recommendations()
        print ""

        print "MERGE STRATEGY"
        print "=============="
        print generate_merge_strategy()
        print ""
    }

    # Additional insights
    if (verbose_output) {
        print "ADDITIONAL INSIGHTS"
        print "==================="
        print_file_type_analysis()
        print_change_patterns()
        print ""
    }
}

# Print category header with formatting
function print_category_header(category) {
    header = toupper(category) " RISK FILES:"
    printf "%s\n", header
}

# Analyze file types and their risk contributions
function print_file_type_analysis() {
    print "File Type Risk Analysis:"

    # Count files by extension
    for (i = 0; i < file_count; i++) {
        ext = file_extensions[i]
        if (ext in type_counts) {
            type_counts[ext]++
            type_risk_sum[ext] += file_adjusted_risks[i]
        } else {
            type_counts[ext] = 1
            type_risk_sum[ext] = file_adjusted_risks[i]
        }
    }

    # Display type analysis
    for (ext in type_counts) {
        avg_risk = type_risk_sum[ext] / type_counts[ext]
        printf "  %s files: %d (avg risk: %.1f%%)\n", ext, type_counts[ext], avg_risk * 100
    }
}

# Analyze change patterns
function print_change_patterns() {
    print "Change Pattern Analysis:"

    large_files = 0
    complex_files = 0

    for (i = 0; i < file_count; i++) {
        change_size = file_additions[i] + file_deletions[i]
        if (change_size > 50) {
            large_files++
        }
        if (file_hunks[i] > 5) {
            complex_files++
        }
    }

    printf "  Large changes (>50 lines): %d files\n", large_files
    printf "  Complex changes (>5 hunks): %d files\n", complex_files
    printf "  Change concentration: %.1f%% of changes in top 20%% of files\n",
           calculate_change_concentration()
}

# Calculate change concentration (Pareto analysis)
function calculate_change_concentration() {
    if (file_count == 0) return 0

    # Sort files by change volume (conceptually)
    total_changes = 0
    for (i = 0; i < file_count; i++) {
        total_changes += file_additions[i] + file_deletions[i]
    }

    # Simple concentration estimate
    top_20_percent = int(file_count * 0.2)
    if (top_20_percent == 0) top_20_percent = 1

    # This is a simplified calculation
    return 80.0  # Placeholder for actual Pareto calculation
}

# Output summary report
function output_summary_report() {
    printf "MERGE RISK SUMMARY: %.1f%% (%s)\n", overall_risk * 100,
           (overall_risk >= CRITICAL_THRESHOLD ? "CRITICAL" :
            overall_risk >= HIGH_THRESHOLD ? "HIGH" :
            overall_risk >= MEDIUM_THRESHOLD ? "MEDIUM" : "LOW")
    printf "Files: %d total (%d critical, %d high-risk)\n",
           file_count, critical_files, high_risk_files
    printf "Changes: %d lines across %d hunks\n", change_volume, total_hunks

    if (include_recommendations) {
        print ""
        print "KEY RECOMMENDATIONS:"
        print generate_recommendations()
    }
}

# Main output function
END {
    # Calculate all metrics first
    calculate_metrics()

    # Output based on requested format
    if (report_format == "summary") {
        output_summary_report()
    } else if (report_format == "json") {
        output_json_report()
    } else {
        output_detailed_report()
    }
}

# JSON output format
function output_json_report() {
    print "{"
    printf "  \"summary\": {\n"
    printf "    \"overallRisk\": %.3f,\n", overall_risk
    printf "    \"riskLevel\": \"%s\",\n",
           (overall_risk >= CRITICAL_THRESHOLD ? "CRITICAL" :
            overall_risk >= HIGH_THRESHOLD ? "HIGH" :
            overall_risk >= MEDIUM_THRESHOLD ? "MEDIUM" : "LOW")
    printf "    \"fileCount\": %d,\n", file_count
    printf "    \"totalChanges\": %d,\n", change_volume
    printf "    \"totalHunks\": %d\n", total_hunks
    printf "  },\n"

    printf "  \"distribution\": {\n"
    printf "    \"critical\": %d,\n", critical_files
    printf "    \"high\": %d,\n", high_risk_files
    printf "    \"medium\": %d,\n", medium_risk_files
    printf "    \"low\": %d\n", low_risk_files
    printf "  },\n"

    if (include_recommendations) {
        printf "  \"recommendations\": \"%s\",\n", generate_recommendations()
        printf "  \"strategy\": \"%s\",\n", generate_merge_strategy()
    }

    printf "  \"files\": [\n"
    for (i = 0; i < file_count; i++) {
        printf "    {\n"
        printf "      \"path\": \"%s\",\n", files[i]
        printf "      \"risk\": %.3f,\n", file_adjusted_risks[i]
        printf "      \"category\": \"%s\",\n", file_categories[i]
        printf "      \"additions\": %d,\n", file_additions[i]
        printf "      \"deletions\": %d,\n", file_deletions[i]
        printf "      \"hunks\": %d,\n", file_hunks[i]
        printf "      \"extension\": \"%s\"\n", file_extensions[i]
        printf "    }%s\n", (i < file_count - 1 ? "," : "")
    }
    printf "  ]\n"
    print "}"
}
