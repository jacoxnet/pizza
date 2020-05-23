# Generated by Django 2.0.3 on 2020-05-22 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.PositiveSmallIntegerField(choices=[(1, 'pizza'), (2, 'Sicilian Pizza'), (3, 'pizza topping'), (4, 'sub'), (5, 'sub add-on'), (6, 'pasta'), (7, 'salad'), (8, 'dinner platter')])),
                ('name', models.CharField(max_length=64)),
                ('size', models.CharField(choices=[('L', 'Large'), ('S', 'Small')], max_length=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.AddField(
            model_name='menuitem',
            name='topping',
            field=models.ManyToManyField(blank=True, to='orders.Topping'),
        ),
    ]
