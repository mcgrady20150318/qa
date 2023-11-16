import requests
import json 
import time
import argparse
from rich import print
import PyPDF2
import hashlib
import os

parser = argparse.ArgumentParser(description='请传入arxiv id或者本地pdf，开始问答')
parser.add_argument('--id', type=str, default='2310.11511', help='arxiv id')
parser.add_argument('--pdf', type=str, help='本地pdf位置')
args = parser.parse_args()

server = 'http://106.75.61.87:5000'
pdf_path = ''
pdf_hash = ''
paper = ''

def get_hash(id):
    md5 = hashlib.md5()
    md5.update(id.encode('utf-8'))
    return md5.hexdigest()

def get_pdf_content(pdf_path):
    paper = ""
    f = open(pdf_path,'rb')
    reader = PyPDF2.PdfReader(f)
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        paper += page.extract_text()
    return paper

def check_file(pdf_path):
    if os.path.exists(pdf_path):
        return True
    else:
        return False

def get_pdf(args):
    print('[bold magenta]...pdf正在解析...[/bold magenta]')
    if args.pdf:
        pdf_path = args.pdf
        assert check_file(pdf_path), "pdf文件不存在"
        key = get_hash(pdf_path)
    else:
        id = args.id
        pdf_path = './' + id + '.pdf'
        if not check_file(pdf_path):
            url = 'https://arxiv.org/pdf/'+id+'.pdf'
            try:
                response = requests.get(url)
            except:
                print('[bold magenta]...pdf下载失败...[/bold magenta]')
            with open(pdf_path, 'wb') as file:
                file.write(response.content)
        key = get_hash(id)        
    paper = get_pdf_content(pdf_path)
    print('[bold magenta]...pdf解析完毕...[/bold magenta]')
    return key,paper
    
def upload(key,paper):
    url = server+'/upload'
    data = json.dumps({'key':key,"paper":paper})
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url=url, data = data, headers=headers)
    return response.text

def qa(key,question):
    url = server+'/qa'
    data = json.dumps({'key': key,'question':question})
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url=url, data = data, headers=headers, stream=True)
    pre = b''
    for chunk in response.iter_content(chunk_size=2):
        if chunk:
            pre += chunk
            try:
                print('[bold blue]'+pre.decode('utf-8')+'[/bold blue]',end='',flush=True)
                pre = b''
                time.sleep(0.1)
            except:
                pass

key,paper = get_pdf(args)
res = upload(key,paper)
if res == 'done':
    print('[bold red]上传成功，请开始问答[/bold red]')
    while True:
        question = input('Q:')
        if question == 'quit' or question == 'exit':
            break
        qa(key,question)
        print('\n')
else:
    print('[bold red]上传失败[/bold red]')