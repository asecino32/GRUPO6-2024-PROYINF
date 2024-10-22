# python manage.py insertar_boletin
from django.core.management.base import BaseCommand
from tasks.models import Boletin, Fuente  # Asegúrate de importar tus modelos
from datetime import date

class Command(BaseCommand):
    help = 'Inserta un nuevo boletín y su fuente asociada'

    def handle(self, *args, **kwargs):
        # Crear una nueva fuente
        nueva_fuente = Fuente(
            titulo='CNN',
            descripcion='Temblo fuerte',
            fuente_activa=True,  # Cambia a False si no está activa
            url='http://cnn.org'
        )
        nueva_fuente.save()

        # Crear un nuevo boletín asociado a la fuente
        nuevo_boletin = Boletin(
            fecha_creacion=date.today(),  # Puedes ajustar la fecha según necesites
            titulo='Terremoto',
            ciudad_tratada='Santiago',
            tematica='Desastres',
            fuente_boletin=nueva_fuente
        )
        nuevo_boletin.save()

        self.stdout.write(self.style.SUCCESS('Boletín y fuente insertados exitosamente'))
