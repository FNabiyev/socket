# Generated by Django 3.1.7 on 2021-04-02 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20210331_0206'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
