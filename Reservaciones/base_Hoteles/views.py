
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import View, CreateView, UpdateView,ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReservationForm, RoomForm, CustomUserCreationForm, LoginForm, UserUpdateForm
from .forms import UserUpdateForm, ProfileUpdateForm
from rest_framework import viewsets
from .models import Profile, User, Room, Reservation, Stay
from .serializers import RoomSerializer, ReservationSerializer, StaySerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import datetime
from django.urls import reverse_lazy
from django.db import transaction



# Vista para User
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Vista para Room
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'rooms/room_list.html'
    context_object_name = 'rooms'

class RoomCreateView(LoginRequiredMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'rooms/room_form.html'
    success_url = reverse_lazy('rooms_list')

class RoomUpdateView(LoginRequiredMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'rooms/room_form.html'
    success_url = reverse_lazy('rooms_list')

class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'rooms/room_confirm_delete.html'
    success_url = reverse_lazy('rooms_list')
    
# # botones view
# class ReservationUpdateView(LoginRequiredMixin, UpdateView):
#     model = Reservation
#     form_class = ReservationForm
#     template_name = 'reservas/reservation_form.html'
#     success_url = reverse_lazy('reservations_list')

# class ReservationDeleteView(LoginRequiredMixin, DeleteView):
#     model = Reservation
#     template_name = 'reservas/reservation_confirm_delete.html'
#     success_url = reverse_lazy('reservations_list')  

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'rooms/room_list.html', {'rooms': rooms})

# Vista para Reservation
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]    

class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'reservas/list_reservations.html'
    context_object_name = 'reservations'


def index(request):
    return render(request, 'index.html')   


# Loging
class CustomLoginView(View):
    template_name = 'login/login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
                else:
                    return render(request, self.template_name, {
                        'form': form,
                        'error_message': 'La cuenta está desactivada.'
                    })
            else:
                return render(request, self.template_name, {
                    'form': form,
                    'error_message': 'Usuario o contraseña incorrectos.'
                })
        return render(request, self.template_name, {'form': form})


        

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
    
class CustomSignupView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'login/register.html', {'form': form})
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])   
            user.save()  # Guarda el usuario en la base de datos
            return redirect('login')
        return render(request, 'login/register.html', {'form': form})

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        # Crear un perfil automáticamente si no existe
        profile = Profile.objects.create(user=request.user)
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)
        
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'login/perfil.html', context)

def make_reservation(request, id):
    room = get_object_or_404(Room, pk=id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.room = room
            reservation.usuario = request.user

            # Calcula el total según el número de noches
            nights = (reservation.fecha_fin - reservation.fecha_inicio).days
            reservation.total = nights * room.precio_por_noche

            reservation.save()
            return redirect('list_reservations')
    else:
        form = ReservationForm()

    return render(request, 'reservas/make_reservation.html', {'form': form, 'room': room})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def occupancy_statistics(request):
    total_rooms = Room.objects.count()
    occupied_rooms = Reservation.objects.filter(check_out__gte=datetime.datetime.now()).count()
    occupancy_rate = (occupied_rooms / total_rooms) * 100 if total_rooms > 0 else 0
    return Response({
        'total_rooms': total_rooms,
        'occupied_rooms': occupied_rooms,
        'occupancy_rate': occupancy_rate,
    })

# Vista para Stay
class StayViewSet(viewsets.ModelViewSet):
    queryset = Stay.objects.all()
    serializer_class = StaySerializer
