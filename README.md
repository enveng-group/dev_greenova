# Readme

# 1. Switch to main and get latest changes
git checkout main
git pull origin main

# 2. Squash and merge the feature branch
git merge --squash feature-branch
git commit -m "feat: squashed commit message"

# 3. Push changes to main
git push origin main

# 4. Delete feature branch locally
git branch -D feature-branch

# 5. Delete feature branch remotely
git push origin --delete feature-branch


