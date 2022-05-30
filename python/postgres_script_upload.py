
import os
import sys
import shutil

layer_path = '/home/evgesha/Documents'
layer_name = 'Individualnyy_p=210303_0eiBi85-MYSHOP.FDB'


def remove_connections():
	os.system('''sudo docker exec -it billing_postgres psql -U billing -c "SELECT pg_terminate_backend(pg_stat_activity.procpid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'billing_prod3' 
  AND procpid <> pg_backend_pid();''')
	print('database removed')
	
def remove_db():
	os.system('''sudo docker exec -it billing_postgres psql -U billing -c "DROP DATABASE billing_prod3"''')
	print('database removed')

def db_operations():
	remove_db()
	os.system('''sudo docker exec -it billing_postgres psql -U billing -c "create DATABASE billing_prod3 with owner billing"''')
	print('new database created')
	print('begin upload dump')
	os.system('''cat billing_prod_20225196528_5401.sql | docker exec -i billing_postgres psql -U billing -d billing_prod3''')
	print('upload over')
	
def move_layer():
	os.chdir(layer_path)
	shutil.copy2(layer_path+ '/'+ layer_name  , '/home/evgesha/code/storecraft/.deploy/data/firebird/storage/')
	print('layer moved')

def create_super_user():
	os.system('''sudo docker exec -it billing_postgres psql -U billing -d billing_prod3 -c "INSERT INTO public.auth_user
(id, "password", last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
VALUES(289050, 'pbkdf2_sha256$150000$NXYQhbq2fd4d$r8gpyhY4tDYj36yViUFk4Q++8Cy0bwwi/nGcAP1JH7s=', NULL, true, 'user', '', '', 'wwww@gamil.ru', true, true, '2022-05-30 20:06:56.877');
" ''')
	print('super user created')

if __name__ == '__main__':
	db_operations()
	move_layer()
	create_super_user()
