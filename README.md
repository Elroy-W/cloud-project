# CSIT6000O Project
**Shopping Cart Web Application**


|Name|SID| EMAIL                  | CONTRIBUTION                              |
|---|---|------------------------|-------------------------------------------|
|WANG Enru|20906987| ewangag@connect.ust.hk | 25%                                       |
|WANG Zhetian|20879172| zwangiu@connect.ust.hk                | 25%        |
|ZENG Zhaobo|20881656| zzengaw@connect.ust.hk               | 25%              |
|JIANG Guanxi|20882296| gjiangac@connect.ust.hk               | 25%  |

**Testing Environment**

||                                    |
|---|------------------------------------|
|OS| Ubuntu Server 22.04 TLS            |
|Architecture| 64-bit(x86)                        |
|Instance Type| M5.large                           |
|Network| Public Subnet with public IP       |
|SG| TCP Ports: 80, 8080 From: Anywhere |
|Storage| 50GiB gp2 on Root volume           |

## Infrastructure

## Deployment
### Setup
To setup the environment, some packages need to be installed.

| Package | Description |
| --- | --- |
| minikube | Single-node local k8s cluster |
| kubectl | CLI to control k8s cluster |
| docker | All the components of the project is deployed as Docker images |
| socat | Support port forwarding to expose service of k8s cluster |
| conntrack | Support starting Minikube with none driver |
| arkade | Marketplace for Openfaas in k8s |
| faas-cli | CLI to build/delpoy openfaas functions |

Run the following commands for environment setting

```
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

sudo apt-get update && sudo apt-get install docker.io -y
sudo apt-get install socat -y
sudo apt-get install -y conntrack
curl -sL https://cli.openfaas.com | sudo sh
curl -sLS https://get.arkade.dev | sudo sh
```
Set the hosts
```
vim /etc/hosts
127.0.0.1 app.shopping-cart.com
127.0.0.1 db.shopping-cart.com
127.0.0.1 faas.shopping-cart.com
```
Before deploying the project, the root privilege is required

Start minikube
```angular2html
sudo -i
minikube start --kubernetes-version=v1.22.0 HTTP_PROXY=https://minikube.sigs.k8s.io/docs/reference/networking/proxy/ --driver=none
minikube addons enable ingress  # Start minikube ingress service for nginx
kubectl get pods -n ingress-nginx # Check status for nginx
```
Deploy Openfass
```angular2html
arkade install openfaas --basic-auth-password password123 --set=faasIdler.dryRun=false
kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode # Check Password
```
Port-forwarding for Openfaas Gateway
```angular2html
kubectl port-forward -n openfaas svc/gateway 8080:8080 --address=0.0.0.0 &
```
Deploy Nginx
```angular2html
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.2.0/deploy/static/provider/cloud/deploy.yaml
```
Deploy the project
```angular2html
kubectl apply -f ${REPO_HOME}/mongodb.yml
kubectl apply -f ${REPO_HOME}/server.yml
kubectl apply -f ${REPO_HOME}/namespace.yml
kubectl apply -f ${REPO_HOME}/faas-ingress.yml
```
Port-forwarding for frontend 
```angular2html
kubectl port-forward -n openfaas-fn svc/frontend-service 80:8080 --address=0.0.0.0 &
```
Deploy Openfaas Functions
```angular2html
faas-cli login --username admin --password ${password}
cd ${REPO_HOME}/faas
faas-cli template store pull python3-http
faas-cli deploy -f stack.yml
```

## Testing Backend Services
```angular2html
curl -X GET -b carId=5a2b4235-7f43-4d26-9912-0f76bc914ec6 http://44.200.19.187:8080/function/get-products

curl -i http://44.200.19.187/function/get-product/e173d669-b449-4226-af2e-128142abdd30 

curl -b cartId=5a2b4235-7f43-4d26-9912-0f76bc914ec6 -i http://44.200.19.187:8080/function/list-cart

curl -b cartId=5a2b4235-7f43-4d26-9912-0f76bc914ec6 -d '{"quantity": 1551, "productId": "e173d669-b449-4226-af2e-128142abdd30"}' -i http://44.200.19.187:8080/function/update-cart

curl -X POST -H "Content-Type: application/json" -d '{"quantity": 1551, "productId": "e173d669-b449-4226-af2e-128142abdd30"}' -i http://44.200.19.187:8080/function/update-cart -b cartId=5a2b4235-7f43-4d26-9912-0f76bc914ec6

curl -X GET -b cartId=5a2b4235-7f43-4d26-9912-0f76bc914ec6 -i http://44.200.19.187:8080/function/checkout-cart
```



