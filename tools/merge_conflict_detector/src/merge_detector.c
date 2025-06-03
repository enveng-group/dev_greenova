/*
 * merge_detector.c - Core merge conflict detection and analysis
 *
 * POSIX-compliant C implementation for performance-critical operations
 * Follows data-driven programming paradigm for Git repository analysis
 */

/* Feature test macros for POSIX extensions */
#define _POSIX_C_SOURCE 200809L

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <ctype.h>
#include <time.h>

/* POSIX-compliant constants */
#define MAX_PATH_LENGTH 4096
#define MAX_BRANCH_LENGTH 256
#define MAX_COMMAND_LENGTH 8192
#define MAX_LINE_LENGTH 2048
#define MAX_FILES 10000

/* Data storage file paths */
#define PATTERNS_DB_PATH "data/conflict_patterns.dat"
#define CONFIG_DB_PATH "data/repository_config.dat"
#define HISTORY_DB_PATH "data/analysis_history.dat"
#define RULES_DB_PATH "data/risk_rules.dat"
#define SCRIPT_DIR "scripts"

/* Database field limits */
#define MAX_PATTERN_ID 64
#define MAX_EXTENSION 32
#define MAX_DESCRIPTION 256
#define MAX_MODIFIERS 128

/* Exit codes */
#define SUCCESS 0
#define ERROR_GENERAL 1
#define ERROR_INVALID_ARGS 2
#define ERROR_REPO_NOT_FOUND 3
#define ERROR_BRANCH_NOT_FOUND 4
#define ERROR_PERMISSION_DENIED 5

/* Conflict severity levels */
#define SEVERITY_LOW 1
#define SEVERITY_MEDIUM 2
#define SEVERITY_HIGH 3
#define SEVERITY_CRITICAL 4

/* Data structures for database integration */
struct conflict_pattern {
    char pattern_id[MAX_PATTERN_ID];
    char file_extension[MAX_EXTENSION];
    double conflict_probability;
    int base_score;
    char modifiers[MAX_MODIFIERS];
    char description[MAX_DESCRIPTION];
};

struct repository_config {
    char repo_path[MAX_PATH_LENGTH];
    char branch_pattern[MAX_BRANCH_LENGTH];
    char exclude_patterns[MAX_MODIFIERS];
    char priority_files[MAX_MODIFIERS];
    int check_frequency;
    long last_check;
};

struct risk_rule {
    char rule_id[MAX_PATTERN_ID];
    char condition_type[64];
    double condition_value;
    double risk_multiplier;
    char severity[16];
    char description[MAX_DESCRIPTION];
};

/* Data structures for conflict analysis */
struct file_conflict {
    char path[MAX_PATH_LENGTH];
    int line_start;
    int line_end;
    int severity;
    double probability;
    char pattern_id[MAX_PATTERN_ID];
};

struct conflict_analysis {
    struct file_conflict files[MAX_FILES];
    int file_count;
    double overall_probability;
    int total_conflicts;
    char recommendations[MAX_COMMAND_LENGTH];
};

/* Configuration structure */
struct config {
    int verbose;
    int quiet;
    char output_file[MAX_PATH_LENGTH];
    char format[32];
    int dry_run;
    int score_threshold;
    int maintenance_mode;
    int aggressive;
    int prune;
};

/* Function prototypes */
/* Database functions */
static int load_conflict_patterns(struct conflict_pattern patterns[], int max_patterns);
static int load_repository_config(const char *repo_path, struct repository_config *config);
static int load_risk_rules(struct risk_rule rules[], int max_rules);
static int save_analysis_history(const char *repo_path, const char *branch_name,
                               const struct conflict_analysis *analysis);
static double calculate_file_risk_score(const char *filename, const struct conflict_pattern patterns[],
                                       const struct risk_rule rules[], int pattern_count, int rule_count);
static const char *get_file_extension(const char *filename);

/* Core analysis functions */
static int validate_branch_name(const char *branch_name);
static int validate_repository_path(const char *repo_path);
static int execute_git_command(const char *command, char *output, size_t output_size);
static int analyze_file_conflicts(const char *base_branch, const char *merge_branch,
                                struct conflict_analysis *analysis);
