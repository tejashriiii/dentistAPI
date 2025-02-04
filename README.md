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

```sh
python manage.py makemigrations user
```

```sh
python manage.py makemigrations authentication
```

```sh
python manage.py makemigrations admin_actions 
```

6. Migrate

```sh
python manage.py migrate
```

7. Create superuser 

```sh
python manage.py createsuperuser
```
(don't set email, set a simple username and password)

8. Create roles
```sh
python manage.py runserver
```
- Go to the url `http:localhost:8000/admin`
- Enter your credentials
- Create roles for all 3 roles 
- Run the `http:localhost:8000/ad/register_details` with the default json provided
- Run the `http:localhost:8000/u/signup` with the default json provided
- Run the `http:localhost:8000/u/login` with the default json provided
