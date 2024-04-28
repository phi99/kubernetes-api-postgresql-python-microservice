from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time,socket,os
from sqlalchemy.orm import Session
from apptest import db_models, model_schemas, tools
from apptest.db_sqlalchemy import engine, get_db
from apptest.apiroutes import routes_post, routes_user, routes_auth

db_models.Base.metadata.create_all(bind=engine)

app=FastAPI()
ipadd=socket.gethostbyname(socket.gethostname())

hostip=os.environ.get('HOST_IP')
hostport=os.environ.get('HOST_PORT')

while True:

    try:
        conn=psycopg2.connect(host=HOST_IP,port=HOST_PORT,database='root',user='root',password='testpassword',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection was a success")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

app.include_router(routes_post.router)
app.include_router(routes_user.router)
app.include_router(routes_auth.router)

@app.get("/")
def root():
    return f"hello {ipadd}"
