# Generated by Django 4.2.18 on 2025-02-14 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GT_Movies_Store', '0011_order_status_alter_orderitem_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='tmdb_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='price',
            field=models.DecimalField(decimal_places=2, default=8.0, max_digits=10),
        ),
    ]
