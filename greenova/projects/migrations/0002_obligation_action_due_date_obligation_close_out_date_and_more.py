# Generated by Django 5.1.6 on 2025-02-12 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="obligation",
            name="action_due_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="obligation",
            name="close_out_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="obligation",
            name="compliance_comments",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="obligation",
            name="covered_in_which_inspection_checklist",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="obligation",
            name="evidence",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="obligation",
            name="gap_analysis",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="obligation",
            name="general_comments",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="obligation",
            name="inspection",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="obligation",
            name="inspection_frequency",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="obligation",
            name="new_control_action_required",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="obligation",
            name="non_conformance_comments",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="obligation",
            name="notes_for_gap_analysis",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="obligation",
            name="obligation_type",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="obligation",
            name="person_email",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name="obligation",
            name="procedure",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="obligation",
            name="project_phase",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="obligation",
            name="recurring_forcasted_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="obligation",
            name="recurring_frequency",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="obligation",
            name="recurring_obligation",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="obligation",
            name="recurring_status",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="obligation",
            name="site_or_desktop",
            field=models.CharField(
                blank=True,
                choices=[("Site", "Site"), ("Desktop", "Desktop")],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="obligation",
            name="supporting_information",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="obligation",
            name="accountability",
            field=models.CharField(default="Unassigned", max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="obligation",
            name="environmental_aspect",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="obligation",
            name="primary_environmental_mechanism",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="obligation",
            name="responsibility",
            field=models.CharField(default="Unassigned", max_length=255),
            preserve_default=False,
        ),
        migrations.AddIndex(
            model_name="obligation",
            index=models.Index(
                fields=["project"], name="projects_ob_project_f8fa6f_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="obligation",
            index=models.Index(fields=["status"], name="projects_ob_status_ed6574_idx"),
        ),
        migrations.AddIndex(
            model_name="obligation",
            index=models.Index(
                fields=["action_due_date"], name="projects_ob_action__8808ad_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="obligation",
            index=models.Index(
                fields=["project_phase"], name="projects_ob_project_396a13_idx"
            ),
        ),
    ]
