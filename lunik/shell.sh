#!/bin/bash

settings='--settings=lunik.settings.develop'

#Function django server 
#Put ip:port in OPTARG ej. 0.0.0.0:8002
runserverFunction(){
	echo "Runserver django lunik"
	python manage.py runserver $OPTARG $settings
}

#Put name of app or to set migrations of all apps put ''
makemigrationsFunction(){
	echo "Migraciones pendientes para al app:" $OPTARG
	python manage.py makemigrations $OPTARG $settings
	echo "Migraciones realizadas para la app" $OPTARG
	python manage.py migrate $OPTARG $settings
}

startappFunction(){
	echo "Creacion de la app:" $OPTARG
	python manage.py startapp $OPTARG $settings
}

createSuperuserFunction(){
    echo "Creacion de super usuario:" $OPTARG
    python manage.py createsuperuser --email $OPTARG $settings
}

createEmptyMigration(){
	echo "Creacion de migración vacía" $OPTARG
	python manage.py makemigrations --empty stores --name $OPTARG $settings
}

testFunction(){
	echo "Test: "$OPTARG
	python manage.py test $OPTARG $settings
}
#to run .sh put opts -m(migrations)(app_name) or -r(runserver)(ip:port)
while getopts 'm:r:a:s:e:t:' opts
do
	case $opts in
		m) makemigrationsFunction $OPTARG ;;
		r) runserverFunction $OPTARG ;;
		a) startappFunction $OPTARG ;;
		s) createSuperuserFunction $OPTARG ;;
		e) createEmptyMigration $OPTARG ;;
		t) testFunction $OPTARG ;;
	esac
done



