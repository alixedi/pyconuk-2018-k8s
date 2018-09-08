# Step 1: Toy application

Using python 3(.7)

In order to test:

1. Install dependencies:
`pip install -r requirements.txt`

2. Start the server
`FLASK_APP=webconsole.py flask run`

3. Hit with valid Python:
```
requests.post('http://localhost:5000/api/aa/run/', json={'input': 'print("Hello World")'}).json()
```

4. Hit with invalid Python:
```
requests.post('http://localhost:5000/api/aa/run/', json={'input': 'pint("Hello World")'}).json()
```

5. Remembers variables like normal python, and supports multiple lines:
```
requests.post('http://localhost:5000/api/aa/run/', json={'input': 'b=1'}).json()
requests.post('http://localhost:5000/api/aa/run/', json={'input': 'a=1\nprint("1 + 1 =", a + b)'}).json()
```
