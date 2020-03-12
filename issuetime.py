import requests
import os
import re
import json
import sys
import urllib3
import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#converte tempo de segundos p/ horas
def time_coverter(lbl_8h, lbl_6h, lbl_4h, lbl_2h, issue_link, assign, timespent, label, issue, headers, url): 
    second_per_hour=3600
    total = timespent/second_per_hour
    int(total)
    check_labels(lbl_8h, lbl_6h, lbl_4h, lbl_2h, issue_link, assign, label, total, issue, headers, url)

# checa o label da issue principal
def check_labels(lbl_8h, lbl_6h, lbl_4h, lbl_2h, issue_link, assign, label, total, issue, headers, url):
    for i in range(len(label)):
        if label[i] == 'suporte A' or label[i] == 'suporte B':
            calc_suporte(lbl_8h, lbl_6h, lbl_4h, lbl_2h, issue_link, assign, total, issue, headers, url)
        elif label[i] == 'prospecção A' or label[i] == 'prospecção B':
            calc_others(lbl_8h, lbl_4h, issue_link, assign, total, issue, headers, url)
        elif label[i] == 'formação A' or label[i] == 'formação B':
            calc_others(lbl_8h, lbl_4h, issue_link, assign, total, issue, headers, url)
        elif label[i] == 'treinamento A' or label[i] == 'treinamento B':
            calc_others(lbl_8h, lbl_4h, issue_link, assign, total, issue, headers, url)
        elif label[i] == 'manutenção A' or label[i] == 'manutenção B':
            calc_others(lbl_8h, lbl_4h, issue_link, assign, total, issue, headers, url)
        else:
            print('A Issue não possui labels compatíveis')

def calc_suporte(lbl_8h, lbl_6h, lbl_4h, lbl_2h, issue_link, assign, total, issue, headers, url):
    print('suporte: 2,4,6,8') #calcula a quantidade de issues que devem ser abertas se o label for suporte
    qtd2 = 0
    qtd4 = 0
    qtd6 = 0
    qtd8 = 0
    if total >= 8 or total == 7:
        qtd8 = int(total/8)
        sobra = total % 8
        qtd8 = round(qtd8)  # quantidade de issues de 8
        if sobra <= 8 and sobra >= 7 and sobra !=0:
            qtd8 = int(qtd8+1)
        elif sobra <= 6 and sobra >= 5 and sobra !=0:  # se for de 5 a 6
            qtd6 = int(qtd6+1)
        elif sobra <= 4 and sobra >= 3 and sobra !=0:  # se for de 3 a 4
            qtd4 = int(qtd4+1)
        elif sobra <= 2 and sobra >= 1 and sobra !=0:  # se for de 1 a 2
            qtd2 = int(qtd2+1)
    elif total < 8 and total >=6:
        qtd6 = int(total/6)  # quantidade de issues de 6
        sobra = total % 6
        if sobra <= 6 and sobra >= 5 and sobra !=0:
            qtd6 = int(qtd6+1)
        elif sobra <= 4 and sobra >= 3 and sobra !=0:  # se for de 3 a 4
            qtd4 = int(qtd4+1)
        elif sobra <= 2 and sobra >= 1 and sobra !=0:  # se for de 1 a 2
            qtd2 = int(qtd2+1)
    elif total < 6 and total >=4:
        qtd4 = int(total/4)  # quantidade de issues de 6
        sobra = total % 4
        if sobra <= 4 and sobra >= 3 and sobra !=0:  # se for de 3 a 4
            qtd4 = int(qtd4+1)
        elif sobra <= 2 and sobra >= 1 and sobra !=0:  # se for de 1 a 2
            qtd2 = int(qtd2+1)
    elif total < 4 and total >=2:
        qtd2 = int(total/2)  # quantidade de issues de 6
        sobra = total % 2
        if sobra <= 2 and sobra >= 1 and sobra !=0:  # se for de 3 a 4
            qtd2 = int(qtd2+1)
    elif total < 2 and total != 0:
        qtd2 = int(qtd2+1)        
    new_issue_suporte(lbl_8h, lbl_6h, lbl_4h, lbl_2h, issue_link, assign, qtd8, qtd6, qtd4, qtd2, issue, headers, url)

