# Deploying to Heroku

A short documentation of deploying to Heroku.

## Setting Up

Heroku requires a few things :

1. Procfile
    * For this instance, it would be setting up `gunicorn`.
1. runtime.txt
    * This would be a simple `python 3.8.10`
1. requirements.txt(for Python/Django projects)
    * Can be done with `pip freeze > requirements.txt`

Django itself also requires a few settings:

1. ALLOWED_HOSTS must include the final address that you use.
1. 

## Pipeline

To share database between two apps:

>`heroku addons:attach next-quicktrack::DATABASE --app v3-quicktrack`

This will attach the database addon to your new app. However, it shows up as `HEROKU-POSTGRESQL_[COLOR]_URL` instead. We will need to promote it to `DATABASE_URL` with this command.

>`heroku pg:promote -a v3-quicktrack postgresql-flexible-13362`

This will rename the database to `DATABASE_URL`.