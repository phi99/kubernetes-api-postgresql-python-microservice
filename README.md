.
***In Progress**

	 	 	   ----------------------------------------------------------------
	     	    	     **Multitier microservices architecture in Kubernetes (K8s)**
	  	 	   ----------------------------------------------------------------

```text
Microservice Architecture/Traffic Flow Overview
-------------------------------------------------
[client/systems] -> [k8s service (type nodeport) - for App/API] -> [k8s deployment/pod endpoint - for App/API] -> [k8s service (type cluster IP) - for postgresql] ->  [k8s deployment/pod endpoint - for postgresql]
```

```text
Networking Implementation
---------------------------
Client traffic/request would connect to the k8s service of nodeport type (the destination ip from client would be the node ip address, with nodeport service the node is set to receive traffic on the configured nodeport and forward the traffic to its endpoint that is listening on the port configured in the service config), the service would forward the traffic to one of its endpoint which is a pod that is being managed under deployment resource (the endpoints were part of the service based on label), based on the request, the app would perform the task requested by communicating with the backend db via the service for db. the db service is of cluster IP type. Cluster IP type would be more suitable because it's not exposing itself to the external traffic, only traffic within the cluster can access the db service. 
When there's connection destined to service IP, the kube-proxy intercepts the connection and redirect the packets to a randomly selected backend pod without passing them to actual proxy server which seem to also shown by the output of tcpdump at the API pod

Database/Postgresql implementation
-----------------------------------
The database is implemented utilizing Postgresql.
K8s configmap resource is utilized to provide the config options needed for the postgresql image to run in the k8s deployment. 
K8s persistent volume and persistent volume resource claim was used to provide persistent storage for the postgresql, so that even if the container process/pod is destroyed in the deployment and recreated, the database would persist and accessible on the new pod/deployment.

App/API implementation
----------------------------------------
The App is implemented using python and its api framework called fastapi in Linux environment.
The API is set to listens to TCP port 8000. 
Configmap is also used to set the config options/environment variable.
```
```text
[k8 service for app/api] 
-------------------------
apiVersion: v1
kind: Service
metadata:
  name: 
  labels:
    app: 
spec:
  ports:
  - port: 
    nodePort: 
  selector:
    app: 
  type: NodePort

Notes:
-ingress traffic access the app via service nodeport resource that uses the node ip address and port, upon receiving the traffic the node would forward the traffic to the
endpoint pods
-nodeport is the port on the node that the ingress traffic would connect to
-port is the port that the app is listening on in the pod container
-selector is the label used to select which pod would be the endpoint for the service

cluster ip - user/traffic external from the cluster not able to access the db directly 

[k8 deployment - for api/app]
----------------------------------------
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: 
  labels:
    app: 
  name: 
  namespace: 
spec:
  replicas: 
  selector:
    matchLabels:
      app: 
  strategy: {}
  template:
    metadata:
      creationTimestamp: 
      labels:
        app: 
    spec:
      containers:
      - image: 
        imagePullPolicy: 
        ports:
          - containerPort: 
        envFrom:
          - configMapRef:
              name: 
        name: 
        command: 


Note:
-The pods serve as the endpoints for the services and being created by using Deployment resource as it has features such as replica set to easily scale the pod, and
resilience/high availability as it would ensure that when the pod crash the deployment would create a new pod such that it maintains the desired number of pod replica.
-replica parameter is used to control the number of pods within the deployment
-selector parameter is used to know which pod is a member of the deployment
-templates are used as the template to create the pod so the pods within the deployment are uniform following the template
-the container section is used to specify the container parameters such as the image, commands to run in the container

k8 configmap for app
---------------------
apiVersion: v1
kind: ConfigMap
metadata:
  name: 
  labels:
    app: 
data:
  POSTGRES_USER: 
  POSTGRES_PASSWORD: 
  SVC_DB_PORT: 
  SVC_DB: 
  TARGET_DB: 

configmap is for providing env var for the app

[k8 service - for postgresql type ClusterIP]
--------------------------------------------
apiVersion: v1
kind: Service
metadata:
  creationTimestamp: 
  labels:
    app: 
  name: 
  namespace: 
  resourceVersion: 
  uid: 
spec:
  clusterIP: 
  clusterIPs:
  - 
  internalTrafficPolicy: 
  ipFamilies:
  - IPv4
  ipFamilyPolicy: 
  ports:
  - port: 
    protocol: 
    targetPort: 
  selector:
    app: 
  sessionAffinity: 
  type: 
status:
  loadBalancer: {}

[k8 deployment/pod - for postgresql]
-------------------------------------
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: 
  labels:
    app: 
  name: 
  namespace: 
spec:
  replicas: 
  selector:
    matchLabels:
      app: 
  strategy: {}
  template:
    metadata:
      creationTimestamp: 
      labels:
        app: 
    spec:
      containers:
      - image: 
        imagePullPolicy:
        ports:
          - containerPort: 
        envFrom:
          - configMapRef:
              name: 
        name: 
        volumeMounts:
          - mountPath: 
            name: 
      volumes:
        - name: 
          persistentVolumeClaim:
            claimName: 

Notes:
-similar with deployment for the app
-the deployment for the postgresql uses persistent volume claim and volume mounts in the container to make the database persistent
 

Persistent Volume for Postgresql
---------------------------------
kind: PersistentVolume
apiVersion: v1
metadata:
  name: 
  labels:
    type: 
    app: 
spec:
  storageClassName: 
  capacity:
    storage: 
  accessModes:
    - 
  hostPath:
    path: 

Note:
-persistent vol-> the function of pv is to describe the underlying storage to k8 api
the function of pv is to inform the k8 api of the underlying storage

Persistent Volume Claim for Postgresql
---------------------------------------
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: 
  labels:
    app: 
spec:
  storageClassName: 
  accessModes:
    - 
  resources:
    requests:
      storage: 

Notes:
-pvc is used to bind/use the pv to be used on the pod 
-storageclassname could be used as selector (to inform which pv to bind to)

configmap for Postgresql
------------------------
apiVersion: v1
kind: ConfigMap
metadata:
  name: 
  labels:
    app: 
data:
  POSTGRES_USER: 
  POSTGRES_PASSWORD: 

Notes:
-configmap used to set env var for postgresql

Fastapi Script
---------------
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
```
