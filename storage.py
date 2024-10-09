import os
import json
import logging

import psycopg2

# TODO: put this in logging package - wrap logging with desired specs
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

DBNAME = os.getenv('DBNAME')
DBUSER = os.getenv('DBUSER')
DBPASSWORD = os.getenv("DBPASSWORD")
AUTHSECRET = os.getenv("AUTHSECRET")
HOST = os.getenv("HOST")

def create(cid, secret, is_admin):
    """
    New record into clients table
    """
    conn = None
    query = "insert into clients (\"ClientId\", \"ClientSecret\", \"IsAdmin\") values(%s,%s,%s)"
    try:
        c = 'dbname=' + DBNAME + ' user=' + DBUSER +' password=' +DBPASSWORD +' host=' +HOST
        logger.info('connect config: %s', c)
        conn = psycopg2.connect(c)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(query, (cid, secret, is_admin))
        return True
    except (Exception, psycopg2.DatabaseError) as e:
        logger.error('failed writing to postgres: %s', e)
        return False
    finally:
        if conn:
            cur.close()
            conn.close()