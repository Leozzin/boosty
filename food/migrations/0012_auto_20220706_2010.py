# Generated by Django 3.1 on 2022-07-06 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0011_productart_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderline',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.productart'),
        ),
    ]
