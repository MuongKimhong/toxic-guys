#!/bin/bash

git pull origin master

ttab "cd ~/Development/toxic_guys/frontend; npm run serve"

ttab "source virtual_environment/bin/activate; python3 manage.py runserver" 

code .
