import sys, os
if len(sys.argv) > 1:
    DUMP_NAME = os.getcwd() + "\\" + sys.argv[1]
else:
    DUMP_NAME = os.getcwd() + "\\" + "billing_staging_2022122663520_35478.sql"
POSTGRES_USER = "billing"
POSTGRES_PASSWORD = POSTGRES_USER
NAME_BASE = 'billing'
CONTAINER_NAME = "billing_postgres"
SUPERUSER = 'john'
SUPERUSER_PASS = 'securePass1'
layer = sys.argv[2]
engine = sys.argv[3]
if sys.platform == "win32":
    OPERATION_BODY = f"docker exec -it {CONTAINER_NAME}"
else:
    OPERATION_BODY = f"sudo docker exec -it {CONTAINER_NAME}"
DB_OPERATION = OPERATION_BODY + " psql -U billing -c"

def start_postgres():
    os.system('cd C:\\Users\\evgesha\\code\\billing && docker-compose -f .\.deploy\local-compose.yml up -d billing_postgres')

def remove_db():
    oper = f'''{OPERATION_BODY} psql -U {SUPERUSER} -d postgres -c  "DROP DATABASE {NAME_BASE}  WITH (FORCE)"'''
    os.system(oper)

def restore_db():
    oper = (
        f"""{OPERATION_BODY} psql -U {POSTGRES_USER} -d postgres -c  "create user {POSTGRES_USER} with encrypted password"""
        + f"'{POSTGRES_PASSWORD}'"
        + '"'
    )
    os.system(oper)
    oper = f'''{OPERATION_BODY} psql -U {POSTGRES_USER} -d postgres -c  "CREATE DATABASE {NAME_BASE}"'''
    os.system(oper)


def upload_dump():
    print("begin upload dump")
    if not sys.platform == "win32":
        operation = f"""cat {DUMP_NAME} | docker exec -i {CONTAINER_NAME} psql -U billing -d billing"""
    else:
        print('here', DUMP_NAME)
        # running on windows
        operation = f"""type  {DUMP_NAME} | docker exec -i {CONTAINER_NAME} psql -U billing -d {NAME_BASE}"""
    os.system(operation)
    print("upload over")

def move_files():
    os.chdir('Downloads\\')
    print(os.getcwd())
    result = os.getcwd()+'\\'+ layer
    print(result)
    command = f'copy {result} C:\\Users\\evgesha\\code\\storecraft\\.deploy\\data\\firebird\\storage'
    os.popen(command)
    result = os.getcwd()+'\\'+ engine
    command = f'copy {result} C:\\Users\\evgesha\\code\\storecraft\\.deploy\\data\\firebird\\'
    os.popen(command)


def stop_storecraft():
    os.system('cd C:\\Users\\evgesha\\code\\storecraft\\ && make stop')

def start_storecraft():
    os.system("cd C:\\Users\\evgesha\\code\\storecraft\\modules && C:\\Users\\evgesha\\code\\storecraft\\venv\\Scripts\\python.exe startMYSHOP.py --server1=http --socket_port1=8101 --thread_pool=4")

def kill_storecraft():
    os.system('taskkill /F /IM python.exe')

def main():
    start_postgres()
    remove_db()
    restore_db()
    upload_dump()
    stop_storecraft()
    move_files()
    start_postgres()
    start_storecraft()

    

if __name__ == "__main__":
    main()
