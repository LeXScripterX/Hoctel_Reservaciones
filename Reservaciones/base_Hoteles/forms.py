from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile, Reservation, Room, Stay, User
from django.contrib.auth.forms import UserCreationForm

# Formulario para Reservation
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['usuario', 'fecha_inicio', 'fecha_fin', 'total']  # Incluyendo 'total' si es necesario

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_inicio'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        self.fields['fecha_fin'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        self.fields['total'].widget.attrs.update({'readonly': 'readonly'})  # Hacer que el campo 'total' sea solo lectura, si es calculado

# Formulario para Room
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['numero', 'tipo', 'precio_por_noche', 'disponible']

# Formulario para Stay (Estancia)
class StayForm(forms.ModelForm):
    class Meta:
        model = Stay
        fields = ['fecha_check_in', 'fecha_check_out', 'reserva']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_check_in'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        self.fields['fecha_check_out'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})



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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_check_in'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        self.fields['fecha_check_out'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio']