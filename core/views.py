from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from core.models import evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout # precisa para efetuar o login
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse

# Create your views here.
# Função para redirecionar a raiz, precisa acrescentar redirect em from django.shortcuts import render, redirect
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
    data_atual = datetime.now() - timedelta(hours=1)
    valor = evento.objects.filter(usuario=usuario, ### Fltra pelo usuario logado no Django
                                  data_evento__gt=data_atual) # __gt siginifica se data de evento for maior que, se quiser menor que utilize __lt
    dic_evento = {'chave':valor}
    return render(request, 'agenda.html', dic_evento)

@login_required(login_url='/login/')
def lista_eventos_passado(request):
    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=1)
    valor = evento.objects.filter(usuario=usuario, ### Fltra pelo usuario logado no Django
                                  data_evento__lt=data_atual) # __gt siginifica se data de evento for maior que, se quiser menor que utilize __lt
    dic_evento = {'chave':valor}
    return render(request, 'eventos_passado.html', dic_evento)

@login_required(login_url='/login/')
def novo_evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = evento.objects.get(id=id_evento)
    return render(request, 'novo_evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        local = request.POST.get('local')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        if id_evento:
            Evento = evento.objects.get(id=id_evento)
            if Evento.usuario == usuario:
                Evento.titulo = titulo
                Evento.local = local
                Evento.descricao = descricao
                Evento.data_evento = data_evento
                Evento.save()
            # ABAIXO É OUTRA MANEIRA DE ALTERAR OS DADOS
            # evento.objects.filter(id=id_evento).update(titulo=titulo,
            #                                            local=local,
            #                                            data_evento=data_evento,
            #                                            descricao=descricao,
            #                                            usuario=usuario)
        else:
            evento.objects.create(titulo=titulo,
                              local=local,
                              data_evento=data_evento,
                              descricao=descricao,
                              usuario=usuario)

    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        Evento = evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    if usuario == Evento.usuario:
        Evento.delete()
    else:
        raise Http404()
    return redirect('/')

#abaixo uma maneira de passar os dados por API por exemplo
def json_lista_evento(request, id_usuario):
    usuario = User.objects.get(id=id_usuario)
    Evento = evento.objects.filter(usuario=usuario).values('id', 'titulo')
    return JsonResponse(list(Evento), safe=False)

# @login_required(login_url='/login/')
# def json_lista_evento(request):
#     usuario = request.user
#     Evento = evento.objects.filter(usuario=usuario).values('id', 'titulo')
#     return JsonResponse(list(Evento), safe=False)

