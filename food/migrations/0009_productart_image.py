# Generated by Django 3.1 on 2022-07-05 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0008_productart'),
    ]

    operations = [
        migrations.AddField(
            model_name='productart',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/product_art/'),
        ),
    ]
