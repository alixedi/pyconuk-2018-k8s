PyconUk - Kubernetes Workshop
=============================

Session 1 - 90m
---------------

###Setting up

0. Introduction to speakers

1. Learning objectives
    * Demonstrate Kubernetes to your colleagues.
    * Deploy a web application on Kubernetes.
    * Manage your deployment e.g. scaling up and down, rolling updates and rollbacks. 
    * Deploy multiple services on Kubernetes.
    * Describe the Kubernetes API to your colleagues.
    * Demonstrate using kubectl to interact with the Kubernetes API.

2. Installation
    * Laptop requirements:
       * ~4 GB of RAM
       * ~15 GB of free disk space
       * Virtualbox
    * Download the Virtual appliance - Ask us for a USB or downlowad from [here](https://tinyurl.com/pyconuk-2018-k8s)
    * Copy/Unzip the virtual appliance
    * Import the appliance: "Import Appliance" in the File menu
    * You VM image has microk8s (https://asciinema.org/a/182634) installed. This includes Docker and Kubernetes.
    * Verify that everything is working
      * login with username: osboxes password: osboxes.org
      * Verify `kubectl get pods --all-namespaces`
      * cd ~/pyconuk-2018-k8s && git pull
    * We will encourage you to pair with someone

3. Hello World!
    * The most basic Flask app in the world:
    
    ```python
    from flask import Flask
    app = Flask(__name__)

    @app.route("/")
    def hello():
        return "Hello World!"
    ```
    
   * You can run it like: `FLASK_APP=hello_world.py flask run`

4. Hello Docker World!
    * A very basic dockerfile for our hello world app can look like:

    ```docker
    FROM python
    RUN pip install flask
    ADD hello_world.py
    ENV FLASK_APP=hello_world.py
    CMD ["flask", "run", "-h", "0.0.0.0"]
    ```

5. A very brief intro to Docker
    * Versus virtualenv, conda and VMs
    * Play around with `$ docker`
    * A brief explanation of images, containers etc.
    * image is a lightweight virtual machine image with isolation
    * Docker is like virtualenv but it isolated not just python packages but the filesystem, network interfaces and system libraries. Docker also standarizes (a lot of things) on how you run applications.
    * An explanation of Dockerfile

6. Interactive Console

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

7. Assignment #1
    * Try and dockerise `webconsole.py`
    * What happens when you try and curl POST `/run` something
    
###Hello Kubernetes

8. Inrtoduction to Kubernetes
    * Challenges of building modern applications
        * Complexity
        * Load characteristics
        * Horizontal scaling
        * CI/CD
    * Microservice - when are they useful and why? 
    * Kubernetes - what and why? > solves most of the microservices problems

9. Kuberbnetes Web Console 
    * Run a basic deployment: 
    ```bash
    kubectl run webconsole \
        --image webconsole:local \
        --port 5000 \
        --replicas 2
    ```
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

10. Introduction to kubectl and Kubernetes API (step3)
    * Start with `kubectl get` - we should have the webconsole running so we shoul be able to show a few objects
    * `$ kubectl --help` has sections for basic commands - beginners and intermediate.

11. Assignment #2
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
