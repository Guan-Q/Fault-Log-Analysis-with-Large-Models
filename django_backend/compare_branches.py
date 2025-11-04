#!/usr/bin/env python3
"""
对比两个分支的文件，找出差异
"""
import os
import sys

# Windows路径映射到WSL路径
WINDOWS_BASE = "/mnt/c/Users/Dell/Desktop"
BRANCH_MAIN = f"{WINDOWS_BASE}/Fault-Log-Analysis-with-Large-Models-main"
BRANCH_MASTER = f"{WINDOWS_BASE}/Fault-Log-Analysis-with-Large-Models-master"

LOCAL_BACKEND = "/home/wheatwine/django_backend"
LOCAL_FRONTEND = "/home/wheatwine/vue_frontend"

def check_file_exists(filepath):
    """检查文件是否存在"""
    return os.path.exists(filepath)

def read_file_content(filepath):
    """读取文件内容"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return None

# 需要对比的关键文件
BACKEND_FILES = [
    "deepseek_api/api.py",
    "deepseek_api/models.py",
    "deepseek_api/services.py",
    "deepseek_api/schemas.py",
]

FRONTEND_FILES = [
    "src/components/ChatMessage.vue",
    "src/components/MarkdownRenderer.vue",
    "package.json",
    "src/views/Chat.vue",
]

print("=" * 60)
print("分支文件对比工具")
print("=" * 60)
print()

print("检查master分支 (后端多轮对话):")
for file in BACKEND_FILES:
    master_file = f"{BRANCH_MASTER}/django_backend/{file}"
    local_file = f"{LOCAL_BACKEND}/{file}"
    
    master_exists = check_file_exists(master_file)
    local_exists = check_file_exists(local_file)
    
    print(f"\n文件: {file}")
    print(f"  Master分支: {'存在' if master_exists else '不存在'}")
    print(f"  本地文件: {'存在' if local_exists else '不存在'}")
    
    if master_exists and local_exists:
        master_content = read_file_content(master_file)
        local_content = read_file_content(local_file)
        if master_content and local_content:
            if master_content != local_content:
                print(f"  ⚠️ 内容不同，需要对比差异")
            else:
                print(f"  ✅ 内容相同")

print("\n" + "=" * 60)
print("检查main分支 (前端Markdown):")
for file in FRONTEND_FILES:
    main_file = f"{BRANCH_MAIN}/vue_frontend/{file}"
    local_file = f"{LOCAL_FRONTEND}/{file}"
    
    main_exists = check_file_exists(main_file)
    local_exists = check_file_exists(local_file)
    
    print(f"\n文件: {file}")
    print(f"  Main分支: {'存在' if main_exists else '不存在'}")
    print(f"  本地文件: {'存在' if local_exists else '不存在'}")
    
    if main_exists and local_exists:
        main_content = read_file_content(main_file)
        local_content = read_file_content(local_file)
        if main_content and local_content:
            if main_content != local_content:
                print(f"  ⚠️ 内容不同，需要对比差异")
            else:
                print(f"  ✅ 内容相同")

