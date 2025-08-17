#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

def fix_chinese_punctuation():
    """修复add_new_articles.py中的中文标点符号"""
    file_path = 'add_new_articles.py'
    
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换中文标点符号为英文标点
        replacements = {
            '：': ':',
            '、': ',',
            '（': '(',
            '）': ')',
            '【': '[',
            '】': ']',
            '“': '"',
            '”': '"',
            '‘': "'",
            '’': "'",
            '——': '--',
            '…': '...',
            '。': '.',
            '？': '?',
            '！': '!',
            '；': ';',
            '《': '<',
            '》': '>',
            '——': '--',
            '·': '.'
        }
        
        for chinese, english in replacements.items():
            content = content.replace(chinese, english)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("成功修复所有中文标点符号")
        return True
        
    except Exception as e:
        print(f"修复失败: {e}")
        return False

if __name__ == "__main__":
    fix_chinese_punctuation()