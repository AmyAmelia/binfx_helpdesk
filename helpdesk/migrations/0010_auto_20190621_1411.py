# Generated by Django 2.1.2 on 2019-06-21 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0009_auto_20190621_1408'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issue',
            old_name='iss_type',
            new_name='type',
        ),
        migrations.RenameField(
            model_name='requesttype',
            old_name='iss_type',
            new_name='type',
        ),
    ]
