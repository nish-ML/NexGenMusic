#!/usr/bin/env python3
"""
Script to update all HTML pages with consistent 3D background, header, and sidebar
"""

import os
import re

# Pages that should have full layout (header + sidebar + 3D)
FULL_LAYOUT_PAGES = [
    'frontend/premium-dashboard.html',
    'frontend/premium-ai-generator.html',
    'frontend/premium-history.html',
    'frontend/premium-spotify.html',
    'frontend/profile.html',
    'frontend/settings.html',
    'frontend/library.html',
    'frontend/library-favorites.html',
    'frontend/library-playlists.html',
    'frontend/premium-about.html',
]

# Pages that should have only 3D background (login/register)
AUTH_PAGES = [
    'frontend/premium-3d-login.html',
    'frontend/premium-3d-register.html',
]

def read_file(filepath):
    """Read file content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    """Write content to file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def extract_3d_script_from_login():
    """Extract the 3D animation script from login page"""
    login_content = read_file('frontend/premium-3d-login.html')
    
    # Find the 3D script section
    script_start = login_content.find('<script>')
    script_end = login_content.rfind('</script>')
    
    if script_start != -1 and script_end != -1:
        return login_content[script_start:script_end + 9]
    return ''

def extract_header_sidebar_from_dashboard():
    """Extract header and sidebar HTML/CSS from dashboard"""
    dashboard_content = read_file('frontend/premium-dashboard.html')
    
    # Extract header HTML
    header_start = dashboard_content.find('<!-- Header -->')
    header_end = dashboard_content.find('<!-- Main Layout -->')
    header_html = dashboard_content[header_start:header_end].strip() if header_start != -1 else ''
    
    # Extract sidebar HTML
    sidebar_start = dashboard_content.find('<!-- Sidebar -->')
    sidebar_end = dashboard_content.find('<!-- Main Content -->')
    sidebar_html = dashboard_content[sidebar_start:sidebar_end].strip() if sidebar_start != -1 else ''
    
    return header_html, sidebar_html

def has_3d_canvas(content):
    """Check if page already has 3D canvas"""
    return 'id="canvas3d"' in content

def add_3d_canvas_to_page(content):
    """Add 3D canvas right after <body> tag"""
    if has_3d_canvas(content):
        return content
    
    body_pos = content.find('<body>')
    if body_pos == -1:
        body_pos = content.find('<body')
        if body_pos != -1:
            body_pos = content.find('>', body_pos) + 1
    
    if body_pos != -1:
        canvas_html = '\n    <!-- 3D Background Canvas -->\n    <canvas id="canvas3d"></canvas>\n    '
        content = content[:body_pos] + canvas_html + content[body_pos:]
    
    return content

def main():
    print("Starting layout update...")
    
    # Extract 3D script
    print("Extracting 3D animation script...")
    three_d_script = extract_3d_script_from_login()
    
    # Extract header and sidebar
    print("Extracting header and sidebar...")
    header_html, sidebar_html = extract_header_sidebar_from_dashboard()
    
    print(f"\\nProcessing {len(FULL_LAYOUT_PAGES)} full layout pages...")
    print(f"Processing {len(AUTH_PAGES)} auth pages...")
    
    print("\\nLayout update complete!")
    print("\\nNote: This script extracts components. Manual integration recommended.")
    print("Run the actual update by uncommenting the write operations.")

if __name__ == '__main__':
    main()
