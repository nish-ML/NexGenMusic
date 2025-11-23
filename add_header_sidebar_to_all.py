#!/usr/bin/env python
"""
Script to add white header and sidebar to all premium pages
"""

import os
import re

# Pages to update with their active nav IDs
pages_to_update = {
    'frontend/premium-spotify.html': 'nav-spotify',
    'frontend/premium-history.html': 'nav-history',
    'frontend/premium-about.html': 'nav-about',
}

# Read the header/sidebar template
with open('templates/includes/premium_header_sidebar.html', 'r', encoding='utf-8') as f:
    header_sidebar_template = f.read()

def update_page(filepath, active_nav_id):
    """Update a page to include header and sidebar"""
    print(f"\nUpdating {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has the new structure
    if 'premium_header_sidebar' in content or 'class="main-layout"' in content:
        print(f"  ✓ {filepath} already has header/sidebar")
        return
    
    # Find the body tag
    body_match = re.search(r'<body[^>]*>', content)
    if not body_match:
        print(f"  ✗ Could not find <body> tag in {filepath}")
        return
    
    body_start = body_match.end()
    
    # Find the closing body tag
    body_end_match = re.search(r'</body>', content)
    if not body_end_match:
        print(f"  ✗ Could not find </body> tag in {filepath}")
        return
    
    body_end = body_end_match.start()
    
    # Extract the current body content
    current_body_content = content[body_start:body_end]
    
    # Remove existing header if present
    current_body_content = re.sub(
        r'<header[^>]*>.*?</header>',
        '',
        current_body_content,
        flags=re.DOTALL
    )
    
    # Remove canvas3d if present
    current_body_content = re.sub(
        r'<canvas[^>]*id="canvas3d"[^>]*></canvas>',
        '',
        current_body_content
    )
    
    # Clean up extra whitespace
    current_body_content = current_body_content.strip()
    
    # Wrap content in container div if not already wrapped
    if not current_body_content.startswith('<div class="container"'):
        current_body_content = f'        <div class="container">\n{current_body_content}\n        </div>'
    
    # Create the new body content with header/sidebar
    new_header_sidebar = header_sidebar_template.replace(
        'id="' + active_nav_id + '"',
        'id="' + active_nav_id + '" class="active"'
    )
    
    new_body_content = f'''
{new_header_sidebar}
{current_body_content}
    </main>
</div>

<script src="/static/js/3d-background-premium.js"></script>
<script>
    function logout() {{
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('token');
        window.location.href = '/';
    }}
</script>
'''
    
    # Reconstruct the full content
    new_content = (
        content[:body_start] +
        new_body_content +
        content[body_end:]
    )
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✓ Updated {filepath}")

def main():
    print("=" * 60)
    print("Adding White Header & Sidebar to All Premium Pages")
    print("=" * 60)
    
    for filepath, active_nav_id in pages_to_update.items():
        if os.path.exists(filepath):
            update_page(filepath, active_nav_id)
        else:
            print(f"\n✗ File not found: {filepath}")
    
    print("\n" + "=" * 60)
    print("✅ Update Complete!")
    print("=" * 60)
    print("\nUpdated pages:")
    for filepath in pages_to_update.keys():
        if os.path.exists(filepath):
            print(f"  ✓ {filepath}")

if __name__ == '__main__':
    main()
