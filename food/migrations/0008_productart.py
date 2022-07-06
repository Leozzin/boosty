# Generated by Django 3.1 on 2022-07-05 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0007_activitylevel_diettype'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductArt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField(max_length=10000)),
                ('price', models.FloatField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.categorie')),
            ],
        ),
    ]
