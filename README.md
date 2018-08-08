# pyconuk-2018-k8s

# Learning Objectives
* What is Kubernetes?
* Get familiar with Kubernetes vocabulary.
* Install and run Kubernetes on `localhost`.
* Interact with the Kubernetes API using `kubectl`.
* Use the Python client to interact with the Kubernetes API

# Development of toy application
In order to teach students about Kubernetes, we would like to develop a toy application that is designed to be complex enough to touch beginner-intermediate k8s features. We have selected a mock JupyterHub for this.

1. Write a Flask app that provides users with Python consoles by spinning `code.InteractiveConsole` processes.
2. Dockerise the Flask application as well as `code.InteractiveConsole` processes and run them on Kubernetes.
3. Use a queue for incoming console requests. Split out the code that provisions the consoles from the Flask app. Define a cron job that monitors the average wait time in the queue and scale the cluster up/down.
