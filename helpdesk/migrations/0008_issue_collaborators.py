# Generated by Django 2.1.2 on 2019-06-18 10:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('helpdesk', '0007_auto_20190531_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='collaborators',
            field=models.ManyToManyField(blank=True, null=True, related_name='colab_issues', to=settings.AUTH_USER_MODEL),
        ),
    ]
