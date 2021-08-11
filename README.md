# Flask bootstrap

## Setup environment

You must set your python virtual environment, with virtualenv or conda. 

### With virtualenv

```bash
virtualenv --python=python3.7 flask-bootstrap
source flask-bootstrap/bin/activate
pip install --upgrade pip
pip install --upgrade -r requirements.txt
```

### With Anaconda

```bash
conda create -n flask-bootstrap python=3.7.9 -y
conda activate flask-bootstrap
pip install --upgrade pip
pip install --upgrade -r requirements.txt
```

## Start server

Start your API server with:
```bash
python main.py
```

## Test server

Try one of the following commands:
```bash
curl localhost:5000
curl localhost:5000/John%20Doe
curl -XPOST localhost:5000 -d '{"name": "John Doe"}' 
```

## Test scenario

Once your server is up, you can execute a test scenario with:
```bash
python test.py test-input.json
```

Assuming test-input.json contains:
```bash
{"name": "You"}
{"name": "Me"}
```

All events in `test-input.json` are sent to API. API responses are printed to standard output.
```bash
200 Hello, You!
200 Hello, Me!
```
