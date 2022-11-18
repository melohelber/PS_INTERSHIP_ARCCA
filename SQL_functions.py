import psycopg2
import math, time
import numpy as np
import pandas as pd


host = 'database-1.cqmgr5myhr8z.us-east-1.rds.amazonaws.com'
database = 'PS_ARCCA'
user = 'pelots'
password = 'pelots123'
port = '5432'

def connect_db():
  conn = psycopg2.connect(host=host, 
                         database=database,
                         user=user, 
                         password=password,
                         port = port)
  return conn

def check_connection(conn):
    try:
        cur = conn.cursor()
        connected = True
        return conn
    except:
        connected = False
        return connect_db()

def create_db(conn, sql):
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()

#http://127.0.0.1/pgadmin4

def check_exists(conn, name):
    sql = "SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename  = '%s')"%(name)
    # print(sql)
    # conn = connect_db()
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchone()[0]

def get_table_row_count(conn, name):
    sql = "SELECT count(*) AS exact_count FROM public.%s;"%(name)
    # print(sql)
    # conn = connect_db()
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchone()[0]

def get_links(conn, name):
    sql = "SELECT trip_advisor_url FROM public.%s"%name
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()

def get_table_last_rvw_date_ID(conn, name):
    # sql = "SELECT MAX (review_at) FROM public.%s;"%(name)
    # print(sql)
    # conn = connect_db()
    sql = "SELECT id_review, review_at FROM public.%s WHERE review_at=(SELECT MAX(review_at) FROM public.%s);"%(name, name)
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


def create_table(conn, name):
    # [['id_review' ,'user', 'userloc', 'n_reviews','title', 'link_review', 'text', 'score', 'review_at', 'visit_at', 'response_by', 'response_date', 'response']]
    sql = '''CREATE TABLE IF NOT EXISTS public.%s (
            id_review      SERIAL PRIMARY KEY,
            user_          VARCHAR ( 50 ),
            userloc        VARCHAR ( 50 ),
            n_reviews      INT,
            title          VARCHAR ( 1000 ),
            link_review    VARCHAR ( 1000 ),
            text_          VARCHAR ( 10000000 ),
            score          INT,
            review_at      DATE DEFAULT NULL,
            visit_at       DATE DEFAULT NULL,
            response_by    VARCHAR ( 50 ),
            response_date  DATE DEFAULT NULL,
            response       VARCHAR ( 10000000 )
            );'''%(name)
    create_db(conn, sql)

def insert_data(conn, sql):
    cur = conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cur.close()
        return 1
    # cur.close()

def insert_all_DF_Data(conn, df, name):
    for i in df.index:
        sql = '''
        INSERT into public.%s (id_review,user_,userloc,n_reviews,title,link_review,text_,score,review_at,visit_at,response_by,response_date,response) 
        values(
        ''' %name
        for k in df.columns:
            if df[k][i] != '' and df[k][i] != pd.NaT and df[k][i] != 'NaT':
                sql = sql+"'"+str(df[k][i])+"'"
            else:
                sql = sql+'NULL'
            if k != 'response':
                sql = sql+','
        sql = sql+');'

        insert_data(conn, sql)

def insert_all_DF_Data_urls(conn, df, name):
    for i in df.index:
        sql = '''
        INSERT into public.%s (store_id,store_name,trip_advisor_url) 
        values(
        ''' %name
        for k in df.columns:
            if df[k][i] != '' and df[k][i] != pd.NaT and df[k][i] != 'NaT':
                sql = sql+"'"+str(df[k][i])+"'"
            else:
                sql = sql+'NULL'
            if k != 'trip_advisor_url':
                sql = sql+','
        sql = sql+');'
        print(sql)
        input('vai?')
        insert_data(conn, sql)