# Generated by Django 5.1.6 on 2025-02-14 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0004_alter_project_options_alter_obligation_project"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="obligation",
            options={
                "ordering": ["action_due_date", "obligation_number"],
                "verbose_name": "Obligation",
                "verbose_name_plural": "Obligations",
            },
        ),
        migrations.AlterModelOptions(
            name="project",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Project",
                "verbose_name_plural": "Projects",
            },
        ),
        migrations.RemoveIndex(
            model_name="obligation",
            name="projects_ob_project_f8fa6f_idx",
        ),
        migrations.RemoveIndex(
            model_name="obligation",
            name="projects_ob_status_ed6574_idx",
        ),
        migrations.RemoveIndex(
            model_name="obligation",
            name="projects_ob_action__8808ad_idx",
        ),
        migrations.RemoveIndex(
            model_name="obligation",
            name="projects_ob_project_396a13_idx",
        ),
        migrations.AlterField(
            model_name="obligation",
            name="environmental_aspect",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="obligation",
            name="primary_environmental_mechanism",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="obligation",
            name="project_phase",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="obligation",
            name="site_or_desktop",
            field=models.CharField(
                blank=True,
                choices=[("Site", "Site"), ("Desktop", "Desktop")],
                max_length=10,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="obligation",
            name="status",
            field=models.CharField(
                choices=[
                    ("not started", "Not Started"),
                    ("in progress", "In Progress"),
                    ("completed", "Completed"),
                ],
                default="not started",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
