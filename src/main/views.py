from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html', context={})

def login(request):
    return render(request, 'login.html', context={})

def redirect_to_index(request):
    return redirect('/')

def error404(request):
    return render(request, 'errors/page_404.html', context={})