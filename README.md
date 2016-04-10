# Qiang Tools

A tools application by flask.

## Deploy to Local

### Set env config under .env file

### Run migration by alembic

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

### Create user

```
python manage.py shell
>>> from app import db
>>> from models import User
>>> db.session.add(User('admin', '12345'))
>>> db.session.commit()
>>> exit()
```

---

## Deploy to Heroku

```
heroku git:remote -a [YOUR_HEROKU_APP]
heroku config:set APP_SETTINGS=config.ProductionConfig --remote heroku
heroku addons:create heroku-postgresql:hobby-dev
heroku config
git push heroku master
heroku run python manage.py db upgrade
heroku run python manage.py shell
(Create user)
```

---

## License

MIT
