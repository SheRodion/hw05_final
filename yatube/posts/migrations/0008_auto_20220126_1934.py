# Generated by Django 2.2.16 on 2022-01-26 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20220126_1915'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={'verbose_name_plural': 'Подписки'},
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='unique follow'),
        ),
        migrations.AlterModelTable(
            name='follow',
            table='Follow',
        ),
    ]