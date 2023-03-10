# Generated by Django 4.1.7 on 2023-03-04 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_user_user_score_alter_user_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_habit_drink',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_habit_smoke',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='who_to_date',
            field=models.CharField(max_length=2),
        ),
    ]