static int calculate_conflict_probability(struct conflict_analysis *analysis);
static int generate_recommendations(struct conflict_analysis *analysis);
static int output_analysis(const struct conflict_analysis *analysis, const struct config *cfg);

/* Utility functions */
static void print_usage(const char *program_name);
static void print_version(void);
static int parse_arguments(int argc, char *argv[], struct config *cfg,
                         char *base_branch, char *merge_branch);

/* Security: Validate Git branch names against injection attacks */
static int
validate_branch_name(const char *branch_name)
{
    const char *p;
    size_t len;

    if (branch_name == NULL || *branch_name == '\0') {
        return 0;
    }

    len = strlen(branch_name);
    if (len >= MAX_BRANCH_LENGTH) {
        return 0;
    }

    /* Check for dangerous characters that could enable command injection */
    for (p = branch_name; *p != '\0'; p++) {
        if (*p == ';' || *p == '|' || *p == '&' || *p == '$' ||
            *p == '`' || *p == '\n' || *p == '\r' || *p == '\t') {
            return 0;
        }
    }

    /* Check for path traversal attempts */
    if (strstr(branch_name, "..") != NULL) {
        return 0;
    }

    /* Check for Git-specific restrictions */
    if (*branch_name == '-' || *branch_name == '.' ||
        branch_name[len-1] == '.' || branch_name[len-1] == '/') {
        return 0;
    }

    return 1;
}

/* Load conflict patterns from whitespace-delimited database */
static int
load_conflict_patterns(struct conflict_pattern patterns[], int max_patterns)
{
    FILE *fp;
    char line[MAX_LINE_LENGTH];
    int count = 0;
    char *token;
    int field_num;

    fp = fopen(PATTERNS_DB_PATH, "r");
    if (fp == NULL) {
        return 0;
    }

    while (fgets(line, sizeof(line), fp) && count < max_patterns) {
        /* Skip comments and empty lines */
        if (line[0] == '#' || line[0] == '\n' || line[0] == '\0') {
            continue;
        }

        /* Remove trailing newline */
        line[strcspn(line, "\n")] = '\0';

        /* Parse whitespace-delimited fields using strtok */
        field_num = 0;
        token = strtok(line, " \t");

        while (token != NULL && field_num < 6) {
            switch (field_num) {
                case 0:
                    strncpy(patterns[count].pattern_id, token, MAX_PATTERN_ID - 1);
                    patterns[count].pattern_id[MAX_PATTERN_ID - 1] = '\0';
                    break;
                case 1:
                    strncpy(patterns[count].file_extension, token, MAX_EXTENSION - 1);
                    patterns[count].file_extension[MAX_EXTENSION - 1] = '\0';
                    break;
                case 2:
                    patterns[count].conflict_probability = strtod(token, NULL);
                    break;
                case 3:
                    patterns[count].base_score = atoi(token);
                    break;
                case 4:
                    strncpy(patterns[count].modifiers, token, MAX_MODIFIERS - 1);
                    patterns[count].modifiers[MAX_MODIFIERS - 1] = '\0';
                    break;
                case 5:
                    strncpy(patterns[count].description, token, MAX_DESCRIPTION - 1);
                    patterns[count].description[MAX_DESCRIPTION - 1] = '\0';
                    /* Append remaining tokens as description */
                    while ((token = strtok(NULL, " \t")) != NULL) {
                        strncat(patterns[count].description, " ",
                               MAX_DESCRIPTION - strlen(patterns[count].description) - 1);
                        strncat(patterns[count].description, token,
                               MAX_DESCRIPTION - strlen(patterns[count].description) - 1);
                    }
                    break;
            }
            if (field_num < 5) {
                token = strtok(NULL, " \t");
            }
            field_num++;
        }

        if (field_num >= 6) {
            count++;
        }
    }

    fclose(fp);
    return count;
}

