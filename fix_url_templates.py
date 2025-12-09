#!/usr/bin/env python3
import os
import re

def fix_url_syntax_errors(file_path):
    """Fix URL template syntax errors with extra closing braces"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix {% url 'name' %}} to {% url 'name' %}
        content = re.sub(r"(\{%\s*url\s+[^%]+)\}\}", r"\1%}", content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed: {file_path}")
        return True
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def find_and_fix_url_templates():
    """Find and fix all templates with URL syntax errors"""
    templates_dir = "f:\\HR_sys\\v3\\HR_sys\\templates"
    fixed_count = 0
    
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check if file has URL syntax errors
                    if re.search(r"\{%\s*url\s+[^%]+\}\}", content):
                        if fix_url_syntax_errors(file_path):
                            fixed_count += 1
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    print(f"\nTotal templates fixed: {fixed_count}")

if __name__ == "__main__":
    find_and_fix_url_templates()