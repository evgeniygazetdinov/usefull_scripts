#!/usr/bin/env python3.6
import os
import shutil

layer_path = '/home/evgesha/Documents'
layer_name = 'IP_KAREV_ANTON_=190627_x4OAQfo-MYSHOP.FDB'
engine_name = 'bellatrix.litebox.ru_23_06_2022_06_45_48_ENGINE.FDB'
phone = '79085314351'
NAME_BASE = 'billing_prod3'
billin_dir = '/home/evgesha/code/'
CONTAINER_NAME = 'billing_postgres'

LAYER_PLACE = '/'.join([layer_path, layer_name])
LAYER_STORAGE = '/home/evgesha/code/storecraft/.deploy/data/firebird/storage/'
ENGINE_STORAGE = '/home/evgesha/code/storecraft/.deploy/data/firebird/'
ENGINE_PLACE = '/'.join([layer_path, engine_name])
DB_OPERATION = f'sudo docker exec -it {CONTAINER_NAME} psql -U billing -c'
CONTAINER_OP = 'sudo docker'
DUMP_NAME = 'billing_prod_2022896155_43760.sql'

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

def do_postgres_job():
	remove_db()
	print('db_ removed')
	restore_db_from_dump()
	
def move_firebird_files():
	os.chdir(layer_path)
		# copy layer from     to
	shutil.copy2(LAYER_PLACE, LAYER_STORAGE)
	shutil.copy2(ENGINE_PLACE, ENGINE_STORAGE)
	print('layer moved')

def create_super_user_in_django():
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
	engine_work = """/home/evgesha/code/storecraft/.deploy/data/firebird/engine_work.sql"""
	layer_work = """/home/evgesha/code/storecraft/.deploy/data/firebird/layer_work.sql"""
	my_file = open(engine_work, 'w')
	my_file.write(f"""CONNECT '/firebird/data/{engine_name}' USER 'SYSDBA' PASSWORD 'masterkey';
		update engine_users eu set eu.passwd='pbkdf2_sha256$200$XfwDobs6u49X$O6lr8NFZiuAHwrcBfe+sSJhDQcjOV+DGG6j1HCNCtxU=' 
		where eu.phonenumber = '{phone}';""")
	my_file.close()
	my_file = open(layer_work, 'w')
	my_file.write(f"""CONNECT '/firebird/data/storage/{layer_name}' USER 'SYSDBA' PASSWORD 'masterkey';
		update profile pr set pr.status='-1' where pr.uid != 468 and pr.status='1';""")
	my_file.close()
			
	return [engine_work, layer_work]

def do_job_with_firebird():
	sql_paths = create_sql_with_layer()
	os.chdir('/home/evgesha/code/storecraft/.deploy/data/firebird')
	os.system('docker exec -it firebird isql -q -i firebird/data/engine_work.sql')
	os.system('docker exec -it firebird isql -q -i firebird/data/layer_work.sql')
	[os.remove(path) for path in sql_paths]

def make_migrations():
	os.chdir('/home/evgesha/code/storecraft')
	try:
		os.system('make migrations')
	except:
		pass

def up_billing_again():
	os.chdir('/home/evgesha/code/billing')
	os.system('env37/bin/python3 manage.py runserver 0.0.0.0:8000')

def main():
	#remove_connection_to(CONTAINER_NAME)
	kill_server()
	do_postgres_job()
	create_super_user_in_django()
	# # TODO move layer and restore db to async
	# remove_connection_to('storecraft', need_to_up_container=False)
	# try:
	# 	move_firebird_files()
	# except Exception as e:
	# 	print(e)
	# do_job_with_firebird()
	

	# make_migrations()
	# notify_me()
	# up_billing_again()



if __name__ == '__main__':
	main()
	
