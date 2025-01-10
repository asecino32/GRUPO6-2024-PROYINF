from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
""" class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(blank=True, default='', unique=True)
    username = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    class Meta:
        db_table = 'tasks_customuser'

    def __str__(self):
        return self.email """


class Fuente(models.Model):
    id_fuente = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=1000)
    fuente_activa = models.BooleanField(blank=False)
    url = models.URLField(max_length=200)
    def __str__(self):
        return f"{self.titulo} {self.url} {self.fuente_activa}"


class Boletin(models.Model):
    id_boletin = models.AutoField(primary_key=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    titulo = models.CharField(max_length=100)
    ciudad_tratada = models.CharField(max_length=100)
    tematica = models.CharField(max_length=100)
    archivo = models.FileField(upload_to='pdfs/')
    fuente_boletin = models.ForeignKey(Fuente, on_delete=models.CASCADE, related_name='fuente')