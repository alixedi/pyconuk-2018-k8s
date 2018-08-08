# Step 1: Toy application

Using python 3(.7)

In order to test:

1. Install dependencies:
`pip install -r requirements.txt`

2. Start the server
`FLASK_APP=webconsole.py flask run`

3. Hit with valid Python:
```
curl \
-H "Content-Type: application/json" \
-d '{"input": "print(\"Hello World\")"}' \
localhost:5000/run/aa
```

4. Hit with invalid Python:
```
curl \
-H "Content-Type: application/json" \
-d '{"input": "pint(\"Hello World\")"}' \
localhost:5000/run/aa
```

5. Remembers variables like normal python, and supports multiple lines:
```
curl \
-H "Content-Type: application/json" \
-d '{"input": "b=1"}' \
localhost:5000/run/aa

curl \
-H "Content-Type: application/json" \
-d '{"input": "a=1\nprint(\"1 + 1 =\", a + b)"}' \
localhost:5000/run/aa
```
