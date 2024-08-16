from django.contrib import admin
from .models import User, Room, Reservation, Stay

class UserAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'rol')
    search_fields = ('nombre', 'email')

class RoomAdmin(admin.ModelAdmin):
    list_display = ('numero', 'tipo', 'precio_por_noche', 'disponible')
    search_fields = ('numero', 'tipo')
    list_filter = ('tipo', 'disponible')

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'get_room_numero', 'fecha_inicio', 'fecha_fin', 'total')
    search_fields = ('usuario__nombre', 'room__numero')
    list_filter = ('fecha_inicio', 'fecha_fin')

    def get_room_numero(self, obj):
        return obj.room.numero
    get_room_numero.short_description = 'Número de Habitación'

class StayAdmin(admin.ModelAdmin):
    list_display = ('reserva', 'fecha_check_in', 'fecha_check_out')
    search_fields = ('reserva__usuario__nombre',)
    list_filter = ('fecha_check_in', 'fecha_check_out')

admin.site.register(User, UserAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Stay, StayAdmin)
