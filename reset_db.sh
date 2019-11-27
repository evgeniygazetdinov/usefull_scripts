#delete all migrations and reset models.py to initial state
rm -r app/migrations/
chmod +x manage.py
./manage.py flush
./manage.py schemamigration app --initial
./manage.py migrate app --fake
#after changing models.py
./manage.py schemamigration app --auto
./manage.py migrate app