# Generated by Django 4.2.7 on 2024-01-11 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pratice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.TextField(),
        ),
    ]