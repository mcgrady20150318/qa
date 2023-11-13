import requests
import json 
import time
import argparse
from rich import print

parser = argparse.ArgumentParser(description='请传入arxiv id，开始问答')
parser.add_argument('--id', type=str, help='arxiv id')
args = parser.parse_args()

domain = 'http://106.75.61.87:5000/'

def upload(id):
    url = domain+'upload'
    data = json.dumps({'id':id})
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url=url, data = data, headers=headers)
    return response.text

def qa(id,question):
    url = domain+'qa'
    data = json.dumps({'id': id,'question':question})
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url=url, data = data, headers=headers, stream=True)
    pre = b''
    for chunk in response.iter_content(chunk_size=2):
        if chunk:
            pre += chunk
            try:
                print('[bold magenta]'+pre.decode('utf-8')+'[/bold magenta]',end='',flush=True)
                pre = b''
                time.sleep(0.1)
            except:
                pass

id = args.id
print('[bold magenta]...正在解析...[/bold magenta]')
res = upload(id)
if res == 'done':
    print('[bold magenta]解析成功，请开始问答[/bold magenta]')
    while True:
        question = input('Q:')
        qa(id,question)
        print('\n')
else:
    print('[bold magenta]解析失败[/bold magenta]')
    

