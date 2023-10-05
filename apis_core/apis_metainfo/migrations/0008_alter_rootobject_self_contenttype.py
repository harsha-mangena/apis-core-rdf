# Generated by Django 4.1.11 on 2023-10-11 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("apis_metainfo", "0007_delete_source"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rootobject",
            name="self_contenttype",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
        ),
    ]
