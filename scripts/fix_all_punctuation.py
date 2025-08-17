#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os

def fix_all_punctuation():
    """修复所有中文标点符号为英文标点"""
    file_path = "D:\\develop\\Python\\PyManagement\\scripts\\add_new_articles.py"
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 定义中文到英文标点的映射
    punctuation_map = {
        '，': ',',  # 中文逗号
        '。': '.',  # 中文句号
        '；': ';',  # 中文分号
        '：': ':',  # 中文冒号
        '？': '?',  # 中文问号
        '！': '!',  # 中文感叹号
        '（': '(',  # 中文左括号
        '）': ')',  # 中文右括号
        '【': '[',  # 中文左方括号
        '】': ']',  # 中文右方括号
        '「': '"',  # 中文左引号
        '」': '"',  # 中文右引号
        '『': '"',  # 中文左双引号
        '』': '"',  # 中文右双引号
        '“': '"',  # 中文左双引号
        '”': '"',  # 中文右双引号
        '‘': "'",  # 中文左单引号
        '’': "'",  # 中文右单引号
        '—': '-',  # 中文破折号
        '…': '...', # 中文省略号
        '、': ',',  # 中文顿号
        '《': '"',  # 中文书名号
        '》': '"',  # 中文书名号
        '〈': '<',  # 中文左尖括号
        '〉': '>',  # 中文右尖括号
    }
    
    # 替换所有中文标点
    for chinese, english in punctuation_map.items():
        content = content.replace(chinese, english)
    
    # 写入修复后的内容
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("成功修复所有中文标点符号")

if __name__ == "__main__":
    fix_all_punctuation()