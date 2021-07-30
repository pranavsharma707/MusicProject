# Generated by Django 3.2.5 on 2021-07-14 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicapp', '0002_auto_20210712_0937'),
    ]

    operations = [
        migrations.RenameField(
            model_name='music',
            old_name='author',
            new_name='artist',
        ),
        migrations.AlterField(
            model_name='music',
            name='path',
            field=models.FileField(upload_to='music/'),
        ),
    ]
