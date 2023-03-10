# Generated by Django 4.1.3 on 2023-01-03 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=100)),
                ('lname', models.CharField(max_length=100)),
                ('mobile', models.PositiveIntegerField()),
                ('address', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=80)),
                ('profile_pic', models.ImageField(upload_to='profile_pic')),
                ('usertype', models.CharField(default='buyer', max_length=100)),
            ],
        ),
    ]
