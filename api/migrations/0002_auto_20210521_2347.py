# Generated by Django 3.2.3 on 2021-05-21 18:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clothes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_Clothes', models.CharField(max_length=50)),
                ('type_Clothes', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('link_Image', models.URLField(max_length=255)),
                ('link_Source', models.URLField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'Clothes',
                'verbose_name_plural': 'Clothes',
            },
        ),
        migrations.CreateModel(
            name='SetOfClothes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_Set_Of_Clothes', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.DeleteModel(
            name='UserClothes',
        ),
        migrations.AddField(
            model_name='setofclothes',
            name='users',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clothes',
            name='set_Of_Clothes',
            field=models.ManyToManyField(to='api.SetOfClothes'),
        ),
    ]