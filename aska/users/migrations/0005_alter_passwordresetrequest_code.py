# Generated by Django 4.2.5 on 2023-11-05 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_passwordresetrequest_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetrequest',
            name='code',
            field=models.CharField(default='510879', editable=False, max_length=100),
        ),
    ]
