# Generated by Django 5.0.9 on 2024-10-24 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0007_rename_subscription_usersubscription_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
