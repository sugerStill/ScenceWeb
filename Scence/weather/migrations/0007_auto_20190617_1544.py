# Generated by Django 2.2.1 on 2019-06-17 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0006_auto_20190617_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historyweather',
            name='pid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='History', to='weather.City', to_field='citypid'),
        ),
        migrations.DeleteModel(
            name='WeatherManager',
        ),
    ]
