# Generated by Django 5.1.2 on 2025-05-12 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_comentario'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlantillaBoletin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('contenido_html', models.TextField()),
            ],
        ),
    ]
