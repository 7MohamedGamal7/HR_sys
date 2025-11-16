#!/usr/bin/env python
"""
Script to fix Django template syntax errors across all templates
"""
import os
import re
from pathlib import Path

def fix_template_syntax(content):
    """Fix common Django template syntax errors"""
    
    # Fix template tags without spaces: {%tag to {% tag
    content = re.sub(r'\{%([a-z_]+)', r'{% \1', content)
    
    # Fix template tags without spaces: tag%} to tag %}
    content = re.sub(r'([a-z_]+)%\}', r'\1 %}', content)
    
    # Fix {{if to {% if
    content = re.sub(r'\{\{if\s+', r'{% if ', content)
    
    # Fix {{else to {% else
    content = re.sub(r'\{\{else\s+%\}\}', r'{% else %}', content)
    
    # Fix {{endif to {% endif
    content = re.sub(r'\{\{endif\s+%\}\}', r'{% endif %}', content)
    
    # Fix {{for to {% for
    content = re.sub(r'\{\{for\s+', r'{% for ', content)
    
    # Fix {{endfor to {% endfor
    content = re.sub(r'\{\{endfor\s+%\}\}', r'{% endfor %}', content)
    
    # Fix {{block to {% block
    content = re.sub(r'\{\{block\s+', r'{% block ', content)
    
    # Fix {{endblock to {% endblock
    content = re.sub(r'\{\{endblock\s+%\}\}', r'{% endblock %}', content)
    
    # Fix {{url to {% url
    content = re.sub(r'\{\{url\s+', r'{% url ', content)
    
    # Fix {{csrf_token %}} to {% csrf_token %}
    content = re.sub(r'\{\{csrf_token\s+%\}\}', r'{% csrf_token %}', content)
    
    # Fix {{form|crispy %}} to {{ form|crispy }}
    content = re.sub(r'\{\{([a-z_]+)\|crispy\s+%\}\}', r'{{ \1|crispy }}', content)
    
    # Fix double spaces in template tags
    content = re.sub(r'\{%\s\s+', r'{% ', content)
    content = re.sub(r'\s\s+%\}', r' %}', content)
    
    return content

def fix_all_templates(templates_dir='templates'):
    """Fix all HTML templates in the templates directory"""
    fixed_count = 0
    error_count = 0
    
    templates_path = Path(templates_dir)
    
    for html_file in templates_path.rglob('*.html'):
        try:
            # Read the file
            with open(html_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Fix syntax
            fixed_content = fix_template_syntax(original_content)
            
            # Only write if changes were made
            if fixed_content != original_content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                print(f"✅ Fixed: {html_file}")
                fixed_count += 1
            else:
                print(f"⏭️  Skipped (no changes): {html_file}")
                
        except Exception as e:
            print(f"❌ Error fixing {html_file}: {e}")
            error_count += 1
    
    print(f"\n{'='*60}")
    print(f"✅ Fixed {fixed_count} templates")
    print(f"❌ Errors: {error_count}")
    print(f"{'='*60}")

if __name__ == '__main__':
    fix_all_templates()