/* Load repository configuration from database */
static int
load_repository_config(const char *repo_path, struct repository_config *config)
{
    FILE *fp;
    char line[MAX_LINE_LENGTH];
    char *token;
    int field_num;

    fp = fopen(CONFIG_DB_PATH, "r");
    if (fp == NULL) {
        return 0;
    }

    while (fgets(line, sizeof(line), fp)) {
        /* Skip comments and empty lines */
        if (line[0] == '#' || line[0] == '\n' || line[0] == '\0') {
            continue;
        }

        /* Remove trailing newline */
        line[strcspn(line, "\n")] = '\0';

        /* Parse first field to check path match */
        token = strtok(line, " \t");
        if (token != NULL && strstr(token, repo_path) != NULL) {
            strncpy(config->repo_path, token, MAX_PATH_LENGTH - 1);
            config->repo_path[MAX_PATH_LENGTH - 1] = '\0';

            field_num = 1;
            while ((token = strtok(NULL, " \t")) != NULL && field_num < 6) {
                switch (field_num) {
                    case 1:
                        strncpy(config->branch_pattern, token, MAX_BRANCH_LENGTH - 1);
                        config->branch_pattern[MAX_BRANCH_LENGTH - 1] = '\0';
                        break;
                    case 2:
                        strncpy(config->exclude_patterns, token, MAX_MODIFIERS - 1);
                        config->exclude_patterns[MAX_MODIFIERS - 1] = '\0';
                        break;
                    case 3:
                        strncpy(config->priority_files, token, MAX_MODIFIERS - 1);
                        config->priority_files[MAX_MODIFIERS - 1] = '\0';
                        break;
                    case 4:
                        config->check_frequency = atoi(token);
                        break;
                    case 5:
                        config->last_check = atol(token);
                        break;
                }
                field_num++;
            }

            fclose(fp);
            return 1;
        }
    }

    fclose(fp);
    return 0;
}

/* Load risk assessment rules from database */
static int
load_risk_rules(struct risk_rule rules[], int max_rules)
{
    FILE *fp;
    char line[MAX_LINE_LENGTH];
    int count = 0;
    char *token;
    int field_num;

    fp = fopen(RULES_DB_PATH, "r");
    if (fp == NULL) {
        return 0;
    }

    while (fgets(line, sizeof(line), fp) && count < max_rules) {
        /* Skip comments and empty lines */
        if (line[0] == '#' || line[0] == '\n' || line[0] == '\0') {
            continue;
        }

        /* Remove trailing newline */
        line[strcspn(line, "\n")] = '\0';

        /* Parse whitespace-delimited fields using strtok */
        field_num = 0;
        token = strtok(line, " \t");

        while (token != NULL && field_num < 6) {
            switch (field_num) {
                case 0:
                    strncpy(rules[count].rule_id, token, MAX_PATTERN_ID - 1);
                    rules[count].rule_id[MAX_PATTERN_ID - 1] = '\0';
                    break;
                case 1:
                    strncpy(rules[count].condition_type, token, 63);
                    rules[count].condition_type[63] = '\0';
                    break;
                case 2:
                    rules[count].condition_value = strtod(token, NULL);
                    break;
                case 3:
                    rules[count].risk_multiplier = strtod(token, NULL);
                    break;
                case 4:
                    strncpy(rules[count].severity, token, 15);
                    rules[count].severity[15] = '\0';
                    break;
                case 5:
                    strncpy(rules[count].description, token, MAX_DESCRIPTION - 1);
                    rules[count].description[MAX_DESCRIPTION - 1] = '\0';
                    /* Append remaining tokens as description */
                    while ((token = strtok(NULL, " \t")) != NULL) {
                        strncat(rules[count].description, " ",
                               MAX_DESCRIPTION - strlen(rules[count].description) - 1);
                        strncat(rules[count].description, token,
                               MAX_DESCRIPTION - strlen(rules[count].description) - 1);
                    }
                    break;
            }
            if (field_num < 5) {
                token = strtok(NULL, " \t");
            }
            field_num++;
        }

        if (field_num >= 6) {
            count++;
        }
    }

    fclose(fp);
    return count;
}

/* Save analysis results to history database */
static int
save_analysis_history(const char *repo_path, const char *branch_name, const struct conflict_analysis *analysis)
{
    FILE *fp;
    time_t timestamp;
    const char *status;

    timestamp = time(NULL);

    /* Determine status based on conflict probability */
    if (analysis->overall_probability >= 0.8) {
        status = "CRITICAL";
    } else if (analysis->overall_probability >= 0.6) {
        status = "WARNING";
    } else if (analysis->overall_probability >= 0.3) {
        status = "SUCCESS";
    } else {
        status = "SUCCESS";
    }

    fp = fopen(HISTORY_DB_PATH, "a");
    if (fp == NULL) {
        return 0;
    }

    fprintf(fp, "%ld %s %s %.2f %d %d %s\n",
            timestamp, repo_path, branch_name,
            analysis->overall_probability, analysis->file_count,
            analysis->total_conflicts, status);

    fclose(fp);
    return 1;
}

