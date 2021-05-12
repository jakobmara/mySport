Requirements:
-------------------------------------------------------------------------------------------------------------- 
python3
django, Once you have python3 running the command ">pip install django" will install the django package for you
if you wish to run the populateDB script you will need to also run the command ">pip install PandasBasketball" aswell as ">pip install pandas"
--------------------------------------------------------------------------------------------------------------


Once the above requirements are met to start the sever type in cmd within the directory: ">python manage.py runserver" 
and go to URL: "http://127.0.0.1:8000/mySport/" to access the website.
To run the populateDB script which will repopulate the DB you can run the command: ">python manage.py populateDB" however there will already 
be a prepopulated database within file.
