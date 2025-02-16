# dentist-API

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

```sh
python manage.py migrate django_celery_beat
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

a. Go to `http://localhost:8000/admin`
b. Enter your superuser credentials from step 7
c. In the `Authentication` app add a doctor and admin
d. **STRICTLY** Keep password field empty for all the users

9. Run Celery worker

```sh
celery -A dentistAPI worker --loglevel=info --pool=solo
```

10. Run Celery beat
```sh
celery -A dentistAPI beat --scheduler django_celery_beat.schedulers.DatabaseScheduler --loglevel=info
```

# dentist-UI

1. Clone the frontend (get out of this directory)

```sh
git clone https://github.com/tejashriiii/dentistFrontend
```

2. Follow instructions from [here](https://github.com/tejashriiii/dentistFrontend)
3. Set password for doctor and admin with the signup page
4. Login as the admin
5. Register the patient using registration form

## Production steps (FOR DEPLOYMENT ONLY)

- Replace`pyscopg2-binary` with the entire package built using the c libraries
- Follow django's article and setup `httpd` and all
