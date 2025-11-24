#!/usr/bin/env python3
"""
Automated Layout Updater for NexGenMusic
This script helps update remaining pages with 3D background and header
"""

import os
import re

# Pages that need to be updated
PAGES_TO_UPDATE = [
    'frontend/library-favorites.html',
    'frontend/library-playlists.html',
    'frontend/premium-history.html',
    'frontend/premium-spotify.html',
    'frontend/premium-about.html',
    'frontend/spotify_recommendations.html',
    'frontend/history.html',
]

# Three.js CDN to add
THREEJS_CDN = '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>'

# 3D Canvas HTML
CANVAS_HTML = '''    <!-- 3D Background Canvas -->
    <canvas id="canvas3d"></canvas>
    '''

# Header HTML template
HEADER_HTML = '''    <!-- Header -->
    <header class="header">
        <a href="/dashboard/" class="logo">
            <span class="logo-icon">🎵</span>
            <span>NexGenMusic</span>
        </a>
        <a href="/dashboard/" class="back-btn">← Back to Dashboard</a>
    </header>
    '''

# 3D Script reference
SCRIPT_REF = '''    <!-- 3D Background Animation Script -->
    <script src="/static/js/3d-background-full.js"></script>'''

# CSS to add
CSS_ADDITION = '''        /* 3D Background Canvas */
        #canvas3d {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            pointer-events: none;
        }
        
        /* Make content appear above 3D background */
        .header, .main-layout, .container {
            position: relative;
            z-index: 1;
        }
        
        /* Header - Mint Frost Whisper */
        .header {
            background: linear-gradient(90deg, #e0fff4 0%, #d4f8e8 50%, #c8f5e0 100%);
            border-bottom: 2px solid rgba(152, 255, 152, 0.3);
            padding: 16px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 12px rgba(152, 255, 152, 0.15);
        }
        
        .logo { 
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 20px;
            font-weight: 700;
            color: #2d7a5f;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        
        .logo:hover {
            color: #10b981;
            transform: scale(1.05);
        }
        
        .logo-icon {
            font-size: 28px;
            filter: drop-shadow(0 2px 4px rgba(152, 255, 152, 0.3));
        }
        
        .back-btn {
            padding: 10px 20px;
            background: rgba(255, 255, 255, 0.3);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.4);
            border-radius: 8px;
            color: #2d7a5f;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        
        .back-btn:hover {
            background: rgba(255, 255, 255, 0.5);
            transform: translateY(-2px);
        }
        
'''

def read_file(filepath):
    """Read file content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return None

def write_file(filepath, content):
    """Write content to file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def backup_file(filepath):
    """Create backup of file"""
    backup_path = filepath + '.backup'
    content = read_file(filepath)
    if content:
        write_file(backup_path, content)
        print(f"✅ Backup created: {backup_path}")

def add_threejs_cdn(content):
    """Add Three.js CDN to head if not present"""
    if 'three.js' in content.lower():
        return content, False
    
    # Find </head> and add before it
    head_end = content.find('</head>')
    if head_end != -1:
        content = content[:head_end] + '    ' + THREEJS_CDN + '\n' + content[head_end:]
        return content, True
    return content, False

def add_3d_css(content):
    """Add 3D CSS to style section"""
    if '#canvas3d' in content:
        return content, False
    
    # Find <style> and add after it
    style_start = content.find('<style>')
    if style_start != -1:
        insert_pos = content.find('\n', style_start) + 1
        content = content[:insert_pos] + CSS_ADDITION + content[insert_pos:]
        return content, True
    return content, False

def add_canvas_and_header(content):
    """Add canvas and header after body tag"""
    if 'id="canvas3d"' in content:
        return content, False
    
    # Find <body> tag
    body_match = re.search(r'<body[^>]*>', content)
    if body_match:
        insert_pos = body_match.end()
        content = content[:insert_pos] + '\n' + CANVAS_HTML + '\n' + HEADER_HTML + '\n' + content[insert_pos:]
        return content, True
    return content, False

def add_3d_script(content):
    """Add 3D script before </body>"""
    if '3d-background-full.js' in content or '3d-background-simple.js' in content:
        return content, False
    
    # Find </body> and add before it
    body_end = content.rfind('</body>')
    if body_end != -1:
        content = content[:body_end] + '\n' + SCRIPT_REF + '\n' + content[body_end:]
        return content, True
    return content, False

def update_page(filepath):
    """Update a single page with all components"""
    print(f"\n📄 Processing: {filepath}")
    
    content = read_file(filepath)
    if not content:
        return False
    
    # Create backup
    backup_file(filepath)
    
    changes_made = []
    
    # Add Three.js CDN
    content, changed = add_threejs_cdn(content)
    if changed:
        changes_made.append("Added Three.js CDN")
    
    # Add 3D CSS
    content, changed = add_3d_css(content)
    if changed:
        changes_made.append("Added 3D CSS")
    
    # Add canvas and header
    content, changed = add_canvas_and_header(content)
    if changed:
        changes_made.append("Added canvas and header")
    
    # Add 3D script
    content, changed = add_3d_script(content)
    if changed:
        changes_made.append("Added 3D script")
    
    if changes_made:
        write_file(filepath, content)
        print(f"✅ Updated successfully!")
        for change in changes_made:
            print(f"   - {change}")
        return True
    else:
        print(f"ℹ️  No changes needed (already updated)")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("NexGenMusic Automated Layout Updater")
    print("=" * 60)
    print("\nThis script will update the following pages:")
    for page in PAGES_TO_UPDATE:
        print(f"  - {page}")
    
    print("\n⚠️  WARNING: This will modify your HTML files!")
    print("Backups will be created with .backup extension")
    
    response = input("\nProceed with updates? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("\n❌ Update cancelled")
        return
    
    print("\n" + "=" * 60)
    print("Starting updates...")
    print("=" * 60)
    
    updated_count = 0
    skipped_count = 0
    
    for page in PAGES_TO_UPDATE:
        if os.path.exists(page):
            if update_page(page):
                updated_count += 1
            else:
                skipped_count += 1
        else:
            print(f"\n❌ File not found: {page}")
            skipped_count += 1
    
    print("\n" + "=" * 60)
    print("Update Summary")
    print("=" * 60)
    print(f"✅ Updated: {updated_count} pages")
    print(f"ℹ️  Skipped: {skipped_count} pages")
    print(f"📁 Total: {len(PAGES_TO_UPDATE)} pages")
    
    if updated_count > 0:
        print("\n✨ Updates complete!")
        print("\n📝 Next steps:")
        print("1. Test each updated page in your browser")
        print("2. Verify 3D background is animating")
        print("3. Check that header displays correctly")
        print("4. If issues occur, restore from .backup files")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
