import pymysql
import json
import logging

import middleware.context as context

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _get_db_connection():

    db_connect_info = context.get_db_info()

    logger.info("RDBService._get_db_connection:")
    logger.info("\t HOST = " + db_connect_info['host'])

    db_info = context.get_db_info()
    db_connection = pymysql.connect(
       **db_info
    )
    return db_connection


def get_by_prefix(db_schema, table_name, column_name, value_prefix):

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name + " where " + \
        column_name + " like " + "'" + value_prefix + "%'"
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()

    conn.close()

    return res


def _get_where_clause_args(template):

    terms = []
    args = []
    clause = None

    if template is None or template == {}:
        clause = ""
        args = None
    else:
        for k,v in template.items():
            terms.append(k + "=%s")
            args.append(v)

        clause = " where " +  " AND ".join(terms)
    return clause, args


def _get_insert_clause_args(template):

    terms = []
    args = []
    clause = None

    if template is None or template == {}:
        clause = ""
        args = None
    else:
        for k,v in template.items():
            terms.append("%s")
            args.append(v)

        clause = " , ".join(terms)

    return clause, args

def _get_update_clause_args( template,id):
    terms = []
    args = []
    clause = None

    if template is None or template == {}:
        clause = ""
        args = None
    else:
        for k, v in template.items():
            terms.append(k + "=%s")
            args.append(v)

        clause = " , ".join(terms) + "  WHERE ID="+ str(id)

    return clause, args

def _get_delete_clause_args(id):
    terms = []
    args = []
    clause = None

    if id is None or id == {}:
        clause = ""
        args = None
    else:
        clause = 'ID=%s'
        args.append(id)

    return clause, args

def find_by_template(db_schema, table_name, template, field_list):

    wc,args = _get_where_clause_args(template)

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name + " " + wc
    res = cur.execute(sql, args=args)
    res = cur.fetchall()

    conn.close()

    return res

def find_by_template_limit(db_schema, table_name, template, field_list):
    qs={}
    limit=0
    offset=0
    for k,v in template.items():
        if k=='offset':
            offset=v
        elif k=='limit':
            limit=v
        else:
            qs[k]=v

    wc, args = _get_where_clause_args(qs)

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name + " " + wc + 'limit '+str(limit)+ ' offset '+str(offset)
    #print(sql)
    res = cur.execute(sql, args=args)
    res = cur.fetchall()

    conn.close()

    return res



def insert_by_template(db_schema, table_name, template, field_list):
    conn = _get_db_connection()
    cur = conn.cursor()
    wc,args = _get_insert_clause_args(template)

    sql = "INSERT INTO " + db_schema + "." + table_name + " VALUES (" + wc + ');'
    try:
        res = cur.execute(sql, args=args)
        conn.commit()
        conn.close()
    except Exception as e:
        if type(e)==pymysql.err.IntegrityError:
            res='integrity error'
    return res

def update_by_id(db_schema, table_name, template,id):
    conn = _get_db_connection()
    cur = conn.cursor()
    wc, args = _get_update_clause_args(template,id)

    sql = "UPDATE " + db_schema + "." + table_name + " SET " + wc
    res = cur.execute(sql, args=args)

    conn.commit()
    conn.close()

    return res

def delete_by_id(db_schema, table_name, id):
    conn = _get_db_connection()
    cur = conn.cursor()
    wc, args = _get_delete_clause_args(id)

    sql = "DELETE FROM " + db_schema + "." + table_name + " WHERE " + wc
    res = cur.execute(sql, args=args)

    conn.commit()
    conn.close()

    return res

def get_address_by_userid(db_schema,table_name1,table_name2,template):
    conn = _get_db_connection()
    cur = conn.cursor()
    wc,args = _get_where_clause_args(template)

    sql = "SELECT * FROM "+ db_schema + "." + table_name1 + " where ID = ( SELECT addressID FROM " + db_schema + "." + table_name2 + "" + wc + ')'
    res = cur.execute(sql, args=args)
    res = cur.fetchall()
    conn.close()

    return res

def get_users_by_addressid(db_schema,table_name,template):
    conn = _get_db_connection()
    cur = conn.cursor()
    wc, args = _get_where_clause_args(template)

    sql = "SELECT * FROM "+ db_schema + "." + table_name + wc
    res = cur.execute(sql, args=args)
    res = cur.fetchall()
    conn.close()

    return res




