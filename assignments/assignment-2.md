Assignment 2:
-------------

* Build the image:

   * `cd ../step2`
   * `./build.sh`

* Run as service deployment: 

```bash
kubectl run webconsole \
     --image pyconuk-2018-k8s:step2 \
     --port 5000 \
     --replicas 2 \
     --expose
```

* Grab the service ip: 
   `export WEBCONSOLE_IP=$(kubectl get service webconsole -o go-template="{{ .spec.clusterIP  }}")`
   
* Use the service:

```python
import requests
import os
requests.post(f'http://{os.environ["WEBCONSOLE_IP"]}:5000/api/ali/run/',
              json={'input': 'print("Hello World")'}).json()
```

* Lets explore a few kubectl commands.

```
     kubectl get pods
     kubectl get deployments
     kubectl get services
     kubectl --help
     kubectl explain
     kubectl describe
```
    
* Assignment: See if you can figure out a problem with our application

