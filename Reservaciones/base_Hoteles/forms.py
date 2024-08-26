from django import forms
from .models import Profile, Reservation, Room, Stay, User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 

# Formulario Para Habitacion
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['numero', 'tipo', 'precio_por_noche', 'disponible']


# Formulario para reserva
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['fecha_inicio', 'fecha_fin', 'room']  # Agregamos 'room' al formulario
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_fin': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
def clean(self):
       cleaned_data = super().clean()
       fecha_inicio = cleaned_data.get('fecha_inicio')
       fecha_fin = cleaned_data.get('fecha_fin')
       room = cleaned_data.get('room')

       if fecha_inicio and fecha_fin and room:
           if fecha_inicio >= fecha_fin:
               raise forms.ValidationError("La fecha de inicio debe ser anterior a la fecha de fin.")
           
           # Verificar disponibilidad de la habitación
           if Reservation.objects.filter(
                room=room,
                fecha_inicio__lte=fecha_fin,
                fecha_fin__gte=fecha_inicio
            ).exists():
               raise forms.ValidationError("La habitación no está disponible para las fechas seleccionadas.")
           return cleaned_data
       

# Formulario personalizado para la creación de usuarios
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'nombre', 'rol')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])  # Asegúrate de que la contraseña se establezca correctamente
        if commit:
            user.save()
        return user
    

# Formulario para el inicio de sesión
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=63, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    # Formulario para actualizar datos del usuario
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'nombre', 'rol']

# Formulario para actualizar la estancia (Stay)
class StayUpdateForm(forms.ModelForm):
    class Meta:
        model = Stay
        fields = ['fecha_check_in', 'fecha_check_out']
        widgets = {
            'fecha_check_in': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_check_out': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio']