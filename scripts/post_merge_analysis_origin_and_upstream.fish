#!/usr/bin/env fish

# After all PRs are merged, run the full analysis
mkdir -p analysis_logs
git fetch --all
git status > analysis_logs/repo_status.log
git log --graph --oneline --decorate upstream/main...origin/staging > analysis_logs/commit_history.log
git diff --name-status upstream/main origin/staging > analysis_logs/changed_files.log
git diff --stat upstream/main origin/staging > analysis_logs/diff_stats.log
