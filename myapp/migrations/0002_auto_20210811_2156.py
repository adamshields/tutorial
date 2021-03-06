# Generated by Django 3.2.6 on 2021-08-12 01:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['id', 'name'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='listing',
            options={'ordering': ['id', 'title'], 'verbose_name': 'Listing', 'verbose_name_plural': 'Listings'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['id', 'display_name'], 'verbose_name': 'Profile', 'verbose_name_plural': 'Profiles'},
        ),
    ]
