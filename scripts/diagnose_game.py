#!/usr/bin/env python3
"""
Mood Wave Rider - Diagnostic Script
Checks if all game files are properly installed
"""

import os
import sys

def check_file(path, expected_size_min=None):
    """Check if file exists and optionally verify size"""
    if os.path.exists(path):
        size = os.path.getsize(path)
        status = "✅"
        if expected_size_min and size < expected_size_min:
            status = "⚠️"
        print(f"{status} {path} ({size:,} bytes)")
        return True
    else:
        print(f"❌ {path} - NOT FOUND")
        return False

def check_content(path, search_string):
    """Check if file contains specific string"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            if search_string in content:
                print(f"   ✅ Contains: {search_string}")
                return True
            else:
                print(f"   ❌ Missing: {search_string}")
                return False
    except Exception as e:
        print(f"   ❌ Error reading file: {e}")
        return False

def main():
    print("=" * 60)
    print("🎮 MOOD WAVE RIDER - DIAGNOSTIC CHECK")
    print("=" * 60)
    print()
    
    all_good = True
    
    # Check game files
    print("📁 Checking Game Files:")
    print("-" * 60)
    
    if not check_file('static/js/mood-wave-rider.js', 10000):
        all_good = False
    else:
        check_content('static/js/mood-wave-rider.js', 'class MoodWaveRider')
    
    if not check_file('static/css/mood-wave-rider.css', 5000):
        all_good = False
    else:
        check_content('static/css/mood-wave-rider.css', '.game-header')
    
    if not check_file('templates/mood-wave-rider.html', 2000):
        all_good = False
    
    print()
    
    # Check dashboard integration
    print("📄 Checking Dashboard Integration:")
    print("-" * 60)
    
    if not check_file('frontend/premium-dashboard.html'):
        all_good = False
    else:
        print("   Checking for game card...")
        check_content('frontend/premium-dashboard.html', 'openMoodWaveRider()')
        
        print("   Checking for CSS link...")
        check_content('frontend/premium-dashboard.html', 'mood-wave-rider.css')
        
        print("   Checking for JavaScript function...")
        check_content('frontend/premium-dashboard.html', 'function openMoodWaveRider')
    
    print()
    
    # Check test files
    print("🧪 Checking Test Files:")
    print("-" * 60)
    
    check_file('test_game.html')
    check_file('GAME_TROUBLESHOOTING.md')
    
    print()
    print("=" * 60)
    
    if all_good:
        print("✅ ALL CHECKS PASSED!")
        print()
        print("🎮 To test the game:")
        print("1. Run: python manage.py runserver")
        print("2. Open: http://localhost:8000/dashboard/")
        print("3. Click the 'Mood Wave Rider' card")
        print()
        print("If game still doesn't work:")
        print("- Open browser console (F12)")
        print("- Look for error messages")
        print("- Check GAME_TROUBLESHOOTING.md")
    else:
        print("❌ SOME CHECKS FAILED!")
        print()
        print("Missing files need to be created.")
        print("Check the error messages above.")
    
    print("=" * 60)

if __name__ == '__main__':
    main()
