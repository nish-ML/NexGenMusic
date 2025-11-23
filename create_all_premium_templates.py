#!/usr/bin/env python
"""
Create premium templates for all pages with header and sidebar
"""

import os

# Read the header/sidebar template
with open('templates/includes/premium_header_sidebar.html', 'r', encoding='utf-8') as f:
    header_sidebar = f.read()

# Template structure for each page
def create_page_template(title, active_nav_id, page_content):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - NexGenMusic</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
{header_sidebar.replace(f'id="{active_nav_id}"', f'id="{active_nav_id}" class="active"')}
        <div class="container">
{page_content}
        </div>
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
</body>
</html>'''

# Page configurations
pages = {
    'templates/spotify_recommendations_premium.html': {
        'title': 'Spotify Recommendations',
        'active_nav': 'nav-spotify',
        'content': '''
            <h1 style="font-size: 32px; font-weight: 700; margin-bottom: 24px;">🎧 Spotify Recommendations</h1>
            <div style="background: white; border-radius: 16px; padding: 40px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                <p style="color: #64748b; margin-bottom: 24px;">Get personalized music recommendations based on your mood and preferences.</p>
                <div id="recommendations-container">
                    <!-- Content will be loaded by JavaScript -->
                </div>
            </div>
        '''
    },
    'templates/history_premium.html': {
        'title': 'Generation History',
        'active_nav': 'nav-history',
        'content': '''
            <h1 style="font-size: 32px; font-weight: 700; margin-bottom: 24px;">🕐 Generation History</h1>
            <div style="background: white; border-radius: 16px; padding: 40px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                <p style="color: #64748b; margin-bottom: 24px;">View all your previously generated music tracks.</p>
                <div id="history-container">
                    <!-- Content will be loaded by JavaScript -->
                </div>
            </div>
        '''
    },
    'templates/about_premium.html': {
        'title': 'About',
        'active_nav': 'nav-about',
        'content': '''
            <h1 style="font-size: 32px; font-weight: 700; margin-bottom: 24px;">ℹ️ About NexGenMusic</h1>
            <div style="background: white; border-radius: 16px; padding: 40px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                <h2 style="font-size: 24px; font-weight: 600; margin-bottom: 16px;">AI-Powered Music Generation</h2>
                <p style="color: #64748b; line-height: 1.6; margin-bottom: 16px;">
                    NexGenMusic uses advanced AI technology to generate unique music based on your emotions and preferences.
                </p>
                <h3 style="font-size: 20px; font-weight: 600; margin-top: 24px; margin-bottom: 12px;">Features</h3>
                <ul style="color: #64748b; line-height: 1.8; margin-left: 24px;">
                    <li>AI-powered mood-based music generation</li>
                    <li>Spotify integration for personalized recommendations</li>
                    <li>Save and organize your favorite tracks</li>
                    <li>Beautiful 3D animated interface</li>
                    <li>High-quality audio output</li>
                </ul>
            </div>
        '''
    },
    'templates/library_premium.html': {
        'title': 'My Library',
        'active_nav': 'nav-library',
        'content': '''
            <h1 style="font-size: 32px; font-weight: 700; margin-bottom: 24px;">📚 My Library</h1>
            <div style="background: white; border-radius: 16px; padding: 40px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                <p style="color: #64748b; margin-bottom: 24px;">Access all your saved music, playlists, and favorites.</p>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 32px;">
                    <a href="/library/favorites/" style="background: #eff6ff; padding: 32px; border-radius: 12px; text-decoration: none; text-align: center; transition: all 0.2s;">
                        <div style="font-size: 48px; margin-bottom: 16px;">❤️</div>
                        <h3 style="font-size: 18px; font-weight: 600; color: #1e293b; margin-bottom: 8px;">Favorites</h3>
                        <p style="font-size: 14px; color: #64748b;">Your liked tracks</p>
                    </a>
                    <a href="/library/playlists/" style="background: #f0fdf4; padding: 32px; border-radius: 12px; text-decoration: none; text-align: center; transition: all 0.2s;">
                        <div style="font-size: 48px; margin-bottom: 16px;">📁</div>
                        <h3 style="font-size: 18px; font-weight: 600; color: #1e293b; margin-bottom: 8px;">Playlists</h3>
                        <p style="font-size: 14px; color: #64748b;">Your collections</p>
                    </a>
                </div>
            </div>
        '''
    },
    'templates/favorites_premium.html': {
        'title': 'Favorites',
        'active_nav': 'nav-favorites',
        'content': '''
            <h1 style="font-size: 32px; font-weight: 700; margin-bottom: 24px;">❤️ Favorites</h1>
            <div style="background: white; border-radius: 16px; padding: 40px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                <p style="color: #64748b; margin-bottom: 24px;">All your favorite tracks in one place.</p>
                <div id="favorites-container">
                    <!-- Content will be loaded by JavaScript -->
                </div>
            </div>
        '''
    },
    'templates/playlists_premium.html': {
        'title': 'Playlists',
        'active_nav': 'nav-playlists',
        'content': '''
            <h1 style="font-size: 32px; font-weight: 700; margin-bottom: 24px;">📁 Playlists</h1>
            <div style="background: white; border-radius: 16px; padding: 40px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                <p style="color: #64748b; margin-bottom: 24px;">Manage your music collections.</p>
                <div id="playlists-container">
                    <!-- Content will be loaded by JavaScript -->
                </div>
            </div>
        '''
    },
}

def main():
    print("=" * 60)
    print("Creating Premium Templates for All Pages")
    print("=" * 60)
    
    for filepath, config in pages.items():
        print(f"\nCreating {filepath}...")
        
        template = create_page_template(
            config['title'],
            config['active_nav'],
            config['content']
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(template)
        
        print(f"  ✓ Created {filepath}")
    
    print("\n" + "=" * 60)
    print("✅ All Templates Created!")
    print("=" * 60)
    print(f"\nCreated {len(pages)} premium templates")

if __name__ == '__main__':
    main()
