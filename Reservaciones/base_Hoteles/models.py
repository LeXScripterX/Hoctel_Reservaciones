from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=50, choices=[('cliente', 'Cliente'), ('administrador', 'Administrador')])

    # Cambiando el related_name para evitar conflictos
    groups = models.ManyToManyField(
        Group,
        related_name='base_hoteles_user_groups',  # Cambiado para evitar conflictos con el modelo de Django
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='base_hoteles_user_permissions',  # Cambiado para evitar conflictos con el modelo de Django
        blank=True
    )

    def __str__(self):
        return self.nombre


# Modelo de Habitación
class Room(models.Model):
    id = models.AutoField(primary_key=True)
    numero = models.CharField(max_length=10)
    tipo = models.CharField(max_length=50, choices=[('simple', 'Simple'), ('doble', 'Doble'), ('suite', 'Suite')])
    precio_por_noche = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.tipo} - {self.numero}'

# Modelo de Reserva
class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')

    def __str__(self):
        return f'Reserva {self.id} - {self.usuario.nombre}'

# Modelo de Estancia
class Stay(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_check_in = models.DateTimeField()
    fecha_check_out = models.DateTimeField()
    reserva = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='stay')

    def __str__(self):
        return f'Estancia {self.id} - {self.reserva.usuario.nombre}'


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='default_profile_picture.jpg', upload_to='profile_pics')
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'