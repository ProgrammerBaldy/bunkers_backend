# Generated by Django 3.1.6 on 2021-02-10 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('measure_unit', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Product_subproducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productid', models.IntegerField()),
                ('subproductid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Product_supplies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productid', models.IntegerField()),
                ('supplyid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Subproduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('measure_unit', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Subproduct_supplies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subproductid', models.IntegerField()),
                ('supplyid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Supply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('measure_unit', models.CharField(max_length=20)),
            ],
        ),
    ]
