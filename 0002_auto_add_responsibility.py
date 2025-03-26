import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('global', '0001_initial'),
        ('responsibility', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='obligation',
            name='responsibility',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='responsibility.Responsibility',
            ),
        ),
    ]
