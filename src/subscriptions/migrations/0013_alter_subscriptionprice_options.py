# Generated by Django 5.0.9 on 2024-10-24 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0012_alter_subscription_options_subscription_featured_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscriptionprice',
            options={'ordering': ['subscription__order', 'order', 'featured', '-updated']},
        ),
    ]
