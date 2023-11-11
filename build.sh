#!/bin/bash

echo ""
echo "Checking for ttab..."

if which ttab > /dev/null; then
	echo "ttab is installed"
else
    echo "ttab is not installed"
    echo ""
    echo "Checking for Nodejs..."
    
	if type node > /dev/null 2>&1 && which node > /dev/null 2>&1 ;then
		echo " "	
		node -v
		echo "Nodejs is installed"
	else
		echo "Please install nodejs to continue"
		exit 1
	fi

	# install ttab with npm registry
	sudo npm install ttab -g	
fi


ttab "cd $PWD/frontend; npm install; npm run serve"

ttab "cd $PWD; python3 -m venv virtual_environment; source virtual_environment/bin/activate; pip3 install -r requirements.txt; python3 manage.py makemigrations; python3 manage.py migrate; python3 manage.py runserver"

ttab "cd $PWD/websocket; npm install; npm start"
