#!/usr/bin/env fish

# Create a comparison without modifying origin/staging
git fetch --all
git checkout -b pre_merge_analysis upstream/main
git diff --name-status upstream/main origin/staging > logs/pre_merge_analysis.log
git diff --stat upstream/main origin/staging >> logs/pre_merge_analysis.log
git checkout origin/staging
