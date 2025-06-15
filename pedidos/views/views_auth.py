from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from pedidos.decorators import login_required_if_not_debug

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")  # ajuste para sua view principal
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    return render(request, "pedidos/login.html")

@login_required_if_not_debug
def logout_view(request):
    logout(request)
    return redirect("login")
