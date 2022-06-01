
import os
import sys
import shutil

layer_path = '/home/evgesha/Documents'
layer_name = 'Individualnyy_p=210303_0eiBi85-MYSHOP.FDB'
NAME_BASE = 'billing_prod3'
LAYER_PLACE = '/'.join([layer_path, layer_name])
LAYER_STORAGE = '/home/evgesha/code/storecraft/.deploy/data/firebird/storage/'
DB_OPERATION = 'sudo docker exec -it billing_postgres psql -U billing -c'

	
def remove_db():
	os.system(f'''{DB_OPERATION} "DROP DATABASE {NAME_BASE}"''')
	print('database removed')

def restore_db():
	os.system(f'''{DB_OPERATION} "create DATABASE {NAME_BASE} with owner billing"''')
	print('new database created')

def upload_dump():
	print('begin upload dump')
	os.system(f'''cat billing_prod_20225196528_5401.sql | docker exec -i billing_postgres psql -U billing -d {NAME_BASE}''')
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
	os.system(f'''{DB_OPERATION} "INSERT INTO "auth_user" ("password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined") VALUES ('pbkdf2_sha256$150000$TNb5eCJOSRiN$qITNydZmKMh+0ljKvlQVwZ8pZxgnmRwyFztThFs316U=', NULL, true, 'user', '', '', 'w@w.ru', true, true, '2022-06-01T01:45:37.940205+00:00'::timestamptz) RETURNING "auth_user"."id"; args=('pbkdf2_sha256$150000$TNb5eCJOSRiN$qITNydZmKMh+0ljKvlQVwZ8pZxgnmRwyFztThFs316U=', None, True, 'user', '', '', 'w@w.ru', True, True, datetime.datetime(2022, 6, 1, 1, 45, 37, 940205, tzinfo=<UTC>))
" ''')
	os.system(f'''{DB_OPERATION} "INSERT INTO "billing_userprofile" ("created_at", "updated_at", "user_id", "title", "activation_trial_period_available", "registration_date", "global_user_id", "layer_owner", "payment_day", "expected_positive_balance_date", "timezone_offset_minutes", "organization", "credit", "freeze_application_service_hours", "version_service_user", "auto_payment", "auto_payment_robokassa_invoice_id") VALUES ('2022-06-01T01:45:38.048464+00:00'::timestamptz, '2022-06-01T01:45:38.048485+00:00'::timestamptz, 289051, 'user', true, '2022-06-01T01:45:38.048242+00:00'::timestamptz, NULL, false, NULL, NULL, 0, 'mts', false, NULL, NULL, false, NULL) RETURNING "billing_userprofile"."id"; args=(datetime.datetime(2022, 6, 1, 1, 45, 38, 48464, tzinfo=<UTC>), datetime.datetime(2022, 6, 1, 1, 45, 38, 48485, tzinfo=<UTC>), 289051, 'user', True, datetime.datetime(2022, 6, 1, 1, 45, 38, 48242, tzinfo=<UTC>), None, False, None, None, 0, 'mts', False, None, None, False, None)
" ''')
	os.system(f'''{DB_OPERATION} "UPDATE "billing_userprofile" SET "created_at" = '2022-06-01T01:45:38.048464+00:00'::timestamptz, "updated_at" = '2022-06-01T01:45:38.055182+00:00'::timestamptz, "user_id" = 289051, "title" = 'user', "activation_trial_period_available" = true, "registration_date" = '2022-06-01T01:45:38.048242+00:00'::timestamptz, "global_user_id" = NULL, "layer_owner" = false, "payment_day" = NULL, "expected_positive_balance_date" = NULL, "timezone_offset_minutes" = 0, "organization" = 'mts', "credit" = false, "freeze_application_service_hours" = NULL, "version_service_user" = NULL, "auto_payment" = false, "auto_payment_robokassa_invoice_id" = NULL WHERE "billing_userprofile"."id" = 286841; args=(datetime.datetime(2022, 6, 1, 1, 45, 38, 48464, tzinfo=<UTC>), datetime.datetime(2022, 6, 1, 1, 45, 38, 55182, tzinfo=<UTC>), 289051, 'user', True, datetime.datetime(2022, 6, 1, 1, 45, 38, 48242, tzinfo=<UTC>), False, 0, 'mts', False, False, 286841)" ''')
	print('super user created')

if __name__ == '__main__':
	db_operations()
	# TODO move layer and restore db to async
	move_layer()
	create_super_user()