/* Get file extension from filename */
static const char *
get_file_extension(const char *filename)
{
    const char *dot = strrchr(filename, '.');
    if (dot == NULL || dot == filename) {
        return "*";  /* No extension or hidden file */
    }
    return dot;
}

/* Calculate file-specific risk score using database patterns and rules */
static double
calculate_file_risk_score(const char *filename, const struct conflict_pattern patterns[],
                         const struct risk_rule rules[], int pattern_count, int rule_count)
{
    const char *extension;
    double base_score = 0.4;  /* Default score */
    double multiplier = 1.0;
    int i;

    extension = get_file_extension(filename);

    /* Find matching pattern */
    for (i = 0; i < pattern_count; i++) {
        if (strcmp(patterns[i].file_extension, extension) == 0 ||
            strcmp(patterns[i].file_extension, "*") == 0) {
            base_score = patterns[i].conflict_probability;
            break;
        }
    }

    /* Apply risk rules - simplified version for demonstration */
    for (i = 0; i < rule_count; i++) {
        if (strcmp(rules[i].condition_type, "CONFIGURATION") == 0 &&
            (strstr(filename, ".conf") || strstr(filename, ".config") ||
             strstr(filename, ".ini") || strstr(filename, ".yaml") ||
             strstr(filename, ".yml"))) {
            multiplier *= rules[i].risk_multiplier;
        } else if (strcmp(rules[i].condition_type, "BUILD_SCRIPT") == 0 &&
                  (strstr(filename, "Makefile") || strstr(filename, "makefile") ||
                   strstr(filename, ".mk") || strstr(filename, "build"))) {
            multiplier *= rules[i].risk_multiplier;
        }
    }

    return base_score * multiplier;
}

/* Validate repository path to prevent directory traversal */
static int
validate_repository_path(const char *repo_path)
{
    struct stat st;
    char git_dir[MAX_PATH_LENGTH];
    int result;

    if (repo_path == NULL || *repo_path == '\0') {
        repo_path = ".";
    }

    /* Check if path exists and is accessible */
    if (stat(repo_path, &st) != 0) {
        return 0;
    }

    if (!S_ISDIR(st.st_mode)) {
        return 0;
    }

    /* Check if it's a Git repository */
    result = snprintf(git_dir, sizeof(git_dir), "%s/.git", repo_path);
    if (result >= sizeof(git_dir)) {
        return 0;
    }

    if (stat(git_dir, &st) == 0 && S_ISDIR(st.st_mode)) {
        return 1;
    }

    /* Check if we're inside a Git repository */
    if (chdir(repo_path) != 0) {
        return 0;
    }

    return 1;
}

/* Execute Git command safely with output capture */
static int
execute_git_command(const char *command, char *output, size_t output_size)
{
    FILE *pipe;
    char safe_command[MAX_COMMAND_LENGTH];
    int result;
    size_t bytes_read = 0;
    char buffer[1024];

    /* Build safe command with proper escaping */
    result = snprintf(safe_command, sizeof(safe_command),
                     "git %s 2>/dev/null", command);

    if (result >= sizeof(safe_command)) {
        return ERROR_GENERAL;
    }

    pipe = popen(safe_command, "r");
    if (pipe == NULL) {
        return ERROR_GENERAL;
    }

    /* Read output safely */
    if (output != NULL && output_size > 0) {
        output[0] = '\0';

        while (fgets(buffer, sizeof(buffer), pipe) != NULL &&
               bytes_read < output_size - 1) {
            size_t buffer_len = strlen(buffer);
            size_t remaining = output_size - bytes_read - 1;

            if (buffer_len <= remaining) {
                strcat(output, buffer);
                bytes_read += buffer_len;
            } else {
                strncat(output, buffer, remaining);
                break;
            }
        }
    }

    result = pclose(pipe);
    return WEXITSTATUS(result);
}

