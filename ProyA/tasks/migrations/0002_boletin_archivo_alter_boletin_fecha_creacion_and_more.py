# Generated by Django 5.1.2 on 2024-11-05 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='boletin',
            name='archivo',
            field=models.FileField(default=1, upload_to='pdfs/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='boletin',
            name='fecha_creacion',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='fuente',
            name='url',
            field=models.URLField(),
        ),
    ]
