# Generated by Django 4.1.7 on 2023-04-02 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_submission_prepod_submission_student_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='prepod',
            field=models.CharField(max_length=150, null=True),
        ),
    ]