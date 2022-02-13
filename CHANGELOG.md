# 3.0.0-dev.2

Quicktrack is now deployed to ``! You can now use the most cutting edge version of Quicktrack.
A friendly reminder that a lot of existing features are yet to come.

This version also implemented PWA.

## Features

feat: added Reload Prompt (c6c4e71b)

## Refactor

refactor: disabled some path codes for quicktrack (d215ec8c)

## Build

build: added v3-quicktrack to ALLOWED_HOSTS (4af80e5e)
build: fixed gunicorn not working properly (f114c324)
build: added PWA icons and robots.txt (2bc52d30)
build: added VitePWA (76bf7e270)
build: removed django-manifest-loader (985afacd)
build: gunicorn now runs on development on default (dc2d3924)
build: added vite-plugin-pwa (b37d1830)

## docs

docs: updated Django and PWA Staticfiles (441207a8)


# 3.0.0-dev.1

Backend for Quicktrack is now inside the current folder. All backend files resides within `backend`.

## Build

build: files built into /static/ rather than /assets/ (31970237)
build: moved parent folder to root directory (568572e6)
build: added Backend (340493bb)
build: added Makefile (6d94bd1f)
build: npm i install (f45d1fff)
build: added Heroku Procfile and runtime.txt (795510d)
build: added requirements.txt (aaa927f5)
build: modified .gitignore (fbede547)