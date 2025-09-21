import requests
import time
import hashlib
import json
import re
import subprocess

def calculate_signature(params, ts, user_id):
    """计算签名：将 params、ts、user_id 的值拼接后计算 MD5"""
    # 注意：params 已经是字符串形式的 JSON
    sign_str = f"wJxaspn8Arv4HRkjVd7eSU5gfGYumhyqparams{params}ts{ts}user_id6d32b18e90fe11eea60b5254001e7c00"
    return hashlib.md5(sign_str.encode()).hexdigest()

def fetch_api_data():
    # 获取当前时间戳
    current_ts = int(time.time())
    print(f"当前时间戳: {current_ts}")

    # API 配置
    api_url = "https://afdian.com/api/open/query-order"
    user_id = "6d32b18e90fe11eea60b5254001e7c00"
    params_str = '{"page":1}'  # 字符串形式的 JSON

    # 计算签名
    signature = calculate_signature(params_str, current_ts, user_id)
    print(f"计算出的签名: {signature}")

    # 构建请求体
    payload = {
        "user_id": user_id,
        "params": params_str,
        "ts": current_ts,
        "sign": signature
    }

    # 发送请求
    headers = {"Content-Type": "application/json"}
    print(f"发送请求到: {api_url}")
    print(f"请求体: {json.dumps(payload, indent=2)}")

    response = requests.post(api_url, headers=headers, data=json.dumps(payload), timeout=10)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API请求失败: {response.status_code} - {response.text}")

def update_readme(data):
    # 创建要插入的内容
    data_content = "无数据"
    if data.get("ec") == 200:
        data_content = str(data.get('data', {}).get('total_count', 0))

    # 处理 README.md
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()

        pattern = r'https://img\.shields\.io/badge/a-.*?-c\?style=for-the-badge&label=爱发电&labelColor=%239469e3&color=%23B291F0'
        replacement = f'https://img.shields.io/badge/a-{data_content}-c?style=for-the-badge&label=爱发电&labelColor=%239469e3&color=%23B291F0'
        updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(updated_content)
    except FileNotFoundError:
        print("README.md 文件未找到")

    # 处理 README.En.md
    try:
        with open('README.En.md', 'r', encoding='utf-8') as f:
            content = f.read()

        pattern = r'https://img\.shields\.io/badge/a-.*?-c\?style=for-the-badge&label=Afdian&labelColor=%239469e3&color=%23B291F0'
        replacement = f'https://img.shields.io/badge/a-{data_content}-c?style=for-the-badge&label=Afdian&labelColor=%239469e3&color=%23B291F0'
        updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        with open('README.En.md', 'w', encoding='utf-8') as f:
            f.write(updated_content)
    except FileNotFoundError:
        print("README.En.md 文件未找到")

def commit_and_push():
    try:
        # 添加文件到暂存区
        subprocess.run(['git', 'add', 'README.md', 'README.En.md'], check=True)
        
        # 提交更改
        subprocess.run(['git', 'commit', '-m', 'Update API data in README'], check=True)
        
        # 推送到远程仓库
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("成功提交并推送更改")
    except subprocess.CalledProcessError as e:
        print(f"Git操作失败: {e}")

if __name__ == "__main__":
    try:
        print("开始获取API数据...")
        data = fetch_api_data()
        print("API响应:", json.dumps(data, indent=2, ensure_ascii=False))
        update_readme(data)
        commit_and_push()
        print("README更新成功")
    except Exception as e:
        print(f"错误: {e}")