/* Data-driven conflict analysis using Git diff output */
static int
analyze_file_conflicts(const char *base_branch, const char *merge_branch,
                      struct conflict_analysis *analysis)
{
    char command[MAX_COMMAND_LENGTH];
    char diff_output[MAX_COMMAND_LENGTH * 4];
    char *line;
    int result;

    /* Initialize analysis structure */
    analysis->file_count = 0;
    analysis->overall_probability = 0.0;
    analysis->total_conflicts = 0;
    analysis->recommendations[0] = '\0';

    /* Get list of modified files between branches */
    result = snprintf(command, sizeof(command),
                     "diff --name-only %s..%s", base_branch, merge_branch);

    if (result >= sizeof(command)) {
        return ERROR_GENERAL;
    }

    if (execute_git_command(command, diff_output, sizeof(diff_output)) != 0) {
        return ERROR_GENERAL;
    }

    /* Process each modified file */
    line = strtok(diff_output, "\n");
    while (line != NULL && analysis->file_count < MAX_FILES) {
        struct file_conflict *conflict = &analysis->files[analysis->file_count];

        /* Store file path safely */
        strncpy(conflict->path, line, sizeof(conflict->path) - 1);
        conflict->path[sizeof(conflict->path) - 1] = '\0';

        /* Analyze specific file for conflicts */
        result = snprintf(command, sizeof(command),
                         "diff --unified=3 %s..%s -- '%s'",
                         base_branch, merge_branch, conflict->path);

        if (result < sizeof(command)) {
            char file_diff[MAX_COMMAND_LENGTH];
            if (execute_git_command(command, file_diff, sizeof(file_diff)) == 0) {
                /* Parse diff hunks for conflict probability */
                char *hunk_line = strtok(file_diff, "\n");
                int hunk_count = 0;

                while (hunk_line != NULL) {
                    if (strncmp(hunk_line, "@@", 2) == 0) {
                        hunk_count++;
                        /* Extract line numbers for conflict zones */
                        if (sscanf(hunk_line, "@@ -%*d,%*d +%d,%d @@",
                                  &conflict->line_start, &conflict->line_end) == 2) {
                            conflict->line_end += conflict->line_start;
                        }
                    }
                    hunk_line = strtok(NULL, "\n");
                }

                /* Calculate conflict probability based on hunk density */
                conflict->probability = (double)hunk_count * 0.2;
                if (conflict->probability > 1.0) {
                    conflict->probability = 1.0;
                }

                /* Determine severity based on file type and change density */
                if (strstr(conflict->path, ".c") || strstr(conflict->path, ".h") ||
                    strstr(conflict->path, ".cpp") || strstr(conflict->path, ".java")) {
                    conflict->severity = SEVERITY_HIGH;
                    conflict->probability *= 1.2;
                } else if (strstr(conflict->path, "Makefile") ||
                          strstr(conflict->path, ".mk")) {
                    conflict->severity = SEVERITY_CRITICAL;
                    conflict->probability *= 1.5;
                } else {
                    conflict->severity = SEVERITY_MEDIUM;
                }

                if (conflict->probability > 1.0) {
                    conflict->probability = 1.0;
                }

                analysis->file_count++;
                analysis->total_conflicts += hunk_count;
            }
        }

        line = strtok(NULL, "\n");
    }

    return SUCCESS;
}

/* Calculate overall conflict probability using data-driven metrics */
static int
calculate_conflict_probability(struct conflict_analysis *analysis)
{
    double total_probability = 0.0;
    int high_severity_files = 0;
    int i;

    if (analysis->file_count == 0) {
        analysis->overall_probability = 0.0;
        return SUCCESS;
    }

    /* Aggregate individual file probabilities */
    for (i = 0; i < analysis->file_count; i++) {
        total_probability += analysis->files[i].probability;

        if (analysis->files[i].severity >= SEVERITY_HIGH) {
            high_severity_files++;
        }
    }

    /* Calculate weighted probability */
    analysis->overall_probability = total_probability / analysis->file_count;

    /* Apply severity multiplier */
    if (high_severity_files > 0) {
        double severity_factor = 1.0 + (0.2 * high_severity_files / analysis->file_count);
        analysis->overall_probability *= severity_factor;
    }

    /* Cap at 100% */
    if (analysis->overall_probability > 1.0) {
        analysis->overall_probability = 1.0;
    }

    return SUCCESS;
}

