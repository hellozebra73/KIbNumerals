# Generated by Django 2.0.5 on 2018-08-01 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opp', '0004_auto_20180801_1820'),
    ]

    operations = [
        migrations.RenameField(
            model_name='problem',
            old_name='number_of_numeral',
            new_name='number_of_numerals',
        ),
    ]