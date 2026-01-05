import os
import django
import sys

# Ensure project root is on sys.path so `mycourse` is importable
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mycourse.settings')
try:
    django.setup()
except Exception as e:
    print('Failed to setup Django:', e)
    sys.exit(1)

from django.test import Client
from django.contrib.auth import get_user_model
from courses.models import Cart, Course

User = get_user_model()

ADMIN_PASSWORD = '12122005'
CANDIDATES = ['admin', 'administrator', 'root']

client = Client()
user = None

# Try common usernames first
for uname in CANDIDATES:
    if client.login(username=uname, password=ADMIN_PASSWORD):
        user = User.objects.filter(username=uname).first()
        print(f'Logged in with username: {uname}')
        break

# If not, try any superuser account (attempt login with its username)
if not user:
    su = User.objects.filter(is_superuser=True).first()
    if su:
        if client.login(username=su.username, password=ADMIN_PASSWORD):
            user = su
            print(f'Logged in with superuser: {su.username}')

if not user:
    print('Unable to authenticate with given password. Aborting test.')
    sys.exit(2)

# Ensure there is at least one course and a cart item for the user
course = Course.objects.first()
if not course:
    print('No Course objects found; cannot create cart item. Aborting.')
    sys.exit(3)

cart_items = Cart.objects.filter(user=user)
if not cart_items.exists():
    Cart.objects.create(user=user, course=course)
    print(f'Created Cart item for user {user.username} and course {course.title}')
else:
    print(f'User already has {cart_items.count()} cart item(s)')

# Access checkout page (GET)
r = client.get('/checkout/', HTTP_HOST='localhost')
print('GET /checkout/ status_code=', r.status_code)

# POST checkout selecting momo (follow redirects / renders)
r2 = client.post('/checkout/', {'payment_method': 'momo'}, follow=True, HTTP_HOST='localhost')
print('POST /checkout/ (momo) status_code=', r2.status_code)

content = r2.content.decode('utf-8', errors='ignore')
if 'momo-qr.png' in content or 'Quét mã QR' in content or 'Hướng dẫn thanh toán' in content:
    print('Payment instruction page rendered successfully (contains momo markers).')
    # Optional: print the final path
    try:
        final_path = r2.request.get('PATH_INFO')
        print('Final PATH_INFO =', final_path)
    except Exception:
        pass
    sys.exit(0)

# If not found, print some diagnostics
print('Payment instruction page not detected in response. Response snippet:')
print(content[:800])
sys.exit(4)
