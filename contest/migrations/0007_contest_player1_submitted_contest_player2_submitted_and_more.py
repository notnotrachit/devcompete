# Generated by Django 4.2.7 on 2023-11-27 09:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contest', '0006_contest_ai_result_analysis'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='player1_submitted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contest',
            name='player2_submitted',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player1_score', models.IntegerField()),
                ('player2_score', models.IntegerField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contest.contest')),
                ('player1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player1_result', to=settings.AUTH_USER_MODEL)),
                ('player2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player2_result', to=settings.AUTH_USER_MODEL)),
                ('winner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='winner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]