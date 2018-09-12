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
      * network -> change to bridge
    * You VM image has microk8s (https://asciinema.org/a/182634) installed. This includes Docker and Kubernetes.
    * Verify that everything is working
      * login with username: osboxes password: osboxes.org
      * get the ip address: `ip addr show | grep enp0s3`
      * ssh into your machine 
      * Verify `kubectl get pods --all-namespaces`
      * cd ~/pyconuk-2018-k8s && git pull
    * We will encourage you to pair with someone

4. Hello World!
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
    * Docker is like virtualenv but it isolated not just python packages but the filesystem, network interfaces and system libraries. Docker also standarizes (a lot of things) on how you run applications.
    * An explanation of Dockerfile

6. Hello Docker World!
    * A very basic dockerfile for our hello world app can look like:

    ```docker
    FROM python
    RUN pip install flask
    ADD hello_world.py
    ENV FLASK_APP=hello_world.py
    CMD ["flask", "run", "-h", "0.0.0.0"]
    ```

7. Interactive Console

    ```python
    import code, io, contextlib
    import flask

    app = flask.Flask(__name__)
    app.console = None

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

    @app.route('/run/', methods=['POST'])
    def run():
        if app.console is None:
            app.console = WebConsole()
        return flask.jsonify( 
            app.console.run(
                flask.request.get_json()['input']
            )
        )
    ```

8. Assignment #1
    * Try and dockerise `webconsole.py`
    * What happens when you try and curl POST `/run` something

9. Introduction to Kubernetes
    * Challenges of building modern applications
        * Complexity
        * Load characteristics
        * Horizontal scaling
        * CI/CD
    * Microservice - when are they useful and why? 
    * Kubernetes - what and why? > solves most of the microservices problems

10. Kubernetes Web Console 
    * Run as service deployment: 
    ```bash
    kubectl run webconsole \
        --image webconsole:local \
        --port 5000 \
        --replicas 2 \
        --expose
    ```

   * Try and access a pod using `port-forward`
   * Try and scale the deployment - show the new pods being created
   * Try and kill a pod - show that it gets recreated
   * Try and change the code and demonstrate a rolling update

11. Introduction to kubectl and Kubernetes API (step3)
    * Start with `kubectl get` - we should have the webconsole running so we should be able to show a few objects
    * `$ kubectl --help` has sections for basic commands - beginners and intermediate.

12. Assignment:
    * Lets explore a few kubectl commands.
    * Assignment - See if you can figure out a problem with our application
    * Solution: Demonstrate the replicas problem: `a=1; print(a)` would fail b/c load balancer is round robin.


Session 2 - 90m
---------------

1. How to make reproducable deployments
    * Introduction to `kubectl --dry-run -o yaml`
    * Introduction to `kubectl -apply -f`
    * Why is this nice - Infrastructure as code, declarative etc.

2. Walk through of the yaml produced:

    ```yaml
    apiVersion: extensions/v1beta1
    kind: Deployment
    metadata:
      labels:
        app: webconsole
      name: webconsole
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: webconsole
      strategy: {}
      template:
        metadata:
          creationTimestamp: null
          labels:
            app: webconsole
        spec:
          containers:
          - image: pyconuk-2018-k8s:webconsole
            name: webconsole
            ports:
              - name: http
                containerPort: 5000
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: webconsole
      labels:
        app: webconsole
    spec:
      type: NodePort
      ports:
      - name: webconsole
        port: 80
        targetPort: http
        protocol: TCP
      selector:
        app: webconsole
    ```

4. Split the Web Console into the service and the job
    * Introduce services and jobs
    * Quick walkthrough of [consolehub.py](https://github.com/alixedi/pyconuk-2018-k8s/blob/master/step3/consolehub/consolehub.py)
    * Walk-through of [job_template](https://github.com/alixedi/pyconuk-2018-k8s/blob/master/step3/consolehub/job-template.yaml)
    * `kubectl --apply` followed by `kubectl get pods|services|jobs`

5. Introduce the final version that has API, provisioner, redis as a queue and the jobs

6. Assignment ???

7. Q and A, where to go next, wrap, check off the learning objectives, introduce helm, kapitan etc., point to next steps for further learning

    * Learning objectives

    * Next steps:

        * Docker on Mac and Windows comes with Kubernetes
        * For Linux, use minikube
        * For production, AWS as well as GCP sell Kubernetes clusters
