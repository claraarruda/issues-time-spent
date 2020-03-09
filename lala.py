import requests
import os
import re
import json
import sys
import urllib3
import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# variavel de ambiente para token privado de acesso
t = os.environ.get('TOKEN')
p = os.environ.get('PROJ')  # variavel de ambiente para projeto
i = os.environ.get('ISSUE')  # variavel de ambiente para id da issue
print('O projeto selecionado: {}' .format(p))
print('O token utilizado: {}' .format(t))
print('A issue selecionada: {}' .format(i))

headers = {'PRIVATE-TOKEN': t}

url = 'https://git.serpro/api/v4/projects/{}/issues/{}'.format(p, i)
iurl = '{}/{}/notes' .format(url, i)


ar = requests.get(url, headers=headers, verify=False)
issue = ar.json()
# print(issue)

notes = issue['_links']['notes']
r = requests.get(notes, headers=headers, verify=False)
nts = r.json()
array=[]
for i in nts:
    if "!assign" in i['body']:
        b = str(i['body']) #transforma conteudo do body em string
        b2 = b.split('@')[1] #corta string até o @ do CPF
        if b2 not in array:
            array.append(b2)
print(array)