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

