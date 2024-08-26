from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
     index, CustomLoginView, CustomLogoutView, CustomSignupView,
     profile, RoomListView, RoomCreateView, RoomUpdateView, RoomDeleteView, make_reservation, ReservationListView )
#UserViewSet, RoomViewSet, ReservationViewSet, StayViewSet, index
"""router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'stays', StayViewSet)
"""

urlpatterns = [
    path('', index, name='index'), 
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', CustomSignupView.as_view(), name='register'),
    path('profile/', profile, name='profile'),
    path('rooms/', RoomListView.as_view(), name='rooms_list'),
    path('rooms/create/', RoomCreateView.as_view(), name='room_create'),
    path('rooms/update/<int:pk>/', RoomUpdateView.as_view(), name='room_edit'),
    path('rooms/delete/<int:pk>/', RoomDeleteView.as_view(), name='room_delete'),
    path('rooms/reserve/<int:id>/', make_reservation, name='make_reservation'),
    path('reservations/', ReservationListView.as_view(), name='list_reservations'),
    
]

 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
Para un usuario con rol de "cliente", deberías seleccionar los permisos que le permitan realizar las acciones necesarias, pero sin dar acceso a funciones administrativas. Aquí te sugiero los tipos de permisos que deberías considerar:

Room Permissions:

Can view room (Ver habitaciones)
Reservation Permissions:

Can add reservation (Realizar reservas)
Can change reservation (Modificar sus propias reservas)
Can view reservation (Ver sus propias reservas)
Stay Permissions:

Can view stay (Ver sus propias estancias)
User Permissions:

Can view user (Ver su propio perfil)
Can change user (Modificar su propio perfil)
No deberías seleccionar permisos como Can delete, Can add room, Can change room, Can delete reservation, o cualquier permiso relacionado con la administración de usuarios o habitaciones, ya que esos son para roles administrativos.
"""