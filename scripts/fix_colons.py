#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

def fix_colons():
    """修复add_new_articles.py中的中文全角冒号"""
    file_path = 'add_new_articles.py'
    
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换中文全角冒号为标准冒号
        content = content.replace('：', ':')
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("成功替换所有中文全角冒号为标准冒号")
        return True
        
    except Exception as e:
        print(f"替换失败: {e}")
        return False

if __name__ == "__main__":
    fix_colons()