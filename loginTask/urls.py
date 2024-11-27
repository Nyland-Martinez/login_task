from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect

def redirect_to_login(request):
    return HttpResponseRedirect('/usuarios/login/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('', redirect_to_login),
]
