from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_delete_obligation'),  # Fixed dependency to point to actual previous migration
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('owner', 'Owner'), ('manager', 'Manager'), ('member', 'Member'), ('viewer', 'Viewer')], default='member', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='projects.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_memberships', to='auth.user')),
            ],
            options={
                'verbose_name': 'Project Membership',
                'verbose_name_plural': 'Project Memberships',
                'unique_together': {('user', 'project')},
            },
        ),
    ]