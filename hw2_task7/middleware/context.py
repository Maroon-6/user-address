import json
import os

# This is a bad place for this import
import pymysql

helper_dict={
    "SMARTY":{
        "auth_id":"f490c860-a50e-794c-e462-e2051560fd32",
        "auth_token":"30jhPqGd50tYzN2Pz9Ww"
    }
}

def get_db_info():
    """
    This is crappy code.

    :return: A dictionary with connect info for MySQL
    """
    db_host = os.environ.get("DBHOST", None)
    db_user = os.environ.get("DBUSER", None)
    db_password = os.environ.get("DBPASSWORD", None)

    if db_host is not None:
        db_info = {
            "host": db_host,
            "user": db_user,
            "password": db_password,
            "cursorclass": pymysql.cursors.DictCursor
        }
    else:
        # db_info = {
        #     "host": "localhost",
        #     "user": "dbuser",
        #     "password": "dbuserdbuser",
        #     "cursorclass": pymysql.cursors.DictCursor
        # }
        db_info = {
            "host": "maroon-6-database.cpi1wds87i9t.us-east-1.rds.amazonaws.com",
            "user": "admin",
            "password": "ABC123!#",
            "cursorclass": pymysql.cursors.DictCursor
        }

    return db_info

def get_context(context_name):
    #result=os.environ.get(context_name,None)
    result=helper_dict[context_name]
    if result is not None:
        try:
            tmp=json.loads(result)
            result=tmp
        except:
            pass
    return result


