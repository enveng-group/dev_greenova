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

### Add test data
```bash
python manage.py shell
```

```python
from projects.models import Project, Obligation
project = Project.objects.create(name="Test Project", description="Test Description")
obligation = Obligation.objects.create(
    obligation_number="TEST-001",
    project=project,
    primary_environmental_mechanism="Test Mechanism",
    environmental_aspect="Test Aspect",
    obligation="Test Obligation",
    accountability="Test Account",
    responsibility="Test Resp",
    status="not started"
)
```