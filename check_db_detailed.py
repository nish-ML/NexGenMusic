#!/usr/bin/env python
"""
Detailed database check script for the music generation app
"""

import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicproject.settings')
django.setup()

from music_app.models import History, User
from django.db import connection

def check_database():
    print("Detailed Database Check")
    print("=" * 50)

    # Check database tables
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Database Tables: {[table[0] for table in tables]}")

    # Check users
    users = User.objects.all()
    print(f"\nTotal Users: {users.count()}")
    for user in users:
        print(f"- {user.username} (ID: {user.id}, Superuser: {user.is_superuser}, Staff: {user.is_staff})")

    # Check history entries
    histories = History.objects.all().order_by('-created_at')
    print(f"\nTotal History Entries: {histories.count()}")

    print("\nRecent History (last 5):")
    for h in histories[:5]:
        user_name = h.user.username if h.user else 'Anonymous'
        music_status = 'Yes' if h.music_file else 'No'
        print(f"- '{h.prompt[:40]}...' -> {h.sentiment}/{h.mood} by {user_name} (Music: {music_status})")

    # Check foreign key relationships
    print("\nForeign Key Relationships:")
    linked_histories = histories.filter(user__isnull=False)
    print(f"- {linked_histories.count()} history entries linked to users")

    for h in linked_histories[:3]:
        print(f"- History ID {h.id} -> User '{h.user.username}'")

    # Check for orphaned records
    orphaned_histories = histories.filter(user__isnull=True)
    print(f"- {orphaned_histories.count()} anonymous history entries")

    # Check music files
    music_files = histories.filter(music_file__isnull=False)
    print(f"- {music_files.count()} entries with music files")

    # Check data integrity
    print("\nData Integrity Check:")
    try:
        # Check if all required fields are present
        valid_histories = histories.filter(
            prompt__isnull=False,
            sentiment__isnull=False,
            mood__isnull=False
        )
        print(f"- {valid_histories.count()}/{histories.count()} histories have all required fields")

        # Check sentiment values
        sentiments = histories.values_list('sentiment', flat=True).distinct()
        print(f"- Sentiment values in DB: {list(sentiments)}")

        # Check mood values
        moods = histories.values_list('mood', flat=True).distinct()
        print(f"- Mood values in DB: {list(moods)}")

        print("\n✅ Database appears to be working correctly!")

    except Exception as e:
        print(f"❌ Database integrity check failed: {e}")

if __name__ == "__main__":
    check_database()
