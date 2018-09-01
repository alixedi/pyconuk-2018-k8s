PyconUk - Kubernetes Workshop
=============================

Session 1
---------

1. Introduction - Learning objectives

	* What are Microservice, when are they useful and why?
	* Kubernetes is a framework that helps you deploy, run and manage microservices on clusters. 
	* At the end of today's session, you shall be able to:
		* Demonstrate Kubernetes to your colleagues.
		* Deploy a basic web application 

2. Installation - Virtual machine image?
	* Ask them to install VirtualBox
	* Ask them to download the VM image - this should contain microk8s (https://asciinema.org/a/182634) as well as Docker.
		* Installation script:

		```
		<!--The edge versoin contains docker-->
		sudo snap install microk8s --classic --edge
		```

	* Take some USBs of VM image

3. Hello World 
	* Take from Flask home page
	* For example `hello_world.py`:
	
    ```
    from flask import Flask
    app = Flask(__name__)

    @app.route("/")
    def hello():
        return "Hello World!"	    
    ```

4. Docker Hello World!
	* Basic dockerfile for our hello world app:
	* For example `Dockerfile`

	```
	FROM python
	RUN pip install flask
	ADD hello_world.py
	ENV FLASK_APP=hello_world.py
	CMD ["flask", "run", "-h", "0.0.0.0"]
	```

5. Brief explanation of Docker
    * Docker is like virtualenv but it isolated not just python packages but the filesystem, network interfaces and system libraries. Docker also standarizes (a lot of things) on how you run applications.
    * Get them to play around with the `$ docker` cli.

6. Interactive Console and Web console
	* Very quick walk through of the code
	* Which is:

    ```
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

6. Docker Web Console
	* Follow the example of how we dockerised `hello_world.py`
	* Try and dockerise `webconsole.py`
	* See if you can get it to work
	* What happens when you try and curl POST `/run` something

7. Kuberbnetes Web Console 
    * Push the image for webconsole
    * kubectl run webconsole --image alixedi/webconsole --port 5000 --replicas 2
    * Try and kill a pod - show that it gets recreated

8. Introduction to kubectl and Kubernetes API (step3)
    * Start with `kubectl get` - we should have the webconsole running so we shoul be able to show a few objects
    * Try and cover a fer basic commands
    * `$ kubectl --help` has sections for basic commands - beginners and intermediate.
    * Assignment - ask them to explore describe and explain for instance.
    * Show scaling and rolling updates


Session 2
---------

1. How to make reproducable deployments
    * Introduce --dry-run -o yaml
    * Introduce `kubectl -apply`
    * Touch upon why is this nice - Infrastructure as code, declarative (essentially you describe the desired state of your infrastructure)
	 * Run the web console with a deployment.yaml file (possibly an assignmeent)

2. Explain the deployment.yaml
    * Walk through:
    
    ```
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
    * Introduce what a job is and how is it different to a service - this is basically the version that we developed on 27 Aug (see Git - Step3)
    * Start with a quick walkthrough of [consolehub.py](https://github.com/alixedi/pyconuk-2018-k8s/blob/master/step3/consolehub/consolehub.py)
    * Followed by [job_template](https://github.com/alixedi/pyconuk-2018-k8s/blob/master/step3/consolehub/job-template.yaml)
    * `kubectl --apply` followed by `kubectl get pods|services|jobs`

5. Introduce the final version that has API, provisioner, redis as a queue and the jobs

6. Assignment ???

7. Q and A, where to go next, wrap, check off the learning objectives, introduce helm, kapitan etc., point to next steps for further learning
