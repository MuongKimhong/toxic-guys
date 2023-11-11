#!/bin/bash

git pull origin master

ttab "cd $PWD/frontend; npm run serve"

ttab "source virtual_environment/bin/activate; python3 manage.py runserver" 

ttab "cd $PWD/websocket; npm start" 

code .
