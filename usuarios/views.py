from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from .forms import (CustomUserCreationForm, UserUpdateForm)
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import (CreateView, DetailView, DeleteView)
from django.views.generic.edit import UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.views import (PasswordChangeView, PasswordChangeDoneView)

User = get_user_model()

class UserCreateAndLoginView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'usuarios/signup.html'
    success_url = reverse_lazy('tasks:index')  # Redirige a tareas tras crear el usuario

    def form_valid(self, form):
        # Si el formulario es válido, se guarda el usuario
        response = super().form_valid(form)
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')  # Usamos la contraseña proporcionada
        # Intentamos autenticar al usuario
        user = authenticate(email=email, password=password)
        login(self.request, user)  # Realiza el login automáticamente tras el registro
        return response

class OnlyYouMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser

class UserDetail(OnlyYouMixin, DetailView):
    model = User
    template_name = 'usuarios/user_detail.html'

class UserUpdate(OnlyYouMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'usuarios/user_edit.html'
    
    # Redirigir a la vista de detalles del usuario después de la actualización
    def get_success_url(self):
        return reverse_lazy('user_detail', kwargs={'pk': self.object.pk})  # Usar el pk del objeto actualizado
    
class PasswordChange(PasswordChangeView):
    template_name = 'usuarios/password_change.html'

class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'usuarios/user_detail.html'

class UserDelete(DeleteView):
    model = User
    template_name = 'usuarios/user_delete.html'
    success_url = reverse_lazy('login')  # Redirige al login tras eliminar la cuenta
