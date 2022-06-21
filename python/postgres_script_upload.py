#!/usr/bin/env python3.6
import os
import shutil

layer_path = '/home/evgesha/Documents'
layer_name = 'Gennadevna=180510_RwbVnw7-MYSHOP.FDB'
engine_name = 'sun2.litebox.ru_20_06_2022_11_48_05_ENGINE.FDB'
NAME_BASE = 'billing_prod3'
billin_dir = '/home/evgesha/code/'

CONTAINER_NAME = 'billing_postgres'

LAYER_PLACE = '/'.join([layer_path, layer_name])
LAYER_STORAGE = '/home/evgesha/code/storecraft/.deploy/data/firebird/storage/'
ENGINE_STORAGE = '/home/evgesha/code/storecraft/.deploy/data/firebird/'
ENGINE_PLACE = '/'.join([layer_path, engine_name])
DB_OPERATION = f'sudo docker exec -it {CONTAINER_NAME} psql -U billing -c'
CONTAINER_OP = 'sudo docker'
DUMP_NAME = 'billing_prod_202267111617_87243.sql'

def remove_connection_to(container, need_to_up_container = True):
	os.system(f'''{CONTAINER_OP} stop {container} ''')
	if need_to_up_container:
		os.system(f'''{CONTAINER_OP} start {container} ''')

def remove_db():
	os.system(f'''{DB_OPERATION} "DROP DATABASE {NAME_BASE}"''')
	print('database removed')

def restore_db():
	os.system(f'''{DB_OPERATION} "create DATABASE {NAME_BASE} with owner billing"''')
	print('new database created')

def upload_dump():
	print('begin upload dump')
	os.system(f'''cat {DUMP_NAME} | docker exec -i {CONTAINER_NAME} psql -U billing -d {NAME_BASE}''')
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
	shutil.copy2(ENGINE_PLACE, ENGINE_STORAGE)
	print('layer moved')

def create_super_user():
	os.chdir('/home/evgesha/code/billing')
	res = os.system('''echo "from django.contrib.auth.models import User; User.objects.create_superuser(
		'user', 'leningrad@spb.ru', '1q2w3e4r')" | /home/evgesha/code/billing/env37/bin/python3 manage.py shell''')
	if res:
		os.system('echo created user')

def kill_server():
	os.system('lsof -t -i tcp:8000 | xargs kill -9')

def notify_me():
	os.system('aplay /usr/share/sounds/sound-icons/piano-3.wav' )
	os.system('notify-send "upload status"  "script is over"')

def create_sql_with_layer():

	my_PATH = """/home/evgesha/code/storecraft/.deploy/data/firebird/my_sql.sql"""
	my_file = open(my_PATH, 'w')
	my_file.write("""CONNECT '/firebird/data/sun2.litebox.ru_20_06_2022_11_48_05_ENGINE.FDB' USER 'SYSDBA' PASSWORD 'masterkey';
		update engine_users eu set eu.passwd='pbkdf2_sha256$200$gIdhBJC5WAgz$0q2L7V5WcuodEMI62ULACYVo/rA3JhX6qwsmi0leptk=' 
		where eu.phonenumber = '79037104579';""")
	my_file.close()
	return my_PATH

def replace_engine_password():
	path = create_sql_with_layer()
	os.chdir('/home/evgesha/code/storecraft/.deploy/data/firebird')
	os.system('docker exec -it firebird isql -q -i firebird/data/my_sql.sql')
	os.remove(path)

def main():
	remove_connection_to(CONTAINER_NAME)
	db_operations()
	# TODO move layer and restore db to async
	remove_connection_to('storecraft', need_to_up_container=False)
	
	try:
		move_layer()
	except Exception as e:
		print(e)
	replace_engine_password()
	create_super_user()
	
	kill_server()
	notify_me()


if __name__ == '__main__':
	main()
	
	
	
