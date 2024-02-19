.
***In Progress***
						---------------------------------------------------------------------------
						  **Implementing multitier microservices architecture in Kubernetes (k8s)**  
						----------------------------------------------------------------------------

Microservice Architecture/Traffic Flow Overview
------------------------------------------------
[client/systems] -> [k8s service (type nodeport) - for app/api] -> [k8s deployment/pod endpoint - for app/api] -> [k8s service (type cluster IP) - for postgresql] ->  [k8s deployment/pod endpoint - for postgresql]


Networking Implementation
---------------------------
Client traffic/request would connect to the k8s service of nodeport type (the destination ip from client would be the node ip address, with nodeport service the node is set to receive traffic on the configured nodeport and forward the traffic to its endpoint that is listening on the port configured in the service config), the service would forward the traffic to one of its endpoint which is a pod that is being managed under deployment resource (the endpoints were part of the service based on label), based on the request, the app would perform the task requested by communicating with the backend db via the service for db. the db service is of cluster IP type. Cluster IP type would be more suitable because it's not exposing itself to the external traffic, only traffic within the cluster can access the db service. 

When there's connection destined to service IP, the kube-proxy intercepts the connection and redirect the packets to a randomly selected backend pod without passing them to actual proxy server which seem to also shown by the output of tcpdump at the api pod

Database/Postgresql implementation
-----------------------------------
The database is implemented utilizing Postgresql. k8s configmap resource was used to provide the config options needed for the postgresql image to run in the k8s deployment. 
k8s persistent volume and persistent volume resource claim was used to provide persistent storage for the postgresql, so that even if the container process/pod is destroyed in the deployment and recreated, the database would persist and accessible on the new pod/deployment.

App/API implementation and Docker image
----------------------------------------
The app is implemented using python and its api framework called fastapi in Linux environment. The api is set to listens to TCP port 8000 and the Docker image is created by building Docker
file. Configmap is also used to set the config options/environment variable.
