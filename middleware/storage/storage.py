import os
import logging


import psycopg2

# TODO: put this in logging package - wrap logging with desired specs
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

DBNAME = os.getenv('DBNAME')
DBUSER = os.getenv('DBUSER')
DBPASSWORD = os.getenv('DBPASSWORD')
AUTHSECRET = os.getenv('AUTHSECRET')
HOST = os.getenv('HOST')
HASH = os.getenv('HASH', 'HS256')


class Client():
    def __init__(self, id, client_id, is_admin):
        self.id = id
        self.client_id = client_id
        self.is_admin = is_admin


def block(token):
    """
    Store unauthorized token
    """
    conn = None
    query = f"insert into blocked (token) values('{token}')"
    try:
        c = 'dbname=' + DBNAME + ' user=' + DBUSER + ' password=' + DBPASSWORD + ' host=' + HOST
        logger.info('connect config: %s', c)
        logger.info('query: %s', query)
        conn = psycopg2.connect(c)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(query)
        return True
    except (Exception, psycopg2.DatabaseError) as e:
        logger.error('failed writing to postgres - blocked table: %s', e)
        return False
    finally:
        if conn:
            cur.close()
            conn.close()


def is_blocked(token):
    """
    check if token is unauthorized - does it live in `blocked` table
    """
    logger.info('verifying if token is blocked: %s', token)
    conn = None
    query = f"select count(*) from blocked where token='{token}'"
    try:
        c = 'dbname=' + DBNAME + ' user=' + DBUSER + ' password=' + DBPASSWORD + ' host=' + HOST
        logger.info('connect config: %s', c)
        conn = psycopg2.connect(c)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(query)
        record_count = cur.fetchone()[0]
        if record_count == 1:
            return True
        return False
    except (Exception, psycopg2.DatabaseError) as e:
        logger.error('failed querying postgres - blocked table: %s', e)
        return True
    finally:
        if conn:
            cur.close()
            conn.close()


def authenticate(cid, secret):
    """
    Find row matching cid, secret
    use id, cid, AUTHSECRET to encode/return new JWT
    """
    conn = None
    query = "select * from clients where \"ClientId\"=%s and \"ClientSecret\"=%s"
    try:
        c = 'dbname=' + DBNAME + ' user=' + DBUSER + ' password=' + DBPASSWORD + ' host=' + HOST
        logger.info('connect config: %s', c)
        conn = psycopg2.connect(c)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(query, (cid, secret))
        rows = cur.fetchall()
        if len(rows) != 1:
            return False
        row = rows[0]
        row_id = row[0]
        row_cid = row[1]
        admin = row[2]
        client = Client(row_id, row_cid, admin)
        return client
    except (Exception, psycopg2.DatabaseError) as e:
        logger.error('failed reading from postgres: %s', e)
        # return class with is_auth method
        return False
    finally:
        if conn:
            cur.close()
            conn.close()

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