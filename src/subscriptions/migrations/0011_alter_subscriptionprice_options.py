# Generated by Django 5.0.9 on 2024-10-24 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0010_subscriptionprice_featured_subscriptionprice_order_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscriptionprice',
            options={'ordering': ['order', 'featured', '-updated']},
        ),
    ]