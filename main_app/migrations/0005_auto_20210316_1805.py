# Generated by Django 3.1.7 on 2021-03-16 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_auto_20210316_0545'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(verbose_name='Review Date'),
        ),
    ]