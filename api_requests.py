import requests
import json

def read_ip():
    file = open("/tmp/myipnow.txt", "r")
    ip = file.read().rstrip("\n")
    return ip

def github_scan_rep(repository_path):
    headers = {}
    check = []
    names = []
    contents = []
    get_username = repository_path.split('/')[3]
    get_repository_name = repository_path.split('/')[4]
    file_path = ''
    if len(repository_path.split('/')) > 5:
        get_path = repository_path.split('/')[7:]
        for i in get_path:
            file_path += i + '/'
    url = f'https://api.github.com/repos/{get_username}/{get_repository_name}/contents/{file_path}'
    r = requests.get(url, headers=headers)
    if str(r) == '<Response [403]>':
        return 'Превышено количество запросов'
    elif str(r) == '<Response [404]>':
        return 'Неверный url, либо репозиторий является приватным'
    else:
        data = r.json()
        if file_path != '' and data['type']=='file':
            name = data['name']
            content = data['content']
            check.append({'name':name, 'content': content})
        else:
            for each_file in data:
                if each_file['type']=='file':
                    name = each_file['name']
                    each_file = requests.get(str(each_file['url']), headers = headers).json()
                    content = each_file['content']
                    check.append({'name':name, 'content': content})
        return check


def request_to_det_sec_API(url):
    data = github_scan_rep(url)
    data = {"accept": data}
    ip = read_ip()
    r = requests.post(f'http://{ip}:8000/predict',  data = json.dumps(data)).json()
    return r
