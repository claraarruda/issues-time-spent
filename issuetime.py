import requests
import os
import re
import json
import sys
import urllib3
import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_assign(nts):
    assign=[]
    for i in nts:
        if "!assign" in i['body']:
            b = str(i['body']) #transforma conteudo do body em string
            b2 = b.split('@')[1] #corta string até o @ do CPF
            if b2 not in assign: #verifica se cpf já existe no array
                assign.append(b2)
    print(assign)

def time_coverter(timespent, label, issue, headers, url): #apenas days
    hours_per_day = int(8)  # transformando, 1 dia = 8 horas (jornada trabalho)
    s = str(timespent)  # transformando em string para partir
    h = s.split("d ")[1]  # partindo string
    day = int(s.split("d ")[0])  # dias passados + partição
    hour = int(h.split("h")[0])  # horas passadas + partição
    hours = (day * hours_per_day)  # conversão
    total = (hours + hour)  # total de horas
    print(total)
    check_labels(label, total, issue, headers, url)


def time_coverter2(timespent, label, issue, headers, url): #se tiver week 
    days_per_week = int(5)  # transformando, 1 semana = 5 dias (dias úteis)
    hours_per_day = int(8)  # transformando, 1 dia = 8 horas (jornada trabalho)
    s = str(timespent)  # transformando em string para partir
    d = s.split('w ')[1]  # separando semanas de dias+horas
    h = d.split('d ')[1]  # separando dias de horas
    hour = int(h.split('h')[0])  # removendo 'h' e transformando em inteiro
    day = int(d.split('d')[0])  # removendo 'd' e transformando em inteiro
    week = int(s.split('w')[0])  # removendo 'w' e transformando em inteiro
    days = (week * days_per_week)  # Conversão dias por semana
    total_days = day + days  # dias no total
    hours = (total_days * hours_per_day)  # conversão horas por dia
    total = hours + hour  # somando, resultado = total horas
    print('total hrs: {}' .format(total))
    check_labels(label, total, issue, headers, url)


def check_labels(label, total, issue, headers, url):
    if label == 'suporte A' or label == 'suporte B':
        print('igual {}' .format(label))
        calc_suporte(total, issue, headers, url)
    elif label == 'prospecção A' or label == 'prospecção B':
        print('igual {}' .format(label))
        calc_others(total, issue, headers, url)
    elif label == 'formação A' or label == 'formação B':
        print('igual {}' .format(label))
        calc_others(total, issue, headers, url)
    elif label == 'treinamento A' or label == 'treinamento B':
        print('igual {}' .format(label))
        calc_others(total, issue, headers, url)
    elif label == 'manutenção A' or label == 'manutenção B':
        print('igual {}' .format(label))
        calc_others(total, issue, headers, url)
    else:
        print('issue sem labels')


def calc_suporte(total, issue, headers, url):
    print('suporte: 2,4,6,8')
    qtd2 = 0
    qtd4 = 0
    qtd6 = 0
    qtd8 = 0
    if total >= 8 or total == 7:
        qtd8 = total/8
        sobra = total % 8
        qtd8 = round(qtd8)
        print(qtd8)  # quantidade de issues de 8
        print(sobra)
        if sobra <= 8 and sobra >= 7:
            print('8/7 de sobra')
            qtd8 = qtd8+1
        elif sobra <= 6 and sobra >= 5:  # se for de 5 a 6
            print('6/5 de sobra')
            qtd6 = qtd6+1
        elif sobra <= 4 and sobra >= 3:  # se for de 3 a 4
            print('4/3 de sobra')
            qtd4 = qtd4+1
        elif sobra <= 2 and sobra >= 1:  # se for de 1 a 2
            print('2/1 de sobra')
            qtd2 = qtd2+1
    elif total < 8 and total > 7:
        qtd6 = total/6
        sobra = total % 6
        print(qtd6)
        print(sobra)
        if sobra <= 6 and sobra >= 5:
            print('6/5 de sobra')
            qtd6 = qtd6+1
        elif sobra <= 4 and sobra >= 3:  # se for de 3 a 4
            print('4/3 de sobra')
            qtd4 = qtd4+1
        elif sobra <= 2 and sobra >= 1:  # se for de 1 a 2
            print('2/1 de sobra')
            qtd2 = qtd2+1
    new_issue_suporte(qtd8, qtd6, qtd4, qtd2, issue, headers, url)


def calc_others(total, issue, headers, url):
    qtd4 = 0
    qtd8 = 0
    print('others: 4,8')
    if total >= 8:
        qtd8 = total/8
        sobra = total % 8
        qtd8 = round(qtd8)
        print(qtd8)
        print(sobra)
        if sobra <= 8 and sobra >= 7:
            print('8/7 de sobra')
            qtd8 = qtd8+1
        elif sobra <= 4 and sobra <= 3:
            print('4/3 de sobra')
            qtd4 = qtd4+1
    new_issue_others(qtd8, qtd4, issue, headers, url)


