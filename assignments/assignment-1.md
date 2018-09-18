Assignment #1 webconsole in docker:
-----------------------------------

* Run the application directly
* Create a `Dockerfile` for webconsole
* Build the image
* Run the image
* What happens when you try and use requests POST something to: `/api/<username>/run/`, for example:

```python
import requests
requests.post('http://localhost:5000/api/ali/run/',
              json={'input': 'print("Hello World")'}).json()
```

As a reminder, sample for hello world:

* A very basic dockerfile for our hello world app can look like:

```docker
FROM python
RUN pip install flask
ADD hello.py /
ENV FLASK_APP=/hello.py
CMD ["flask", "run", "-h", "0.0.0.0"]
```
    
* Build a docker image: `docker build . -t hello:local`
* Now you have a docker image: `docker images |grep hello`
* Run the image: `docker run --net host hello:local`
* access the service again: `curl localhost:5000`
