PyconUk - Kubernetes Workshop
=============================

Home instructions
-----------------

- laptop requirement:
    * ~4 GB of RAM
    * ~15 GB of free disk space
- Download & install virtualbox: https://www.virtualbox.org/wiki/Downloads
- Download & unzip our disk image: https://tinyurl.com/y9tvcsbj
- Download & install ssh client (mac & linux have this usually installed), for windows:
  https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html
- When following after the workshop at Pycon UK, see the guide at:
  https://github.com/alixedi/pyconuk-2018-k8s

Session 1 - 90m
---------------

1. Introduction to speakers

2. Learning objectives
    * Demonstrate Kubernetes to your colleagues.
    * Deploy a web application on Kubernetes.
    * Manage your deployment e.g. scaling up and down, rolling updates and rollbacks. 
    * Deploy multiple services on Kubernetes.
    * Describe the Kubernetes API to your colleagues.
    * Demonstrate using kubectl to interact with the Kubernetes API.

3. Installation
    * Laptop requirements:
       * ~4 GB of RAM
       * ~15 GB of free disk space
       * Virtualbox
       * ssh client
    * Download the virtual disk - Ask us for a USB or download from [here](https://tinyurl.com/y9tvcsbj)
    * Unzip the virtual disk
    * Create a virtual machine:
      * Type: Linux, version: Ubuntu 64 bit
      * 2048 RAM
      * "use existing virtual hard disk file" (use the unziped virtaul disk from the previous step)
      * Create 
      * machine -> settings
      * network -> port-forwarding -> create new rule: host port: 2222, guest port: 22
    * You VM image has microk8s (https://asciinema.org/a/182634) installed. This includes Docker and Kubernetes.
    * Verify that everything is working
      * get the ip address of the NAT network: `ip addr show | grep vboxnet0`
      * ssh into your machine: `ssh osboxes@<ip> -p 2222` (if using putty: there is a field for the port)
      * login with username: osboxes password: osboxes.org
      * Verify `kubectl get pods --all-namespaces`
      * cd ~/pyconuk-2018-k8s && git pull
    * We will encourage you to pair with someone

4. Hello World! (step0)
    * The most basic Flask app in the world:
    
    ```python
    from flask import Flask
    app = Flask(__name__)

    @app.route("/")
    def hello():
        return "Hello World!"
    ```
    
   * You can run it like: `FLASK_APP=hello_world.py flask run`

5. A very brief intro to Docker
    * Versus virtualenv, conda and VMs
    * Play around with `$ docker`
    * A brief explanation of images, containers etc.
    * image is a lightweight virtual machine image with isolation
    * Docker is like virtualenv but it isolated not just python packages but the filesystem, network interfaces and system libraries, and other.
      Docker also standarizes (a lot of things) on how you run applications.
      
-- 30 minutes

6. Hello Docker World!
    * A very basic dockerfile for our hello world app can look like:

    ```docker
    FROM python
    RUN pip install flask
    ADD hello_world.py
    ENV FLASK_APP=hello_world.py
    CMD ["flask", "run", "-h", "0.0.0.0"]
    ```
    
    * docker build . -t hello-world:local

7. Interactive Console (step1)

    ```python
    import code
    import io
    import contextlib
    
    import flask
    
    
    app = flask.Flask(__name__)
    app.consoles = {}
    
    
    class WebConsole:
    
        def __init__(self):
            self.console = code.InteractiveConsole()
    
        def run(self, code):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                with contextlib.redirect_stderr(output):
                    for line in code.splitlines():
                        self.console.push(line)
            return {'output': str(output.getvalue())}
    
    
    @app.route('/api/<uname>/run/', methods=['POST'])
    def run(uname):
        if not uname in app.consoles:
            app.consoles[uname] = WebConsole()
        return flask.jsonify(
            app.consoles[uname].run(
                flask.request.get_json()['input']
            )
        )
    ```

8. Assignment #1: webconsole in docker
    * Create a `Dockerfile` for webconsole
    * Build the image
    * Run the image
    * What happens when you try and curl POST `/api/run/` something

-- 1 hour

9. Introduction to Kubernetes
    * Challenges of building modern applications
        * Complexity
        * Load characteristics
        * Horizontal scaling
        * CI/CD
    * Microservice - when are they useful and why? 
    * Kubernetes - what and why? - solves most of the microservices problems

10. Kubernetes Web Console (step2)
    * Run as service deployment: 
    ```bash
    kubectl run webconsole \
        --image pyconuk-2018-k8s:step2 \
        --port 5000 \
        --replicas 2 \
        --expose
    ```
    
   * Explain pods, deployments, and services
   * Access the service:
     * proxy: `kubectl proxy` (explain what this does)
     * Use the service:
       ```python
        import requests
        requests.post('http://localhost:8001/api/v1/namespaces/default/services/webconsole/proxy/api/me/run/',
                      json={'input': 'print("Hello World")'}).json()
        ```
     
11. Show some kubernetes features  
   * Try and scale the deployment - show the new pods being created
     `kubectl scale deployment webconsole --replicas 5`
   * Try and kill a pod - show that it gets recreated
     `kubectl delete <pod-name>`
   * Simulate a service failure:
     `request.get('http://localhost:8001/api/v1/namespaces/default/services/webconsole/proxy/api/crash/')`

12. Introduction to kubectl and Kubernetes API
    * Start with `kubectl get` - we should have the webconsole running so we should be able to show a few objects
    * `$ kubectl --help` has sections for basic commands - beginners and intermediate.

13. Assignment:
    * Lets explore a few kubectl commands.
    * Assignment - See if you can figure out a problem with our application

Session 2 - 90m
---------------

1. Infrastructure as code, why is this nice, declarative vs imperative.

2. Introduction to kubernetes manifests:
   Show:
   ```
      kubectl run webconsole \
        --image pyconuk-2018-k8s:step2 \
        --port 5000 \
        --replicas 2 \
        --expose \
        --dry-run -o yaml
   ```
   Walk through of the simplified yaml produced:

    ```yaml
    apiVersion: extensions/v1beta1
    kind: Deployment
    metadata:
      name: webconsole
    spec:
      replicas: 2
      template:
        metadata:
          labels:
            app: webconsole
        spec:
          containers:
          - image: pyconuk-2018-k8s:step2
            name: webconsole
            ports:
              - name: api
                containerPort: 5000
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: webconsole
    spec:
      ports:
      - name: webconsole
        port: 5000
        targetPort: api
      selector:
        app: webconsole
    ```

3. Back to the example, demonstrate the problem:
    ```python
       import requests
       requests.post('http://localhost:8001/api/v1/namespaces/default/services/webconsole/proxy/api/me/run/',
                     json={'input': 'a = 1'}).json()
       requests.post('http://localhost:8001/api/v1/namespaces/default/services/webconsole/proxy/api/me/run/',
                     json={'input': 'print(a)'}).json()
    ```
    * Ask if people understand why
    * Explain the issue with load balancing

4. Split the Web Console to solve the problem:
    * Introduce jobs
    * Quick walkthrough of [consolehub.py](https://github.com/alixedi/pyconuk-2018-k8s/blob/master/step3/consolehub/consolehub.py)
    * Walk-through of [job_template](https://github.com/alixedi/pyconuk-2018-k8s/blob/master/step3/consolehub/job-template.yaml)
    * Explain `kubectl apply -f step3/consolehub/deployment.yaml`
    * Demonstrate 
    ```python
       import requests
       requests.post('http://localhost:8001/api/v1/namespaces/default/services/consolehub/proxy/api/me/start/').json()
       requests.post('http://localhost:8001/api/v1/namespaces/default/services/consolehub/proxy/api/me/run/',
                     json={'input': 'a = 1'}).json()
       requests.post('http://localhost:8001/api/v1/namespaces/default/services/consolehub/proxy/api/me/run/',
                     json={'input': 'print(a)'}).json()
    ```
    
-- 30 minutes

5. Assignment, run step 3:
   * Build: `./step3/build.sh`
   * Apply the manifest: `kubectl apply -f step3/consolehub/deployment.yaml`
   * Use the application, example:
    ```python
       import requests
       requests.post('http://localhost:8001/api/v1/namespaces/default/services/consolehub/proxy/api/me/start/').json()
       requests.post('http://localhost:8001/api/v1/namespaces/default/services/consolehub/proxy/api/me/run/',
                     json={'input': 'a = 1'}).json()
       requests.post('http://localhost:8001/api/v1/namespaces/default/services/consolehub/proxy/api/me/run/',
                     json={'input': 'print(a)'}).json()
    ```

   * Explorer kubectl:
     ```
        kubectl get pods
        kubectl get services
        kubectl get jobs
     ```

6. Problems with the current implementation:
  * Tight coupling of the application code and infrastructure
  * You create the job synchronously
  
-- 60 minutes
  
7. Introduce the final version:
    * Quick walkthrough of [consolehub.py](https://github.com/alixedi/pyconuk-2018-k8s/blob/master/step4/consolehub/consolehub.py)
    * Only the provisioner is coupled to kubernetes [provisioner.py](https://github.com/alixedi/pyconuk-2018-k8s/blob/master/step4/provisoner/provisioner.py)
    
8. Demonstrate rolling update
    
9. Assignment, do the rolling update:
   * Build: `./step4/build.sh`
   * Apply the manifest: `kubectl apply -f step4/k8s_manifests`
   * use `kubectl get pods` to see pods shutdown and start in a rolling way

10. Next steps:

    * Local running options:
      * docker for mac & windows: https://blog.docker.com/2018/01/docker-mac-kubernetes/
      * minikube (sometimes fiddly) or microk8s (alpha)
    * Production clusters:
      * gcp/aws/digital ocean
      * Other options: https://kubernetes.io/docs/setup/     

11. Q&A
