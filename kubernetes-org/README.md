Tested to work with cloudera k8s.

Steps:
1. Create deployment. 
kubectl  apply -f deploy_cookieflask.yaml 
2. Create service.
kubectl  apply -f service_cookieflask.yaml

Servie type is loadBalancer which uses internal load balancing.
https://cloud.google.com/kubernetes-engine/docs/how-to/internal-load-balancing
