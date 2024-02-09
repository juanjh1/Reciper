# Generated by Django 4.2.9 on 2024-02-09 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("panel", "0005_alter_service_picture"),
    ]

    operations = [
        migrations.CreateModel(
            name="Preparation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("about", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Receta",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("prep_time", models.IntegerField()),
                ("cook_time", models.IntegerField()),
                ("serves", models.IntegerField()),
                ("level", models.CharField(max_length=30)),
                ("tag", models.CharField(max_length=30)),
                ("about", models.CharField(max_length=1000)),
                ("picture", models.ImageField(upload_to="recipe/")),
            ],
        ),
        migrations.CreateModel(
            name="Preparation_time_item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=70)),
                ("description", models.CharField(max_length=200)),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="panel.preparation",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="preparation",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="panel.receta"
            ),
        ),
        migrations.CreateModel(
            name="Part_of_reciept",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="panel.receta"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Item_of_recipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("item", models.CharField(max_length=70)),
                (
                    "Part_of_reciept",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="panel.part_of_reciept",
                    ),
                ),
            ],
        ),
    ]