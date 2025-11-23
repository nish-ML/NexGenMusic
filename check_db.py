import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicproject.settings')
django.setup()

from music_app.models import History
from django.contrib.auth.models import User

print("Database Check:")
print("=" * 30)
print(f"Users: {User.objects.count()}")
print(f"History entries: {History.objects.count()}")

if History.objects.exists():
    h = History.objects.first()
    print(f"Sample history: '{h.prompt}' -> {h.sentiment}/{h.mood} by {h.user.username if h.user else 'No user'}")
    print(f"Music file: {h.music_file}")
else:
    print("No history entries found")

print("\nRecent history (last 5):")
for h in History.objects.order_by('-created_at')[:5]:
    print(f"- {h.created_at}: '{h.prompt[:30]}...' -> {h.sentiment}/{h.mood}")
