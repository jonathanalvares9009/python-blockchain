**Create a virtual isolated environment**

```
python3 -m venv (environment-variable-name)
```

**Activate the virtual environment**

```
source blockchain-env/bin/activate
```

**Install all packages**

```
pip3 install -r requirements.txt
```

**Run the tests**

```
python3 -m pytest backend/tests
```

**Run the application and API**

```
python3 -m backend.app
```

**Run a peer instance**

```
export PEER=True && python3 -m backend.app
```
