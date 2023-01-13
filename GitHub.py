import requests
import json
import base64


def github_scan_rep(repository_path, file_path = ''):
    headers = {}
    check = {}
    url = f'https://api.github.com/repos/{repository_path}/contents/{file_path}'
    r = requests.get(url, headers=headers)
    data = r.json()
    if file_path != '' and data['type']=='file':
        file_content = data['content']
        name = data['name']
        file_content_encoding = data.get('encoding')
        if file_content_encoding == 'base64':
            file_content = base64.b64decode(file_content).decode()
            check.update({name: file_content})
    else:
        for each_file in data:
            if each_file['type']=='file':
                name = each_file['name']
                each_file = requests.get(str(each_file['url']), headers = headers).json()
                content = each_file['content']
                encoding = each_file['encoding']
                if encoding == 'base64':
                    content = base64.b64decode(content).decode()
                    check.update({name: content})
    return check


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
