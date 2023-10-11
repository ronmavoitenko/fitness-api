# Generated by Django 3.2.16 on 2023-10-11 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Foods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('fats', models.IntegerField()),
                ('carbs', models.IntegerField()),
                ('proteins', models.IntegerField()),
                ('calories', models.IntegerField()),
                ('modified_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
