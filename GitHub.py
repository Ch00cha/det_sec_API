def github_scan_rep(repository_path):
    headers = {}
    check = {}
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
    data = r.json()
    if file_path != '' and data['type']=='file':
        content = data['content']
        name = data['name']
        encoding = data['encoding']
        if encoding == 'base64':
            content = base64.b64decode(content).decode()
        names.append(name)
        contents.append(content)
    else:
        for each_file in data:
            if each_file['type']=='file':
                name = each_file['name']
                each_file = requests.get(str(each_file['url']), headers = headers).json()
                content = each_file['content']
                encoding = each_file['encoding']
                if encoding == 'base64':
                    content = base64.b64decode(content).decode()
                names.append(name)
                contents.append(content)
    check.update({'name': names, 'content': contents})
    return json.dumps(check)


# # from github import Github

# # g = Github()

# # repo = g.get_repo("Ch00cha/det_sec_API")
# # contents = repo.get_contents("")
# # for content in contents:
# #     print(content)
# #     content()

# import base64
# import json
# import requests
# import os


# def github_read_file(username, repository_name, file_path):
#     headers = {}      
#     url = f'https://api.github.com/repos/{username}/{repository_name}/contents/{file_path}'
#     r = requests.get(url, headers=headers)
#     # r.raise_for_status()
#     data = r.json()
#     file_content = data['content']
#     file_content_encoding = data.get('encoding')
#     if file_content_encoding == 'base64':
#         file_content = base64.b64decode(file_content).decode()

#     return file_content


# def main():
#     username = 'Ch00cha'
#     repository_name = 'det_sec_API'
#     file_path = 'main.py'
#     file_content = github_read_file(username, repository_name, file_path)
#     # data = json.loads(file_content)
#     print(file_content)


# if __name__ == '__main__':
#     main()

# headers = {}      
# url = 'https://api.github.com/repos/Ch00cha/det_sec_API/contents'
# username = 'Ch00cha'
# repository_name = 'det_sec_API'
# r = requests.get(url, headers=headers)
# data = r.json()
# for i in range(len(data)):
#     if data[i]['type'] == "file":
#         github_read_file(username, repository_name, data[i]['type']):
        
# print(len(data))
