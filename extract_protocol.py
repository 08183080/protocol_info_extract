'''
ftp: https://github.com/hfiref0x/LightFTP                                         ---
ftp: https://sourceforge.net/projects/bftpd/files/bftpd/bftpd-6.1/bftpd-6.1.tar.gz
ftp: https://github.com/proftpd/proftpd                                           ---  
ftp: https://github.com/jedisct1/pure-ftpd
rtsp: https://github.com/rgaufman/live555                                         ---
smtp: https://github.com/Exim/exim                                                ---
http: https://git.lighttpd.net/lighttpd/lighttpd1.4.git
'''
import os
import re
import base64
from openai import OpenAI
import markdown2
import requests
from zhipuai import ZhipuAI
from bs4 import BeautifulSoup

def get_info(url):
    # 正则表达式解析GitHub URL
    pattern = r'https://github\.com/([^/]+)/([^/]+)'
    match = re.match(pattern, url)
    
    if not match:
        raise ValueError("Invalid GitHub URL")
    
    username, repo = match.groups()
    return username, repo

def get_readme(username, repo):
    # GitHub API的URL
    url = f'https://api.github.com/repos/{username}/{repo}/readme'

    # 需要提供GitHub API token（如果有的话）
    headers = {
        'Authorization': "token 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"
    }

    # 发送请求
    response = requests.get(url, headers=headers)

    # 如果请求成功，返回README内容
    if response.status_code == 200:
        readme_data = response.json()
        readme_content = readme_data['content']
        # print(f"README (base64 encoded):\n{readme_content}")
    else:
        print(f"Error: {response.status_code}")

    decoded_content = base64.b64decode(readme_content).decode('utf-8')
    # print(f"Decoded README:\n{decoded_content}")
    return decoded_content
    
def get_project_intro(project):
    # client = OpenAI(api_key=os.getenv('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")
    client = OpenAI(api_key='40a2864c1e8de6bc3a04f71233e9be1d.hxTESOZdAuxChRNi', base_url="https://open.bigmodel.cn/api/paas/v4/")

    # deepseek-chat
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[
            {"role": "system", "content": " Please extract the following key information from the provided README document about the network protocol (e.g., live555):\
                                            Protocol Version: Identify and list the protocol version or versions mentioned.\
                                            Protocol Implementation Method: Describe the implementation method or approach used for the protocol.\
                                            Protocol Features: Highlight the unique or notable features of the protocol as mentioned in the document.\
                                            Other Infomatin: Other information that can describe the protocol implementation that can help my protocol fuzzing.\
                                            Ensure the extracted details are clear, concise, and listed as bullet points."},
            {"role": "user", "content": project},
        ],
        stream=False
    )
    ans = response.choices[0].message.content
    ans = markdown2.markdown(ans, extras=["strip"])
    soup = BeautifulSoup(ans, 'html.parser')
    text = soup.get_text()
    return text



def get_protocol_info(github_url):
    # github_url = 'https://github.com/Exim/exim' #'https://github.com/hfiref0x/LightFTP'
    username, repo = get_info(github_url)
    readme_content = get_readme(username, repo)
    project_intro = get_project_intro(readme_content)
    return project_intro
    # print(project_intro)

if __name__ == "__main__":
    urls = ['https://github.com/hfiref0x/LightFTP', 'https://github.com/proftpd/proftpd',
            'https://github.com/rgaufman/live555', 'https://github.com/Exim/exim']
    
    for url in urls:
        print(get_protocol_info(url))