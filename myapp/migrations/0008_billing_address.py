# Generated by Django 4.1.3 on 2023-02-09 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_delete_billing_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Billing_Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=100)),
                ('lname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.PositiveIntegerField()),
                ('address', models.TextField()),
                ('billing_country', models.CharField(choices=[('USA', 'USA'), ('India', 'India'), ('UAE', 'UAE'), ('Kuwait', 'Kuwait')], max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=100)),
            ],
        ),
    ]
