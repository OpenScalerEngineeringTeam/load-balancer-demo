### Load Balancer Demo

OpenScaler **Load Blanacer Demo** is a simple web application made with Flask to help you try out OpenScaler Load Balancer features.

**Table of content**

- [Description](#description)
- [Quickstart](#quickstart)
- [Test Application Locally](#test-application-locally)
- [Access Application with Load Balancer](#access-application-with-load-balancer)

### Description

[![Architecture of
microservices](/docs/img/architecture-diagram.png)](/docs/img/architecture-diagram.png)

## Quickstart

1. Copy the `cloud-init.config.yaml` file
2. Create a new instance (NOTE: if you don't have a new instance, follow the guide [#install-demo-app-locally])

### Access Application with Load Balancer

## Test Application Locally

To test the application locally

- On Linux:

```shell
python3 -m venv .venv
source .venv/bin/activate    # or .venv/Scripts/activate.fish for fish shell
pip install -r requirements.txt
export FLASK_APP=load-balancer-demo.py
flask run --host=0.0.0.0 --port=8080
```

- On Windows:

```shell
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
$env:FLASK_APP = "load-balancer-demo.py"
flask run --host=0.0.0.0 --port=8080
```

You can now access your application at `http://localhost:8080`

## Install Demo App Locally

If you don't want to create a new instance, you can install the demo app locally as follows:

1. copy the content [load-balancer-demo.py](load-balancer-demo.py) to your local machine
2. run the application locally

```shell
python3 -m venv .venv
source .venv/bin/activate    # or .venv/Scripts/activate.fish for fish shell
pip install -r requirements.txt
export FLASK_APP=load-balancer-demo.py
flask run --host=0.0.0.0 --port=8080
```
