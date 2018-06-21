from django.contrib import admin

# Register your models here.
from django.shortcuts import redirect

from main.views import login

def redirect_to_login(request):
    return redirect('login')

admin.site.site_header = "Administración Aquasoft"
admin.site.login = redirect_to_login