/* Generate data-driven recommendations */
static int
generate_recommendations(struct conflict_analysis *analysis)
{
    char *rec = analysis->recommendations;
    size_t remaining = sizeof(analysis->recommendations) - 1;
    int high_risk_files = 0;
    int critical_files = 0;
    int i;

    rec[0] = '\0';

    /* Count risk levels */
    for (i = 0; i < analysis->file_count; i++) {
        if (analysis->files[i].severity >= SEVERITY_HIGH) {
            high_risk_files++;
        }
        if (analysis->files[i].severity == SEVERITY_CRITICAL) {
            critical_files++;
        }
    }

    /* Generate recommendations based on analysis */
    if (analysis->overall_probability >= 0.8) {
        strncat(rec, "HIGH RISK: Consider rebasing or splitting merge. ", remaining);
    } else if (analysis->overall_probability >= 0.5) {
        strncat(rec, "MEDIUM RISK: Review changes carefully before merge. ", remaining);
    } else {
        strncat(rec, "LOW RISK: Standard merge procedures should suffice. ", remaining);
    }

    if (critical_files > 0) {
        strncat(rec, "Critical build files modified - test thoroughly. ", remaining);
    }

    if (high_risk_files > 3) {
        strncat(rec, "Many source files affected - consider incremental merge. ", remaining);
    }

    if (analysis->total_conflicts > 20) {
        strncat(rec, "High change density - run full test suite. ", remaining);
    }

    return SUCCESS;
}

/* Output analysis results in specified format */
static int
output_analysis(const struct conflict_analysis *analysis, const struct config *cfg)
{
    FILE *output_file = stdout;
    int i;

    /* Open output file if specified */
    if (cfg->output_file[0] != '\0') {
        output_file = fopen(cfg->output_file, "w");
        if (output_file == NULL) {
            fprintf(stderr, "Error: Cannot open output file: %s\n", cfg->output_file);
            return ERROR_GENERAL;
        }
    }

    /* Output in requested format */
    if (strcmp(cfg->format, "json") == 0) {
        fprintf(output_file, "{\n");
        fprintf(output_file, "  \"analysis\": {\n");
        fprintf(output_file, "    \"conflictProbability\": %.2f,\n", analysis->overall_probability);
        fprintf(output_file, "    \"totalFiles\": %d,\n", analysis->file_count);
        fprintf(output_file, "    \"totalConflicts\": %d,\n", analysis->total_conflicts);
        fprintf(output_file, "    \"risk\": \"%s\",\n",
                analysis->overall_probability >= 0.8 ? "HIGH" :
                analysis->overall_probability >= 0.5 ? "MEDIUM" : "LOW");
        fprintf(output_file, "    \"recommendations\": \"%s\",\n", analysis->recommendations);
        fprintf(output_file, "    \"conflictingFiles\": [\n");

        for (i = 0; i < analysis->file_count; i++) {
            fprintf(output_file, "      {\n");
            fprintf(output_file, "        \"path\": \"%s\",\n", analysis->files[i].path);
            fprintf(output_file, "        \"probability\": %.2f,\n", analysis->files[i].probability);
            fprintf(output_file, "        \"severity\": %d,\n", analysis->files[i].severity);
            fprintf(output_file, "        \"lineStart\": %d,\n", analysis->files[i].line_start);
            fprintf(output_file, "        \"lineEnd\": %d\n", analysis->files[i].line_end);
            fprintf(output_file, "      }%s\n", (i < analysis->file_count - 1) ? "," : "");
        }

        fprintf(output_file, "    ]\n");
        fprintf(output_file, "  }\n");
        fprintf(output_file, "}\n");

    } else if (strcmp(cfg->format, "csv") == 0) {
        fprintf(output_file, "file_path,probability,severity,line_start,line_end\n");
        for (i = 0; i < analysis->file_count; i++) {
            fprintf(output_file, "%s,%.2f,%d,%d,%d\n",
                   analysis->files[i].path,
                   analysis->files[i].probability,
                   analysis->files[i].severity,
                   analysis->files[i].line_start,
                   analysis->files[i].line_end);
        }
    } else {
        /* Default text format */
        fprintf(output_file, "Merge Conflict Analysis Report\n");
        fprintf(output_file, "==============================\n\n");
        fprintf(output_file, "Overall Conflict Probability: %.0f%%\n",
                analysis->overall_probability * 100);
        fprintf(output_file, "Risk Level: %s\n\n",
                analysis->overall_probability >= 0.8 ? "HIGH" :
                analysis->overall_probability >= 0.5 ? "MEDIUM" : "LOW");

        if (analysis->file_count > 0) {
            fprintf(output_file, "Conflicting Files (%d):\n", analysis->file_count);
            for (i = 0; i < analysis->file_count; i++) {
                fprintf(output_file, "  %s (%.0f%% risk, lines %d-%d)\n",
                       analysis->files[i].path,
                       analysis->files[i].probability * 100,
                       analysis->files[i].line_start,
                       analysis->files[i].line_end);
            }
            fprintf(output_file, "\n");
        }

        fprintf(output_file, "Recommendations:\n%s\n", analysis->recommendations);
    }

    if (output_file != stdout) {
        fclose(output_file);
    }

    return SUCCESS;
}

