#!/usr/bin/env python3
"""修复 package-lock.json 的合并冲突，保留 HEAD 版本"""

import re

file_path = '../vue_frontend/package-lock.json'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

result_lines = []
in_head_block = False
in_origin_block = False

for i, line in enumerate(lines):
    if line.startswith('<<<<<<< HEAD'):
        in_head_block = True
        continue
    elif line.startswith('======='):
        in_head_block = False
        in_origin_block = True
        continue
    elif line.startswith('>>>>>>> origin/prompt'):
        in_origin_block = False
        continue
    
    if in_head_block:
        result_lines.append(line)
    elif not in_origin_block:
        result_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(result_lines)

print(f"已修复 {file_path} 的冲突，删除了 {len(lines) - len(result_lines)} 行冲突标记")

