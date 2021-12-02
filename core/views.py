from django.shortcuts import render
from core.models import evento

# Create your views here.
# Função para redirecionar a raiz, precisa acrescenatr redirect em from django.shortcuts import render, redirect
#def index(request):
    #return redirect('/agenda/')

def lista_eventos(request):
    usuario = request.user                         ### Receber o usuario logado no Django
    #valor = evento.objects.get(id=2)              ### Uma opção para setar somente um unico registro
    #valor = evento.objects.all()                  ### Mostra todos os registro
    valor = evento.objects.filter(usuario=usuario) ### Fltra pelo usuario logado no Django
    dic_evento = {'chave':valor}
    return render(request, 'agenda.html', dic_evento)