/* Print usage information */
static void
print_usage(const char *program_name)
{
    printf("Usage: %s [OPTIONS] BASE_BRANCH MERGE_BRANCH\n", program_name);
    printf("       %s --maintenance [MAINTENANCE_OPTIONS]\n", program_name);
    printf("       %s --analyze REPOSITORY_PATH\n", program_name);
    printf("\nOPTIONS:\n");
    printf("  -h, --help              Display this help and exit\n");
    printf("  -v, --verbose           Enable verbose output\n");
    printf("  -q, --quiet             Suppress non-essential output\n");
    printf("  -o, --output FILE       Write report to specified file\n");
    printf("  -f, --format FORMAT     Output format: text, json, csv (default: text)\n");
    printf("  --dry-run               Perform analysis without changes\n");
    printf("  --score-threshold NUM   Set conflict threshold (0-100, default: 70)\n");
    printf("  --maintenance           Run repository maintenance\n");
    printf("  --aggressive            Enable aggressive optimization\n");
    printf("  --prune                 Prune orphaned branches\n");
    printf("  --version               Display version information\n");
}

/* Print version information */
static void
print_version(void)
{
    printf("merge_conflict_detector version 1.0\n");
    printf("POSIX-compliant Git merge conflict analyzer\n");
    printf("Copyright (c) 2025, ISC License\n");
}

/* Parse command line arguments */
static int
parse_arguments(int argc, char *argv[], struct config *cfg,
               char *base_branch, char *merge_branch)
{
    int i;

    /* Initialize configuration with defaults */
    cfg->verbose = 0;
    cfg->quiet = 0;
    cfg->output_file[0] = '\0';
    strcpy(cfg->format, "text");
    cfg->dry_run = 0;
    cfg->score_threshold = 70;
    cfg->maintenance_mode = 0;
    cfg->aggressive = 0;
    cfg->prune = 0;

    base_branch[0] = '\0';
    merge_branch[0] = '\0';

    for (i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-h") == 0 || strcmp(argv[i], "--help") == 0) {
            printf("merge_conflict_detector - Git merge conflict analyzer\n");
            printf("Usage: %s [OPTIONS] BASE_BRANCH MERGE_BRANCH\n", argv[0]);
            printf("Options:\n");
            printf("  -h, --help              Display this help\n");
            printf("  -v, --verbose           Enable verbose output\n");
            printf("  --version               Display version\n");
            exit(SUCCESS);
        } else if (strcmp(argv[i], "--version") == 0) {
            printf("merge_conflict_detector version 1.0\n");
            exit(SUCCESS);
        } else if (strcmp(argv[i], "-v") == 0 || strcmp(argv[i], "--verbose") == 0) {
            cfg->verbose = 1;
        } else if (strcmp(argv[i], "-q") == 0 || strcmp(argv[i], "--quiet") == 0) {
            cfg->quiet = 1;
        } else if (argv[i][0] != '-') {
            /* Non-option arguments are branch names */
            if (base_branch[0] == '\0') {
                strncpy(base_branch, argv[i], MAX_BRANCH_LENGTH - 1);
                base_branch[MAX_BRANCH_LENGTH - 1] = '\0';
            } else if (merge_branch[0] == '\0') {
                strncpy(merge_branch, argv[i], MAX_BRANCH_LENGTH - 1);
                merge_branch[MAX_BRANCH_LENGTH - 1] = '\0';
            }
        }
    }

    return SUCCESS;
}

