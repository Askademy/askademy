# Generated by Django 4.2.5 on 2023-10-14 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0004_alter_passwordresetrequest_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetrequest',
            name='code',
            field=models.CharField(default='102069', editable=False, max_length=100),
        ),
    ]
