
import os
import sys

os.system('''sudo docker exec -it billing_postgres psql -U billing -c "DROP DATABASE billing_prod3"''')
print('database removed')
os.system('''sudo docker exec -it billing_postgres psql -U billing -c "create DATABASE billing_prod3 with owner billing"''')
print('new database created')
print('begin upload dump')
os.system('''cat billing_prod_20225196528_5401.sql | docker exec -i billing_postgres psql -U billing -d billing_prod3''')
print('upload over')
