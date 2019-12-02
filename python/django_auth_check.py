from django.contrib.auth import authenticate
#wander user pass
u = authenticate(username="user", password="pass")
u.is_staff #True
u.is_superuser #True
