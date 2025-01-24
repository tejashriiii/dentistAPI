# dentist api

1. Create virtual environment

```sh
conda create -n dentist python=3.12
```

2. Activate virtual environment

```sh
conda activate dentist
```

3. Install requirements

```sh
pip install -r requirements.txt
```

4. **Change .env.example to .env and add proper environment variables according to your setup**

5. Make migrations

```sh
python manage.py makemigrations
```

6. Migrate

```sh
python manage.py migrate
```
