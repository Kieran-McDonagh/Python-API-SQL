# Python-API-SQL

## Running the project locally

### To run the project locally:

### 1) Make sure you have the latest changes:

```
git pull main
```

### 2) From the root of the project activate the virtual environment with:

```
source venv/bin/activate 
```

### If you need to create your own virtual environment, run:

```
python -m venv venv
```


### If you need to install any requirements, run:

```
pip install -r requirements.txt
```

### 3) Finally, run the application with:

```
python main.py
```

(Or if using python 3)

```
python3 main.py
```

## Seeding data

### To get a fresh database, from the project root, run:

```
python remove_database.py
```

#### Now the next time you run the project you will be prompted to seed new data.
