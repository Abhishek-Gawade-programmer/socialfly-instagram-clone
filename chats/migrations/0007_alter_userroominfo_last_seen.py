# Generated by Django 3.2.5 on 2021-08-11 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0006_userroominfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userroominfo',
            name='last_seen',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
