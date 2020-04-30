# Pythonservice


Requirements:

·        A service written in python or golang that queries 2 urls (https://httpstat.us/503 & https://httpstat.us/200)

·        The service will check the external urls (https://httpstat.us/503 & https://httpstat.us/200 ) are up (based on http status code 200) and response time in milliseconds

·        The service will run a simple http service that produces  metrics (on /metrics) and output a prometheus format when hitting the service /metrics url

·   Expected response format:

§  sample_external_url_up{url="https://httpstat.us/503 "}  = 0

§  sample_external_url_response_ms{url="https://httpstat.us/503 "}  = [value]

§  sample_external_url_up{url="https://httpstat.us/200 "}  = 1

§  sample_external_url_response_ms{url="https://httpstat.us/200 "}  = [value]


## Repository :
```bash
   git : https://github.com/shabarishetty46/Pythonservice.git
   dockerhub image:docker pull shetty12345/pythonservice
   Service Type  : Cluster IP 
  ```



Deployment Procedure:

## Installation

Clone the repository 

```bash
git clone https://github.com/shabarishetty46/Pythonservice.git
```
## Folder

```bash
[cloud_user@shettyaws1234c Pythonservice]$ ll
total 24
-rw-rw-r--. 1 cloud_user cloud_user  284 Apr 30 11:54 Dockerfile
-rw-rw-r--. 1 cloud_user cloud_user   17 Apr 30 11:49 packages.txt
-rw-rw-r--. 1 cloud_user cloud_user  653 Apr 30 11:46 pythonservice.py
-rw-rw-r--. 1 cloud_user cloud_user  565 Apr 30 13:07 pythonservice.yml
-rw-rw-r--. 1 cloud_user cloud_user 6378 Apr 30 13:28 README.md

```



## Python Script output 

```python
[cloud_user@shettyaws1234c Pythonservice]$ python pythonservice.py
sample_external_url_up{url="https://httpstat.us/503"}=0
sample_external_url_response_ms{url="https://httpstat.us/503"}=0.45
sample_external_url_up{url="https://httpstat.us/200"}=1
sample_external_url_response_ms{url="https://httpstat.us/200"}=0.13
[cloud_user@shettyaws1234c Pythonservice]$
```

## Build a Docker Image from the Dockerfile

```bash
sudo docker build -t shetty12345/pythonservice:v1 .
```

## Docker image 

```bash
[cloud_user@shettyaws1234c Pythonservice]$ sudo docker images
REPOSITORY                           TAG                 IMAGE ID            CREATED              SIZE
shetty12345/pythonservice            v1                  d760e3e62387        About a minute ago   923 MB
```
## Push the docker Image to dockerhub

```bash
[cloud_user@shettyaws1234c Pythonservice]$ sudo docker push shetty12345/pythonservice
The push refers to a repository [docker.io/shetty12345/pythonservice]
```


## Test the Docker image 

```bash
[cloud_user@shettyaws1234c Pythonservice]$ sudo docker run -it -p 80:80 shetty12345/pythonservice:v1
sample_external_url_up{url="https://httpstat.us/503"}=0
sample_external_url_response_ms{url="https://httpstat.us/503"}=0.15
sample_external_url_up{url="https://httpstat.us/200"}=1
sample_external_url_response_ms{url="https://httpstat.us/200"}=0.1
[cloud_user@shettyaws1234c Pythonservice]$

```

## Check for the master and worker nodes

```bash
[cloud_user@shettyaws1234c ~]$ kubectl get nodes
NAME                             STATUS   ROLES    AGE     VERSION
shettyaws1232c.mylabserver.com   Ready    <none>   63s     v1.18.2
shettyaws1233c.mylabserver.com   Ready    <none>   3m21s   v1.18.2
shettyaws1234c.mylabserver.com   Ready    master   76m     v1.18.2
[cloud_user@shettyaws1234c ~]$
```
## Deploy the pythonservice.yml

```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: python-service
spec:
  selector:
    matchLabels:
      app: python-service
  replicas: 3
  template:
    metadata:
      labels:
        app:
    spec:
      containers:
      - name: python-service
        image: shetty12345/pythonservice:v1
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: python-service
  name: python-service
  namespace: default
spec:
  type: ClusterIP
  ports:
    - port: 80
  selector:
    app: python-service

[cloud_user@shettyaws1234c ~]$
```

```bash
[cloud_user@shettyaws1234c Pythonservice]$ sudo kubectl apply -f pythonservice.yml --kubeconfig=/etc/kubernetes/admin.conf
deployment.apps/python-service created
service/python-service created
```

## Check for Deployment
```bash
[cloud_user@shettyaws1234c Pythonservice]$ kubectl get deployments
NAME             READY   UP-TO-DATE   AVAILABLE   AGE
python-service   0/3     3            0           
```
## Check for service
```bash
[cloud_user@shettyaws1234c Pythonservice]$ kubectl get svc
NAME             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
kubernetes       ClusterIP   10.96.0.1       <none>        443/TCP   85m
python-service   ClusterIP   10.110.145.57   <none>        80/TCP    3m6s         
```
## check for running pods

```bash
[cloud_user@shettyaws1234c Pythonservice]$ kubectl get pods -o wide
NAME                              READY   STATUS    RESTARTS   AGE    IP          NODE                             NOMINATED NODE   READINESS GATES
python-service-6c84db7cb7-27crl   1/1     Running   0          111s   10.38.0.0   shettyaws1232c.mylabserver.com   <none>           <none>
python-service-6c84db7cb7-4w5jk   1/1     Running   0          113s   10.40.0.1   shettyaws1233c.mylabserver.com   <none>           <none>
python-service-6c84db7cb7-gzsqg   1/1     Running   0          109s   10.40.0.2   shettyaws1233c.mylabserver.com   <none>           <none>
[cloud_user@shettyaws1234c Pythonservice]$
```

## Describe svc

```bash
[cloud_user@shettyaws1234c Pythonservice]$ kubectl describe svc python-service
Name:              python-service
Namespace:         default
Labels:            app=python-service
Annotations:       Selector:  app=python-service
Type:              ClusterIP
IP:                10.110.145.57
Port:              <unset>  80/TCP
TargetPort:        80/TCP
Endpoints:         10.38.0.0:80,10.40.0.1:80
Session Affinity:  None
Events:            <none>
[cloud_user@shettyaws1234c Pythonservice]$
       
```

## Check for end point 

```bash 
[cloud_user@shettyaws1234c Pythonservice]$ kubectl get ep
NAME             ENDPOINTS                   AGE
kubernetes       172.31.109.181:6443         104m
python-service   10.38.0.0:80,10.40.0.1:80   22m
[cloud_user@shettyaws1234c Pythonservice]$
```


## Access the node via CLuseter Ip

```bash
cloud_user@shettyaws1234c Pythonservice]$ sudo kubectl exec -it python-service-6c84db7cb7-27crl  curl 10.110.145.57:80 --kubeconfig=/etc/kubernetes/admin.conf
kubectl exec [POD] [COMMAND] is DEPRECATED and will be removed in a future version. Use kubectl kubectl exec [POD] -- [COMMAND] instead.
sample_external_url_up{url="https://httpstat.us/503"}=0
sample_external_url_response_ms{url="https://httpstat.us/503"}=0.55
sample_external_url_up{url="https://httpstat.us/200"}=1
sample_external_url_response_ms{url="https://httpstat.us/200"}=0.25

```
