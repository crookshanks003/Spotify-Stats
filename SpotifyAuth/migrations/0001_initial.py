# Generated by Django 3.1.6 on 2021-02-14 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=100)),
                ('access_key', models.CharField(max_length=100)),
                ('refresh_key', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user_name', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
