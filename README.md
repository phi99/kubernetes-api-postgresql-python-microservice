.
***In Progress**

	 	 	   ----------------------------------------------------------------
	     	    	     **Multitier microservices architecture in Kubernetes (k8s)**
	  	 	   ----------------------------------------------------------------

```text
Microservice Architecture/Traffic Flow Overview
-------------------------------------------------
[client/systems] -> [k8s service (type nodeport) - for app/api] -> [k8s deployment/pod endpoint - for app/api] -> [k8s service (type cluster IP) - for postgresql] ->  [k8s deployment/pod endpoint - for postgresql]
```

```text
Networking Implementation
---------------------------
Client traffic/request would connect to the k8s service of nodeport type (the destination ip from client would be the node ip address, with nodeport service the node is set to receive traffic on the configured nodeport and forward the traffic to its endpoint that is listening on the port configured in the service config), the service would forward the traffic to one of its endpoint which is a pod that is being managed under deployment resource (the endpoints were part of the service based on label), based on the request, the app would perform the task requested by communicating with the backend db via the service for db. the db service is of cluster IP type. Cluster IP type would be more suitable because it's not exposing itself to the external traffic, only traffic within the cluster can access the db service. 
When there's connection destined to service IP, the kube-proxy intercepts the connection and redirect the packets to a randomly selected backend pod without passing them to actual proxy server which seem to also shown by the output of tcpdump at the api pod

Database/Postgresql implementation
-----------------------------------
The database is implemented utilizing Postgresql. k8s configmap resource was used to provide the config options needed for the postgresql image to run in the k8s deployment. 
K8s persistent volume and persistent volume resource claim was used to provide persistent storage for the postgresql, so that even if the container process/pod is destroyed in the deployment and recreated, the database would persist and accessible on the new pod/deployment.

App/API implementation and Docker image
----------------------------------------
The app is implemented using python and its api framework called fastapi in Linux environment. The api is set to listens to TCP port 8000 and the Docker image is created by building Docker
file. Configmap is also used to set the config options/environment variable.
```
```text
[k8 service for app/api] 
-------------------------
apiVersion: v1
kind: Service
metadata:
  name: test-api
  labels:
    app: test-api
spec:
  ports:
  - port: 8000
    nodePort: 30008
  selector:
    app: test-api
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
  creationTimestamp: null
  labels:
    app: test-api
  name: test-api
  namespace: test-namespace
spec:
  replicas: 1
  selector:
    matchLabels:
      app: test-api
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: test-api
    spec:
      containers:
      - image: imagetestenv_new
        imagePullPolicy: Never
        ports:
          - containerPort: 8000
        envFrom:
          - configMapRef:
              name: api-configmap
        name: test-api-container
        command: ["uvicorn","--host","0.0.0.0","testmain:app"]


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
  name: api-configmap
  labels:
    app: test-api
data:
  POSTGRES_USER: 
  POSTGRES_PASSWORD: 
  SVC_DB_PORT: "5432"
  SVC_DB: test-postgres2
  TARGET_DB: root

configmap is for providing env var for the app

[k8 service - for postgresql type ClusterIP]
--------------------------------------------
apiVersion: v1
kind: Service
metadata:
  creationTimestamp: 
  labels:
    app: test-postgres2
  name: test-postgres2
  namespace: test-namespace
  resourceVersion: 
  uid: 
spec:
  clusterIP: 10.109.77.134
  clusterIPs:
  - 10.109.77.134
  internalTrafficPolicy: Cluster
  ipFamilies:
  - IPv4
  ipFamilyPolicy: SingleStack
  ports:
  - port: 5432
    protocol: TCP
    targetPort: 5432
  selector:
    app: test-postgres2
  sessionAffinity: None
  type: ClusterIP
status:
  loadBalancer: {}

[k8 deployment/pod - for postgresql]
-------------------------------------
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: test-postgres2
  name: test-postgres2
  namespace: test-namespace
spec:
  replicas: 1
  selector:
    matchLabels:
      app: test-postgres2
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: test-postgres2
    spec:
      containers:
      - image: postgres
        imagePullPolicy: Never
        ports:
          - containerPort: 5432
        envFrom:
          - configMapRef:
              name: postgres-configmap
        name: test-postgres2
        volumeMounts:
          - mountPath: /var/lib/postgresql/data
            name: postgresvol
      volumes:
        - name: postgresvol
          persistentVolumeClaim:
            claimName: postgres-pvc

Notes:
-similar with deployment for the app
-the deployment for the postgresql uses persistent volume claim and volume mounts in the container to make the database persistent
 

Persistent Volume for Postgresql
---------------------------------
kind: PersistentVolume
apiVersion: v1
metadata:
  name: postgres-pv
  labels:
    type: local
    app: test-postgres2
spec:
  storageClassName: manual1
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteMany
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
  name: postgres-pvc
  labels:
    app: test-postgres2
spec:
  storageClassName: manual1
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 5Gi

Notes:
-pvc is used to bind/use the pv to be used on the pod 
-storageclassname could be used as selector (to inform which pv to bind to)

configmap for Postgresql
------------------------
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgres-configmap
  labels:
    app: test-postgres
data:
  POSTGRES_USER: 
  POSTGRES_PASSWORD: 

Notes:
-configmap used to set env var for postgresql
```

