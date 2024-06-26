# Generated by Django 5.0.6 on 2024-06-26 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0003_alter_user_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                db_index=True, max_length=128, unique=True, verbose_name="Email"
            ),
        ),
    ]
