from django.db import models
from django.contrib.auth.models import User # importação feita para o novo campo usuario da tabela evento
# Create your models here.

# Criação da tabela dentro do banco de dados
class evento(models.Model):
    titulo = models.CharField(verbose_name='Título', max_length=100)
    descricao = models.TextField(verbose_name='Descrição', blank=True, null=True)
    local = models.CharField(verbose_name='Local', blank=True, null=True, max_length=100)
    data_evento = models.DateTimeField(verbose_name='Data do Evento')
    data_criacao = models.DateTimeField(verbose_name='Data da Criação', auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) #criando novo campo para fazer o relacionamento com a tabela usuario do django

    # Depois será preciso executar os seguinte comando via Terminal
    # 01
    # >>> python manage.py makemigrations core ### core é o nome da aplicação
    # 02
    # >>> python manage.py sqlmigrate core 0001 ### 0001 é referente a migração especifica
    # 03
    # >>> python manage.py migrate core 0001
    # 04
    # Depois faz o registro em admin.py
    # from core.models import evento
    # admin.site.register(evento

    # Aqui podemos definir o nome que queremos para nossa tabela do banco de dados
    class Meta:
        db_table = 'evento'

    # Ajusta o formato do titulo para string e remover o nome objeto colocado automaticamente
    def __str__(self):
        return self.titulo

    def get_data_evento(self):
        return self.data_evento.strftime('%d/%m/%Y às %H:%M')

    def get_data_input_evento(self):
        return self.data_evento.strftime('%Y-%m-%dT%H:%M')