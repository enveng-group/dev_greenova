#!/usr/bin/env fish

begin
    echo "Branch: cherry-pick/selected-pr-updates" >> /workspaces/greenova/logs/file-diff.log
    git diff --name-only staging..cherry-pick/selected-pr-updates >> /workspaces/greenova/logs/file-diff.log
    echo "Branch: pr/Channing88/90" >> /workspaces/greenova/logs/file-diff.log
    git diff --name-only staging..pr/Channing88/90 >> /workspaces/greenova/logs/file-diff.log
    echo "Branch: pr/JaredStanbrook/97" >> /workspaces/greenova/logs/file-diff.log
    git diff --name-only staging..pr/JaredStanbrook/97 >> /workspaces/greenova/logs/file-diff.log
    echo "Branch: pr/mhahmad0/102" >> /workspaces/greenova/logs/file-diff.log
    git diff --name-only staging..pr/mhahmad0/102 >> /workspaces/greenova/logs/file-diff.log
    echo "Branch: pr/mhahmad0/99" >> /workspaces/greenova/logs/file-diff.log
    git diff --name-only staging..pr/mhahmad0/99 >> /workspaces/greenova/logs/file-diff.log
    echo "Branch: dotenv-vault" >> /workspaces/greenova/logs/file-diff.log
    git diff --name-only staging..dotenv-vault >> /workspaces/greenova/logs/file-diff.log
    echo "Branch: cameronsims/main" >> /workspaces/greenova/logs/file-diff.log
    git diff --name-only staging..cameronsims/main >> /workspaces/greenova/logs/file-diff.log
    echo "Branch: feature/issue53" >> /workspaces/greenova/logs/file-diff.log
    git diff --name-only staging..feature/issue53 >> /workspaces/greenova/logs/file-diff.log
    echo "Branch: mhahmad0/issue72" >> /workspaces/greenova/logs/file-diff.log
    git diff --name-only staging..mhahmad0/issue72 >> /workspaces/greenova/logs/file-diff.log
    echo "Branch: mhahmad0/issue87" >> /workspaces/greenova/logs/file-diff.log
    git diff --name-only staging..mhahmad0/issue87 >> /workspaces/greenova/logs/file-diff.log
    echo "Branch: fix/import_obligations" >> /workspaces/greenova/logs/file-diff.log
    git diff --name-only staging..fix/import_obligations >> /workspaces/greenova/logs/file-diff.log
    echo "Branch: ipython-integration" >> /workspaces/greenova/logs/file-diff.log
    git diff --name-only staging..ipython-integration >> /workspaces/greenova/logs/file-diff.log
end
