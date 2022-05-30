
import os
import sys
import shutil

layer_path = '/home/evgesha/Documents'
layer_name = 'Individualnyy_p=210303_0eiBi85-MYSHOP.FDB'
def db_operations():
	os.system('''sudo docker exec -it billing_postgres psql -U billing -c "DROP DATABASE billing_prod3"''')
	print('database removed')
	os.system('''sudo docker exec -it billing_postgres psql -U billing -c "create DATABASE billing_prod3 with owner billing"''')
	print('new database created')
	print('begin upload dump')
	os.system('''cat billing_prod_20225196528_5401.sql | docker exec -i billing_postgres psql -U billing -d billing_prod3''')
	print('upload over')
def move_layer():
	os.chdir(layer_path)
	shutil.copy2(layer_path+ '/'+ layer_name  , '/home/evgesha/code/storecraft/.deploy/data/firebird/storage/')


if __name__ == '__main__':
	db_operations()
	move_layer()
