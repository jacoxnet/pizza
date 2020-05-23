# Generated by Django 2.2.12 on 2020-05-22 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Addon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Pizza'), (2, 'Sub')])),
            ],
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='topping',
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='category',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Pizza'), (2, 'Sicilian Pizza'), (4, 'sub'), (6, 'pasta'), (7, 'salad'), (8, 'dinner platter')]),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='size',
            field=models.CharField(choices=[('L', 'Large'), ('S', 'Small'), ('N', 'No Size')], max_length=1),
        ),
        migrations.DeleteModel(
            name='Topping',
        ),
        migrations.AddField(
            model_name='menuitem',
            name='addon',
            field=models.ManyToManyField(blank=True, to='orders.Addon'),
        ),
    ]
