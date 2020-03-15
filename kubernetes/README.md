Tested to work with minikube with local image.
imagePullPolicy has been set to never. Change if your image is publically available.
Image was created in minikube docker environment, which can be accessed by eval $(minikube docker-env)

Steps:
1. Create deployment. 
kubectl  apply -f deploy_cookieflask.yaml 
2. Create service.
kubectl  apply -f service_cookieflask.yaml

Servie type is NodePort currently which serves at nodePort:31444.
For minikube the node IP can be discovered by: minikube ip
