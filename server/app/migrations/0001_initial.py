# Generated by Django 3.2.5 on 2021-07-30 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=0)),
                ('value', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Measurement',
                'verbose_name_plural': 'Measurement',
                'db_table': 'app_measurements',
            },
        ),
    ]
