#Importação de bibliotecas:
#------------------------------------------>
from pyzabbix import ZabbixAPI
import json
import socket
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
#------------------------------------------>

#Configuração da conexão com a API do Zabbix:
zabbix = ZabbixAPI("https://localhost/zabbix")
zabbix.login("User", "Password")

#Obtenção de informações dos hosts cadastrados no Zabbix:
hosts = []
for host in zabbix.host.get(selectInterfaces=['ip'], selectStatus=['status'], selectGroups=['name']):
    hosts.append(host)

#Criação de uma lista de hosts com seus respectivos endereços IP:
with ThreadPoolExecutor() as executor:
    ips = executor.map(lambda x: socket.gethostbyname(x['interfaces'][0]['ip']), hosts)

#Obtenção dos endereços IP de forma assíncrona:
for host, ip in zip(hosts, ips):
    host['ip'] = ip
    #Atribuição dos endereços IP aos hosts:
    group = host['groups'][0]['name']
    host['group'] = group

#Inclusão do nome do grupo ao qual o host pertence na lista de informações:
hosts_json = json.dumps(hosts, indent=4)

#Conversão da lista de informações em JSON:
hosts_df = pd.DataFrame(hosts, columns=['name', 'ip', 'status', 'group'])

#Conversão da lista de informações em um DataFrame:
hosts_df.to_csv('hosts.csv', index=False)

#Por fim, o arquivo é exportado para o diretório do projeto como hosts.csv
