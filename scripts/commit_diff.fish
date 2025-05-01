#!/usr/bin/env fish

begin
    echo "Branch: cherry-pick/selected-pr-updates" >> /workspaces/greenova/logs/commit-diff.log
    git log --oneline --graph staging..cherry-pick/selected-pr-updates >> /workspaces/greenova/logs/commit-diff.log
    echo "Branch: pr/Channing88/90" >> /workspaces/greenova/logs/commit-diff.log
    git log --oneline --graph staging..pr/Channing88/90 >> /workspaces/greenova/logs/commit-diff.log
    echo "Branch: pr/JaredStanbrook/97" >> /workspaces/greenova/logs/commit-diff.log
    git log --oneline --graph staging..pr/JaredStanbrook/97 >> /workspaces/greenova/logs/commit-diff.log
    echo "Branch: pr/mhahmad0/102" >> /workspaces/greenova/logs/commit-diff.log
    git log --oneline --graph staging..pr/mhahmad0/102 >> /workspaces/greenova/logs/commit-diff.log
    echo "Branch: pr/mhahmad0/99" >> /workspaces/greenova/logs/commit-diff.log
    git log --oneline --graph staging..pr/mhahmad0/99 >> /workspaces/greenova/logs/commit-diff.log
    echo "Branch: dotenv-vault" >> /workspaces/greenova/logs/commit-diff.log
    git log --oneline --graph staging..dotenv-vault >> /workspaces/greenova/logs/commit-diff.log
    echo "Branch: cameronsims/main" >> /workspaces/greenova/logs/commit-diff.log
    git log --oneline --graph staging..cameronsims/main >> /workspaces/greenova/logs/commit-diff.log
    echo "Branch: feature/issue53" >> /workspaces/greenova/logs/commit-diff.log
    git log --oneline --graph staging..feature/issue53 >> /workspaces/greenova/logs/commit-diff.log
    echo "Branch: mhahmad0/issue72" >> /workspaces/greenova/logs/commit-diff.log
    git log --oneline --graph staging..mhahmad0/issue72 >> /workspaces/greenova/logs/commit-diff.log
    echo "Branch: mhahmad0/issue87" >> /workspaces/greenova/logs/commit-diff.log
    git log --oneline --graph staging..mhahmad0/issue87 >> /workspaces/greenova/logs/commit-diff.log
    echo "Branch: fix/import_obligations" >> /workspaces/greenova/logs/commit-diff.log
    git log --oneline --graph staging..fix/import_obligations >> /workspaces/greenova/logs/commit-diff.log
    echo "Branch: ipython-integration" >> /workspaces/greenova/logs/commit-diff.log
    git log --oneline --graph staging..ipython-integration >> /workspaces/greenova/logs/commit-diff.log
end
