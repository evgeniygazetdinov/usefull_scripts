import os
import fdb
import config

node_layer_for_update = {
    "cursa": [
        "Severo_Kavkazsk=220607_0Jb0zWq",
        "Vostochno_Sibir=220607_7TYjKa8",
        "Zapadno_Sibirsk=220607_c0cdOYZ",
        "Uralskiy_filial=220607_Z5E55Tl",
        "Kuybyshevskiy_f=220607_ogIhxN",
        "Privolzhskiy_fi=220607_AIhJwR7",
        "Gorkovskiy_fili=220607_uvlKF6W",
        "Moskovskiy_fili=220607_A3P8tQw",
    ],
    "talitha2": ["Dalnevostochnyy=220607_q3o2xU6"],
    "rastaban": ["AO_FPK_=211027_iCwjP3Z"],
}
LAYERS_FOR_UPDATE = [
    "Severo_Kavkazsk=220607_0Jb0zWq",
    "Vostochno_Sibir=220607_7TYjKa8",
    "Zapadno_Sibirsk=220607_c0cdOYZ",
    "Uralskiy_filial=220607_Z5E55Tl",
    "Kuybyshevskiy_f=220607_ogIhxN",
    "Privolzhskiy_fi=220607_AIhJwR7",
    "Gorkovskiy_fili=220607_uvlKF6W",
    "Moskovskiy_fili=220607_A3P8tQw",
    "Dalnevostochnyy=220607_q3o2xU6",
    "AO_FPK_=211027_iCwjP3Z",
]

def connect_to_internal_db():

    con = fdb.connect(
        dsn=(config.DATABASE_CONFIG['host'] + '/' +
            config.DATABASE_CONFIG['port'] + ':' +
            config.DATABASE_CONFIG['dbname']
            ),
        user=config.DATABASE_CONFIG['user'],
        password=config.DATABASE_CONFIG['password'],
        sql_dialect=3,
        charset='WIN1251',
        isolation_level=fdb.bs([fdb.isc_tpb_version3,
                                fdb.isc_tpb_write,
                                fdb.isc_tpb_wait,
                                fdb.isc_tpb_read_committed,
                                fdb.isc_tpb_rec_version
                                ]
                            )
    )

    cur = con.cursor()
    select = "SELECT * FROM V_GLOBAL_BASES WHERE THREAD=0 AND CODE LIKE '%-ENGINE' ORDER BY CODE"
    cur.execute(select)
    return cur, con

def get_all_creditails():
    """ получим все данные по всем бд"""
    job_list = []
    cur, con = connect_to_internal_db()
    for row in cur:
        con_get_layers = fdb.connect(
            dsn=(row[1] + ':' +
                 row[2]
                 ),
            user=row[3],
            password=row[4],
            sql_dialect=3,
            charset='WIN1251',
            isolation_level=fdb.bs([fdb.isc_tpb_version3,
                                    fdb.isc_tpb_write,
                                    fdb.isc_tpb_wait,
                                    fdb.isc_tpb_read_committed,
                                    fdb.isc_tpb_rec_version
                                    ]
                                   )
        )

        cur_get_layers = con_get_layers.cursor()

        select_get_layers = "SELECT CODE FROM ENGINE_LAYERS WHERE CODE <> 'GLOBAL' " \
                            "AND (DISABLED = '0' OR DISABLED IS NULL) " \
                            "AND OWNER_ID is not null " \
                            "ORDER BY CODE"

        cur_get_layers.execute(select_get_layers)

        for row_get_layers in cur_get_layers:
            job_list.append([row[0], row_get_layers[0]])

        con_get_layers.commit()

        cur_get_layers.close()
        con_get_layers.close()

    con.commit()
    return job_list

    

def find_server_by_name(node_name: str) -> str:
    server_ip = str(node_name)
    return server_ip


def find_db_path_by_node_name(node_name: str) -> str:
    path = str(node_name)
    return path


def find_client_code(node_name: str) -> str:
    return node_name


def find_login():
    return "SYSDBA"


def find_password(node_name: str) -> str:
    return node_name


def find_node_by_layer(layer: str) -> str:
    for node, layers in node_layer_for_update.items():
        if layer in layers:
            return node


def make_connection_and_update_layer(
    server_ip: str, path: str, db_var: str, layer_code: str, login: str, password: str
):
    con_layer = fdb.connect(
        dsn=(
            server_ip
            + ":"
            + path
            + "/databases"
            + db_var
            + "/storage/"
            + layer_code
            + "-MYSHOP.FDB"
        ),
        user=login,
        password=password,
        sql_dialect=3,
        charset="WIN1251",
        isolation_level=fdb.bs(
            [
                fdb.isc_tpb_version3,
                fdb.isc_tpb_write,
                fdb.isc_tpb_wait,
                fdb.isc_tpb_read_committed,
                fdb.isc_tpb_rec_version,
            ]
        ),
    )

    cur_layer = con_layer.cursor()

    sql_text = "update config set is_rzd_layer=1"

    cur_layer.execute(sql_text)


def find_creditails_by_node_name(node: str) -> tuple:
    ip = find_server_by_name(node)
    db_path = find_db_path_by_node_name(node)
    db_var = os.path.basename(db_path)
    engine_db_login = find_login()
    engine_db_pass = find_password()
    return ip, db_path, db_var, engine_db_login, engine_db_pass


def make_dict_from_list_layers(layer_list: list) -> dict:
    nodes_with_layers = {}
    for layer in layer_list:
        node = find_node_by_layer(layer)
        if node not in nodes_with_layers:
            nodes_with_layers[node] = [layer]
        if node in nodes_with_layers:
            nodes_with_layers[node].append(layer)
    return nodes_with_layers


def make_update_with_dict(dict_with_nodes: dict):
    for node, layers in dict_with_nodes.items():
        (
            ip,
            db_path,
            db_var,
            engine_db_login,
            engine_db_pass,
        ) = find_creditails_by_node_name(node)
        for layer in layers:
            make_connection_and_update_layer(
                ip, db_path, db_var, layer, engine_db_login, engine_db_pass
            )


# def make_update_with_list(layers_list: list):
#     nodes_dict = make_dict_from_list_layers(layer_list=layers_list)
#     make_update_with_dict(nodes_dict)


# def run_proto_with_dict():
#     make_update_with_dict(node_layer_for_update)


# def run_proto_with_list():
#     make_update_with_list(layers_for_update)

def find_current_nodes_by_layers(all_data: list, layers_on_update: list) -> dict:
    result_with_nodes_and_layers = {}
    for data in all_data:
        current_node = data[0]
        current_layer = data[1]
        if current_layer in layers_on_update:
            if current_node not in result_with_nodes_and_layers:
                result_with_nodes_and_layers[current_node] = [current_layer]
            else:
                result_with_nodes_and_layers[current_node].append(current_layer)
    
    return result_with_nodes_and_layers

def update_each_layer_based_on(layer_node_info):
    for node, layer in layer_node_info.items():
        pass


def do_job():
    all_node_with_layers = get_all_creditails()
    current_info_about_node_and_layers = find_current_nodes_by_layers(all_node_with_layers, LAYERS_FOR_UPDATE)
    # где пароли логины от каждой ноды

    update_each_layer_based_on(current_info_about_node_and_layers)
