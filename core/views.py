from django.shortcuts import render, redirect
from core.models import evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout # precisa para efetuar o login
from django.contrib import messages

# Create your views here.
# Função para redirecionar a raiz, precisa acrescenatr redirect em from django.shortcuts import render, redirect
#def index(request):
    #return redirect('/agenda/')

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou Senha Inválido!!!") # precisou from django.contrib import messages
    return redirect('/')


@login_required(login_url='/login/') # solicitar login precisou importar from django.contrib.auth.decorators import login_required

def lista_eventos(request):
    usuario = request.user                         ### Receber o usuario logado no Django
    #valor = evento.objects.get(id=2)              ### Uma opção para setar somente um unico registro
    #valor = evento.objects.all()                  ### Mostra todos os registro
    valor = evento.objects.filter(usuario=usuario) ### Fltra pelo usuario logado no Django
    dic_evento = {'chave':valor}
    return render(request, 'agenda.html', dic_evento)