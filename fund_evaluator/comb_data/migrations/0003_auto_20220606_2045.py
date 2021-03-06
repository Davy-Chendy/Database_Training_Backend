# Generated by Django 3.1.3 on 2022-06-06 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comb_data', '0002_auto_20220527_0015'),
    ]

    operations = [
        migrations.RenameField(
            model_name='combdata',
            old_name='GraphSpotList',
            new_name='compose',
        ),
        migrations.RenameField(
            model_name='combdata',
            old_name='nicheng',
            new_name='nickname',
        ),
        migrations.AddField(
            model_name='combdata',
            name='drawdown',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='combdata',
            name='earnDrawdownRatio',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='combdata',
            name='rise',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='combdata',
            name='sharpeRatio',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='combdata',
            name='volatility',
            field=models.JSONField(null=True),
        ),
    ]
