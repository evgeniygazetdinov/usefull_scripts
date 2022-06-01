
import os
import shutil

layer_path = '/home/evgesha/Documents'
layer_name = 'Individualnyy_p=210303_0eiBi85-MYSHOP.FDB'
NAME_BASE = 'billing_prod3'
billin_dir = '/home/evgesha/code/'

CONTAINER_NAME = 'billing_postgres'

LAYER_PLACE = '/'.join([layer_path, layer_name])
LAYER_STORAGE = '/home/evgesha/code/storecraft/.deploy/data/firebird/storage/'
DB_OPERATION = f'sudo docker exec -it {CONTAINER_NAME} psql -U billing -c'
CONTAINER_OP = 'sudo docker'

def remove_connection_to(container):
	os.system(f'''{CONTAINER_OP} stop {container} ''')
	os.system(f'''{CONTAINER_OP} start {container} ''')

def remove_db():
	os.system(f'''{DB_OPERATION} "DROP DATABASE {NAME_BASE}"''')
	print('database removed')

def restore_db():
	os.system(f'''{DB_OPERATION} "create DATABASE {NAME_BASE} with owner billing"''')
	print('new database created')

def upload_dump():
	print('begin upload dump')
	os.system(f'''cat billing_prod_20225196528_5401.sql | docker exec -i {CONTAINER_NAME} psql -U billing -d {NAME_BASE}''')
	print('upload over')

def restore_db_from_dump():
	restore_db()
	upload_dump()

def db_operations():
	remove_db()
	restore_db_from_dump()
	
def move_layer():
	os.chdir(layer_path)
		# copy layer from     to
	shutil.copy2(LAYER_PLACE, LAYER_STORAGE)
	print('layer moved')

def create_super_user():
	os.chdir('/home/evgesha/code/billing')
	res = os.system('''echo "from django.contrib.auth.models import User; User.objects.create_superuser(
		'user', 'leningrad@spb.ru', '1q2w3e4r')" | /home/evgesha/code/billing/env37/bin/python3 manage.py shell''')
	if res:
		os.system('echo created user')

if __name__ == '__main__':
	remove_connection_to(CONTAINER_NAME)
	db_operations()
	# TODO move layer and restore db to async
	remove_connection_to('storecraft')
	move_layer()
	create_super_user()
