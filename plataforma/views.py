from email.iterators import body_line_iterator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Imovel, Cidade, Visitas

def heart_clicked(**args):
    return args
clicked = heart_clicked()

def user(**args):
    return args
usuario = user()

@login_required(login_url='/auth/login')

def fav(request):
    id = int(request.GET.get('id'))
    fav = request.GET.get('fav')
    clicked[id] = fav
    
    # if len(usuario) > 0:
    #     for i in range(len(usuario)):
    #         if request.user in usuario[i]:
    #             print(usuario[i][0], usuario[i][1])
    #         else:
    #             clicked[id] = fav
    #             usuario[i].append([request.user, clicked[id]])
    #             print(usuario)
    #             print('else 2')
    # else:
    #     clicked[id] = fav
    #     usuario[0] = [request.user, clicked[id]]
    #     print(usuario)
    #     print('else 1')
                   
    return HttpResponse("{}".format(clicked)), clicked

def home(request):
    preco_minimo = request.GET.get('preco_minimo')
    preco_maximo = request.GET.get('preco_maximo')
    cidade = request.GET.get('cidade')
    tipo = request.GET.getlist('tipo')
    tipo_venda = request.GET.getlist('tipo_venda')
    fav = request.GET.get('favorito')
    cidades = Cidade.objects.all()
    if preco_minimo or preco_maximo or cidade or tipo:
        
        if not preco_minimo:
            preco_minimo = 0
        if not preco_maximo:
            preco_maximo = 999999999
        if not tipo:
            tipo = ['A', 'C']
        if not tipo_venda:
            tipo_venda = ['V', 'A']
        
        if cidade == '0':
            if fav == 'true':
                if clicked > 0:
                    Imovel.favorito = True
                    imoveis = Imovel.objects.filter(valor__gte=preco_minimo)\
                    .filter(valor__lte=preco_maximo)\
                    .filter(tipo_imovel__in=tipo)\
                    .filter(tipo__in=tipo_venda)\
                    .filter(usuario=request.user)\
                    .filter(favorito__in=clicked)
                else:
                    imoveis = Imovel.objects.filter(valor__gte=preco_minimo)\
                    .filter(valor__lte=preco_maximo)\
                    .filter(tipo_imovel__in=tipo)\
                    .filter(tipo__in=tipo_venda)
            else: pass  
        else:
            if fav == 'true':
                if clicked > 0:
                    Imovel.favorito = True
                    imoveis = Imovel.objects.filter(valor__gte=preco_minimo)\
                    .filter(valor__lte=preco_maximo)\
                    .filter(tipo_imovel__in=tipo)\
                    .filter(cidade=cidade)\
                    .filter(tipo__in=tipo_venda)\
                    .filter(usuario=request.user)\
                    .filter(favorito__in=clicked)
                else:
                    imoveis = Imovel.objects.filter(valor__gte=preco_minimo)\
                    .filter(valor__lte=preco_maximo)\
                    .filter(tipo_imovel__in=tipo).filter(cidade=cidade)\
                    .filter(tipo__in=tipo_venda)
            else: pass
    else:
        imoveis = Imovel.objects.all()
    return render(request, 'home.html', {'imoveis': imoveis, 'cidades': cidades, 'clicked' : clicked})


def imovel(request, id):
    imovel = get_object_or_404(Imovel, id=id)
    sugestoes = Imovel.objects.filter(cidade=imovel.cidade).exclude(id=id)[:2]
    return render(request, 'imovel.html', {'imovel': imovel, 'sugestoes': sugestoes, 'id': id, 'clicked' : clicked})

def agendar_visitas(request):
    usuario = request.user
    dia = request.POST.get('dia')
    horario = request.POST.get('horario')
    id_imovel = request.POST.greet('id_imovel')

    visita = Visitas(
        imovel_id=id_imovel,
        usuario=usuario,
        dia=dia,
        horario=horario
    )
    visita.save()
    return redirect('/agendamentos')

def agendamentos(request):
    visitas = Visitas.objects.filter(usuario=request.user)
    return render(request, "agendamentos.html", {'visitas': visitas})

def cancelar_agendamento(request, id):
    visitas = get_object_or_404(Visitas, id=id)
    visitas.status = "C"
    visitas.save()
    return redirect('/agendamentos')



