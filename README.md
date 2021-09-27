# Genesis - easy boilerplate for a RESTful webapp

## Overview

When starting a new tech project of any sort, one of your first tasks is to figure out the design and the architecture. Chosing wrong can have nasty consequences later on, where you need to chose between working on increasingly unmaintanable code or starting from scratch. The purpose of Genesis is to provide you with a ready to use project template that is both easy to develop, test, and put to production. It is easy to scale up and scale out.
The structure follows a philosophy of "out of sight - out of mind". This means the boilerplate is to be kept separate from the "canvas" where you make your new thing. This is to let you write simple and easy to read code.

## Backend

The backend relies on Django. It too makes it easy to create reusable code. The app is divided into a boilerplate and an api, but only the api is registered as an app. The boilerplate specialized the classes you typucally need while working on a Django project. It uses a MongoDB for it's database and connects to it using Djongo. A default Model in this boilerplate is a Djongo model, it comes with the ability to soft-delete or hard-delete it's instances. It also implements simple_history, which created additional models for every model you define. These history models will record any user who tries to modify the instance. This template uses rest_framework_simplejwt for authentication management. It comes with it's own login and authentication viewas. Upon logging in, the api returns a bearer token. This is a RESTful API, it does no maintain sessions. The only way it knows who is logged in is with the Authorization: Bearer token.

## Frontend

The frontend uses the typescript version of React. It communicates with the backend using axios, the nice thing about it is it manages the api service for you, no need to write a separate service file. Authentication management is handled by the Context component. It has all the methods needed to communicated with the authentication endpoints of the backend. Right now it points to localhost by default. You need to specify the base url in the .env file.

## Architecture

There are two separate modes, dev and prod. The idea is to keep them as identical as possible, so that anything which works on dev will also work on prod. The two use the same docker images, but the containers are displayed slightly differently. This is evident in the fact that each module has one Dockerfile but there are two docker-compose files. You also need to provide a separate .env file for each enviornment.

### dev

When launched, a MongoDB, MongoExpress, and Django containers come up, along with a Mongo volume. The Mongo volume contains the database. This is convenient for developent but dangerous for production. Django's docker container also mounts the django codebase as a volume, so you can work on the code as it is running. Once the dev docker composition is launched, use npm start to launch the frontend, in the future this will be automatic.

### prod

Prod only comes with a Django and nginx containers. You will need to specify the login credentials to the database via the .env file. Upon launch, Django launches with gunicorn workers which feed to a sock. That sock is then mounted to the nginx container, which then feeds is as specified in the /frontend/nginx folder. To be tested in the coming days.
