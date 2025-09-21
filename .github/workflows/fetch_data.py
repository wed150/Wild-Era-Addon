import os

import requests
import time
import hashlib
import json
import re

def calculate_signature(token,params, ts, user_id):
    """计算签名：将 params、ts、user_id 的值拼接后计算 MD5"""
    # 注意：params 已经是字符串形式的 JSON

    sign_str = f"{token}params{params}ts{ts}user_id{user_id}"
    return hashlib.md5(sign_str.encode()).hexdigest()

def fetch_api_data(user_id,token):
    # 获取当前时间戳
    current_ts = int(time.time())
    print(f"当前时间戳: {current_ts}")

    # API 配置
    api_url = "https://afdian.com/api/open/query-order"
    params_str = '{"page":1}'  # 字符串形式的 JSON
    # 计算签名
    signature = calculate_signature(token,params_str, current_ts, user_id)

    # 构建请求体
    payload = {
        "user_id": user_id,
        "params": params_str,
        "ts": current_ts,
        "sign": signature
    }

    # 发送请求
    headers = {"Content-Type": "application/json"}

    response = requests.post(api_url, headers=headers, data=json.dumps(payload), timeout=10)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API请求失败")

def process_data(data):
    """处理从API获取的数据，提取用于徽章显示的内容"""
    data_content = "无数据"
    if data.get("ec") == 200:
        total_count = data.get('data', {}).get('total_count', 0)
        data_content = int(total_count)
    return data_content

def update_readme_file(file_path, pattern, replacement):
    """更新单个README文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
    except FileNotFoundError:
        print(f"{file_path} 文件未找到")

def update_readme(data_content):
    """更新README文件中的徽章数据"""
    # 处理 README.md
    pattern = r'https://img\.shields\.io/badge/a-.*?-c\?style=for-the-badge&label=爱发电&labelColor=%239469e3&color=%23B291F0'
    replacement = f'https://img.shields.io/badge/a-{data_content}-c?style=for-the-badge&label=爱发电&labelColor=%239469e3&color=%23B291F0'
    update_readme_file('README.md', pattern, replacement)

    # 处理 README.En.md
    pattern = r'https://img\.shields\.io/badge/a-.*?-c\?style=for-the-badge&label=Afdian&labelColor=%239469e3&color=%23B291F0'
    replacement = f'https://img.shields.io/badge/a-{data_content}-c?style=for-the-badge&label=Afdian&labelColor=%239469e3&color=%23B291F0'
    update_readme_file('README.En.md', pattern, replacement)


if __name__ == "__main__":
    try:
        secret_key =json.loads( os.environ.get("TOKEN", 'o'))

        if secret_key =="o":
            raise Exception("TOKEN 未设置")
        data_content=0
        for i in secret_key:
            data = fetch_api_data(i["user_id"],i["token"])
            data_content += process_data(data)


        # 分离数据处理和文件更新

        update_readme(str(data_content))
    except Exception as e:
        print(f"错误"+str(e))


