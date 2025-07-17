import os
import sys
import requests

GH_MIRROR = os.getenv("GH_MIRROR")
PACKAGES_DIR = "packages"

# 从环境变量中获取 URL 列表
JSON_URLS_RAW = os.getenv("JSON_URLS", "")
JSON_URLS = [url.strip() for url in JSON_URLS_RAW.splitlines() if url.strip()]

def replace_github_url(content):
    return content.replace("https://github.com/", f"{GH_MIRROR}/https://github.com/")

def main():
    if not GH_MIRROR:
        print("Error: GH_MIRROR 环境变量未设置")
        sys.exit(1)

    if not os.path.exists(PACKAGES_DIR):
        os.makedirs(PACKAGES_DIR)

    if not JSON_URLS:
        print("Error: 未提供 JSON URL 列表")
        sys.exit(1)

    for url in JSON_URLS:
        try:
            print(f"正在下载: {url}")
            response = requests.get(url)
            response.raise_for_status()

            content = response.text
            updated_content = replace_github_url(content)

            filename = os.path.join(PACKAGES_DIR, os.path.basename(url))
            with open(filename, "w", encoding="utf-8") as f:
                f.write(updated_content)

            print(f"已保存处理后的文件: {filename}")

        except Exception as e:
            print(f"处理 {url} 出错: {e}")
            continue

if __name__ == "__main__":
    main()