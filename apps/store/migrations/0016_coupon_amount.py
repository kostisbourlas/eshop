# Generated by Django 2.2.12 on 2020-05-27 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_order_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='amount',
            field=models.FloatField(default=5),
            preserve_default=False,
        ),
    ]