#calcula a quantidade de issues que devem ser abertas
def calc_others(lbl_8h, lbl_4h, issue_link, assign, total, issue, headers, url):
    qtd4 = 0
    qtd8 = 0
    print('others: 4,8') 
    if total >= 8:
        qtd8 = total/8
        sobra = total % 8
        qtd8 = round(qtd8)
        if sobra <= 8 and sobra >= 7 and sobra !=0:
            qtd8 = qtd8+1
        elif sobra <= 4 and sobra <= 3 and sobra !=0:
            qtd4 = qtd4+1
    elif total < 8 and total >= 4:
        qtd4 = total/4
        sobra = total % 4
        qtd4 = round(qtd4)
        if sobra <=4 and sobra !=0:
            qtd4 = qtd4+1
        print(qtd4)
    elif total < 4 and total !=0:
        qtd4 = qtd4+1
    new_issue_others(lbl_8h, lbl_4h, issue_link, assign, qtd8, qtd4, issue, headers, url)

def new_issue_others(lbl_8h, lbl_4h, issue_link, assign, qtd8, qtd4, issue, headers, url):
    name = issue['title'] #pega titulo da issue
    for j in range(len(assign)):
        assignee = assign[j] #pega os assigns
        for i in range(qtd8):
            eight = '{}?title={}&assignee_ids={}&description={}&labels={}' .format(
                url, name, assignee, issue_link, lbl_8h)
            ne = requests.post(eight, headers=headers, verify=False)
        if qtd4 != 0:
            for k in range(qtd4):
                four = '{}?title={}&assignee_ids={}&description={}&labels={}' .format(
                    url, name, assignee, issue_link, lbl_4h)
                nf = requests.post(four, headers=headers, verify=False)

def new_issue_suporte(lbl_8h, lbl_6h, lbl_4h, lbl_2h, issue_link, assign, qtd8, qtd6, qtd4, qtd2, issue, headers, url):
    name = issue['title'] 
    for j in range(len(assign)):
        assignee = assign[j]
        for i in range(qtd8):
            eight = '{}?title={}&assignee_ids={}&description={}&labels={}' .format(url, name, assignee, issue_link, lbl_8h)
            ne = requests.post(eight, headers=headers, verify=False)
        if qtd6 != 0:
            for j in range(qtd6):
                six = '{}?title={}&assignee_ids={}&description={}&labels={}' .format(
                    url, name, assignee, issue_link, lbl_6h)
                ns = requests.post(six, headers=headers, verify=False)
        elif qtd4 != 0:
            for k in range(qtd4):
                four = '{}?title={}&assignee_ids={}&description={}&labels={}' .format(
                    url, name, assignee, issue_link, lbl_4h)
                nf = requests.post(four, headers=headers, verify=False)
        elif qtd2 != 0:
            for l in range(qtd2):
                two = '{}?title={}&assignee_ids={}&description={}&labels={}' .format(
                    url, name, assignee, issue_link, lbl_2h)
                nt = requests.post(two, headers=headers, verify=False)

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

    assign = []  # array de assignees

    try:
        assignees = issue['assignee']['id']  # pega o id do assignee
        assign.append(assignees)
    except:
        print('A issue não possui nenhum assignee.')
        exit()

    for i in nts:
        if "!assign" in i['body']:
            b = str(i['body'])  # transforma conteudo do body em string
            b2 = b.split('@')[1]  # corta string até o @ do CPF
            user = 'https://git.serpro/api/v4/projects/{}/users?username={}' .format(
                p, b2)
            uid = requests.get(user, headers=headers, verify=False)
            us = uid.json()
            user_id = us[0]['id']  # pega o id do usuário
            if user_id not in assign:  # verifica se cpf já existe no array
                assign.append(user_id)

    issue_link = issue['_links']['self']

    label = issue['labels'] #pega labels da issue

    if not label:
        print('A issue não possui labels.')

    # pega o tempo gasto
    timespent = int(issue['time_stats']['total_time_spent'])
    if timespent <= 0:
        print('A issue não possui time spent.')
    else:
        time_coverter(lbl_8h, lbl_6h, lbl_4h, lbl_2h, issue_link, assign, timespent, label, issue, headers, url)