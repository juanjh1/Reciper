# Generated by Django 4.2.9 on 2024-02-09 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("panel", "0006_preparation_receta_preparation_time_item_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="item_of_recipe", old_name="Part_of_reciept", new_name="segundo",
        ),
    ]
