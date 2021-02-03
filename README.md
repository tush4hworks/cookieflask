# cookieflask
**Use k8s to wrap docker to wrap flask to wrap selenium**


![Alt text](images/layers.png?raw=true "Title")


We can now interact directly with the REST endpoints exposed by the service to fetch cookies.

It currently exposes two endpoints:

POST /api/cookie : Gives a list of all cookies upon successful login

POST /api/cookie/<cookiename> : Gives specific cookie (by cookiename), if found, else null.

The payload to these requests looks like:

_Necessary params:_

`````{
"baseurl":"https://44.232.15.145:8443/auth/realms/cdpe2e-mow-stage-realm/protocol/saml/clients/samlclient",
"username":"cdpe2e_stagecookieuser@keycloak.com",
"password":"password"
}
`````

_With optional params:_

```
{
"baseurl":"https://44.232.15.145:8443/auth/realms/cdpe2e-mow-stage-realm/protocol/saml/clients/samlclient",
"username":"cdpe2e_stagecookieuser@keycloak.com",
"password":"password",
"username_finder": {"findby":"id", "value":"username id"},
"password_finder":{"findby":"name", "value":"password"},
"button_finder":{"findby":"xpath","value":"//*[@type='submit']"}
}

```

###### How it works:

Request gets routed to one of the pods in k8 deployment.
Flask triggers selenium function to login to baseurl with username, password provided.
Upon successful login it returns session cookies.



###### Selenium logic:

The base method is based on the assumption that a generic login page will always have 3 elements:
Username box
Password box
Submit button

The default finders to locate them are specified as (they are consistent with keycloak and okta):
```
username_finder = finder('name','username')
password_finder = finder('name', 'password')
button_finder = finder('xpath','//*[@type="submit"]')

```
However they can be overridden by the user who makes the request by specifying them in optional params as mentioned above.

It works for all of these selenium locators:
```
['find_element_by_class_name', 'find_element_by_css_selector', 'find_element_by_id', 'find_element_by_link_text', 'find_element_by_name', 'find_element_by_partial_link_text', 'find_element_by_tag_name', 'find_element_by_xpath']

```
If a user wants to override, he has to specify the method suffix after find_element_by_, for example in case he wants the username to be located by class_name, he can provide this attribute in his request:
"username_finder": {"findby":"class_name", "value":"username class"}


###### UI:

The service can also be accessed from UI at https://10.101.91.63/UI/


###### Kubernetes:

It's currently deployed in my namespace with 3 replicas.
A service of type loadbalancer is used to route traffic to them which is then exposed by ingress.

In case deployment, service is deleted, the ingress IP remains the same, so we can rely on that.
In case ingress itself gets deleted, we have to get new ingress IP.

Ingress usually works on hostname, however the entry has to be added to /etc/hosts for it to work.


_Live Ingress:_

```kubectl get ingress milkbikisv2  -n tsharma -o yaml

apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"extensions/v1beta1","kind":"Ingress","metadata":{"annotations":{},"name":"milkbikisv2","namespace":"tsharma"},"spec":{"rules":[{"http":{"paths":[{"backend":{"serviceName":"cookieflaskservicev2","servicePort":5001},"path":"/"},{"backend":{"serviceName":"cookieflaskservicev2","servicePort":5002},"path":"/UI"}]}}]}}
  creationTimestamp: "2020-09-11T07:46:05Z"
  generation: 1
  name: milkbikisv2
  namespace: tsharma
  resourceVersion: "90297892"
  selfLink: /apis/extensions/v1beta1/namespaces/tsharma/ingresses/milkbikisv2
  uid: d93483fb-f402-11ea-9293-14187746a76d
spec:
  rules:
  - http:
      paths:
      - backend:
          serviceName: cookieflaskservicev2
          servicePort: 5001
        path: /
      - backend:
          serviceName: cookieflaskservicev2
          servicePort: 5002
        path: /UI
status:
  loadBalancer:
    ingress:
    - ip: 10.101.91.63
    - ip: 10.101.91.63
```

_Live Service:_

MacBook-Pro-4:kubernetes-org tsharma$ kubectl get service cookieflaskservice2 -n tsharma
````
kubectl get service cookieflaskservicev2 -n tsharma
NAME                   TYPE           CLUSTER-IP       EXTERNAL-IP               PORT(S)                         AGE
cookieflaskservicev2   LoadBalancer   10.108.116.214   10.101.91.5,10.101.91.5   5001:30923/TCP,5002:30596/TCP   144d


````
_Live Pods:_

MacBook-Pro-4:kubernetes-org tsharma$ kubectl get pods -n tsharma -l run=cookieflask

```
NAME                             READY   STATUS    RESTARTS   AGE
cookieflaskv2-686f58d489-lns2g   1/1     Running   0          144d
cookieflaskv2-686f58d489-m9m5t   1/1     Running   0          144d
cookieflaskv2-686f58d489-rpld5   1/1     Running   0          144d


```


The service can be reached at IngressHostname:80 (if added to /etc/hosts), IngressIP:80, or EXTERNAL-IP:5001.



###### Sample Python Client Snippet

```
import requests
payload = {
  "baseurl": "<baseurl>",
  "button_finder": {
    "findby": "xpath",
    "value": "//*[@type='submit']"
  },
  "password": "<password>",
  "password_finder": {
    "findby": "name",
    "value": "password"
  },
  "username": "<username>",
  "username_finder": {
    "findby": "name",
    "value": "username"
  }
}

resp = requests.post('https://10.101.91.63/api/cookie/cdp-session-token', json=payload, verify=False)
token = resp.json()['value']```