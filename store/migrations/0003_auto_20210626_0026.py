# Generated by Django 3.2.4 on 2021-06-26 00:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20210625_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='store.pet'),
        ),
        migrations.AlterField(
            model_name='pet',
            name='type',
            field=models.CharField(choices=[('dog', 'Dog')], default='dog', max_length=50),
        ),
    ]