def new_issue_others(qtd8, qtd4, issue, headers, url):
    name = issue['title']
    print(name)
    for i in range(qtd8):
        eight = url+'?title={}&labels=8h' .format(name)
        ne = requests.post(eight, headers=headers, verify=False)
        print(ne.status_code)
    if qtd4 != 0:
        for k in range(qtd4):
            four = url+'?title={}&labels=4h' .format(name)
            nf = requests.post(four, headers=headers, verify=False)
            print(nf.status_code)
    
def new_issue_suporte(qtd8, qtd6, qtd4, qtd2, issue, headers, url):
    name = issue['title']
    print(name)
    for i in range(qtd8):
        eight = url+'?title={}&labels=8h' .format(name)
        ne = requests.post(eight, headers=headers, verify=False)
        print(ne.status_code)
    if qtd6 != 0:
        for j in range(qtd6):
            six = url+'?title={}&labels=6h' .format(name)
            ns = requests.post(six, headers=headers, verify=False)
            print(ns.status_code)
    elif qtd4 != 0:
        for k in range(qtd4):
            four = url+'?title={}&labels=4h' .format(name)
            nf = requests.post(four, headers=headers, verify=False)
            print(nf.status_code)
    elif qtd2 != 0:
        for l in range(qtd2):
            two = url+'?title={}&labels=2h' .format(name)
            nt = requests.post(two, headers=headers, verify=False)
            print(nt.status_code)

if __name__ == "__main__":
    # variavel de ambiente para token privado de acesso
    t = os.environ.get('TOKEN')
    p = os.environ.get('PROJ')  # variavel de ambiente para projeto
    i = os.environ.get('ISSUE')  # variavel de ambiente para id da issue
    lbl_8h = os.environ.get('OITO')  # variavel de ambiente para o label 8h
    lbl_6h = os.environ.get('SEIS')  # variavel de ambiente para o label 6h
    lbl_4h = os.environ.get('QUATRO')  # variavel de ambiente para o label 4h
    lbl_2h = os.environ.get('DOIS')  # variavel de ambiente para o label 2h

    try:
        os.environ['PROJ']
    except KeyError:
        print('A variável de ambiente PROJ não foi definida.')
        sys.exit(1)    
    try:
        os.environ['ISSUE']
    except KeyError:
        print('A variável de ambiente ISSUE não foi definida.')
        sys.exit(1)        
    try:
        os.environ['TOKEN']
    except KeyError:
        print('A variável de ambiente TOKEN não foi definida.')
        sys.exit(1)   
    try:
        os.environ['OITO']
    except KeyError:
        print('A variável de ambiente OITO não foi definida.')
        sys.exit(1)     
    try:
        os.environ['SEIS']
    except KeyError:
        print('A variável de ambiente SEIS não foi definida.')
        sys.exit(1)    
    try:
        os.environ['QUATRO']
    except KeyError:
        print('A variável de ambiente QUATRO não foi definida.')
        sys.exit(1)    
    try:
        os.environ['DOIS']
    except KeyError:
        print('A variável de ambiente DOIS não foi definida.')
        sys.exit(1)    

    print('O projeto selecionado: {}' .format(p))
    print('O token utilizado: {}' .format(t))
    print('A issue selecionada: {}' .format(i))

    headers = {'PRIVATE-TOKEN': t}
    url = 'https://git.serpro/api/v4/projects/{}/issues' .format(p)
    iurl = '{}/{}' .format(url, i)

    ar = requests.get(iurl, headers=headers, verify=False)
    issue = ar.json()

    notes = issue['_links']['notes']
    r = requests.get(notes, headers=headers, verify=False)
    nts = r.json()

    assign=[] #array de assignees

    assignees = issue['assignee']['id'] #pega o id do assignee
    assign.append(assignees) 
    for i in nts:
        if "!assign" in i['body']:
            b = str(i['body']) #transforma conteudo do body em string
            b2 = b.split('@')[1] #corta string até o @ do CPF
            user = 'https://git.serpro/api/v4/projects/{}/users?username={}' .format(p, b2)
            uid = requests.get(user, headers=headers, verify=False)
            us = uid.json()
            user_id = us[0]['id'] #pega o id do usuário
            if user_id not in assign: #verifica se cpf já existe no array
                assign.append(user_id)

    l1 = str(issue['labels'])

    label = l1.strip("'[]'")
    print(label)
    timespent = issue['time_stats']['human_total_time_spent'] #pega o tempo gasto
    print(timespent)
    timespent = str(timespent)
    if timespent.find('w') == True:
        time_coverter2(timespent, label, issue, headers, url)
    else:
        time_coverter(timespent, label, issue, headers, url)