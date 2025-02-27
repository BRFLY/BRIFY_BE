# Generated by Django 5.0.7 on 2024-07-18 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('link', models.TextField()),
                ('pubDate', models.CharField(max_length=10)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
