## User API REST

#### About
This is a full API Rest with some rules depending on User level.

#### Technologies used
- Python
- Django
- Django Rest Framwork
- Docker, docker-compose
- Postgres

### How to deploy on local 🚀
Copy local enviroments to **.env**
```sh
cp envs/local .env
```
Apply migrations
```sh
docker-compose run django python manage.py migrate
```
If you want, you can inicialize with three type of users:
| user | password | level |
| ------ | ------ | ----- |
| jf_superuser | Strong.1 | **superuser** |
| jf_staff | Strong.1 | **staff** |
| jf_normal | Strong.1 | **normal** |
```sh
docker-compose run django python manage.py loaddata apps/users/fixtures/users.json
```
Start project
```sh
docker-compose up
```

You can enter the commands inside the container, using
```sh
docker-compose run --rm --service-port django bash 
```

### Test
To run the unit test you have to use **pytest**
```sh
docker-compose run django pytest --cov apps/ 
```