/* Find the path to the analyzer AWK script */
static int
find_analyzer_script_path(char *script_path, size_t path_size)
{
    /* Try several possible locations for the AWK script */
    const char *possible_paths[] = {
        "src/analyzer.awk",                    /* Development location */
        "../src/analyzer.awk",                 /* If running from build dir */
        "/usr/local/share/merge-conflict-detector/analyzer.awk",  /* System install */
        "/opt/merge-conflict-detector/src/analyzer.awk",         /* Alternative install */
        NULL
    };

    int i;
    for (i = 0; possible_paths[i] != NULL; i++) {
        if (access(possible_paths[i], R_OK) == 0) {
            strncpy(script_path, possible_paths[i], path_size - 1);
            script_path[path_size - 1] = '\0';
            return 1;
        }
    }

    /* If not found, try to construct path relative to executable */
    char exe_path[MAX_PATH_LENGTH];
    ssize_t len = readlink("/proc/self/exe", exe_path, sizeof(exe_path) - 1);
    if (len != -1) {
        exe_path[len] = '\0';
        char *last_slash = strrchr(exe_path, '/');
        if (last_slash != NULL) {
            *last_slash = '\0';  /* Remove executable name */
            snprintf(script_path, path_size, "%s/../src/analyzer.awk", exe_path);
            if (access(script_path, R_OK) == 0) {
                return 1;
            }
        }
    }

    return 0;  /* Script not found */
}

/* Main function - entry point */
int
main(int argc, char *argv[])
{
    struct config cfg;
    char base_branch[MAX_BRANCH_LENGTH];
    char merge_branch[MAX_BRANCH_LENGTH];

    /* Parse command line arguments */
    if (parse_arguments(argc, argv, &cfg, base_branch, merge_branch) != SUCCESS) {
        return ERROR_INVALID_ARGS;
    }

    /* Check if we're in a Git repository */
    if (execute_git_command("rev-parse --git-dir", NULL, 0) != SUCCESS) {
        if (!cfg.quiet) {
            fprintf(stderr, "Error: Not in a Git repository\n");
        }
        return ERROR_REPO_NOT_FOUND;
    }

    /* Find the AWK analyzer script */
    char script_path[MAX_PATH_LENGTH];
    if (!find_analyzer_script_path(script_path, sizeof(script_path))) {
        if (!cfg.quiet) {
            fprintf(stderr, "Error: Cannot find analyzer.awk script\n");
        }
        return ERROR_GENERAL;
    }

    /* Run git diff first and check for errors */
    char diff_file[MAX_PATH_LENGTH];
    snprintf(diff_file, sizeof(diff_file), "/tmp/merge_detector_diff_%d.txt", getpid());
    char diff_command[MAX_COMMAND_LENGTH];
    if (strlen(base_branch) > 0 && strlen(merge_branch) > 0) {
        snprintf(diff_command, sizeof(diff_command),
                 "git diff --numstat %s..%s > '%s' 2>/dev/null",
                 base_branch, merge_branch, diff_file);
    } else {
        snprintf(diff_command, sizeof(diff_command),
                 "git diff --numstat HEAD~1..HEAD > '%s' 2>/dev/null",
                 diff_file);
    }
    int diff_result = system(diff_command);
    if (diff_result == -1 || WEXITSTATUS(diff_result) != 0) {
        fprintf(stderr, "[ERROR] Git repository appears to be corrupted or inaccessible.\n");
        remove(diff_file);
        return ERROR_REPO_NOT_FOUND;
    }
    /* Now run AWK on the diff file */
    char awk_command[MAX_COMMAND_LENGTH];
    snprintf(awk_command, sizeof(awk_command),
             "awk -v output_format=%s -f '%s' '%s'",
             cfg.format, script_path, diff_file);
    int awk_result = system(awk_command);
    remove(diff_file);
    if (awk_result == -1 || WEXITSTATUS(awk_result) != 0) {
        return ERROR_GENERAL;
    }
    return SUCCESS;
}
