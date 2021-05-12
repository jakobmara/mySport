<h1>mySport</h1>

<h2>What is this</h2>
<p>This project is made to look up basketball satistics when it comes to your favorite player or team</p>

<h2>How does it work</h2>
<p>This project was built using python's web framework called Django</p>

<h2>What is the purpose of this</h2>
<p>I wanted experience in using the Django framework and I am enthusiastic about basketball so I figured I'd create a web application revolving around basketball specific information</p>

<h2>Current features</h2>
<p>Right now you can search up past and present NBA players and will get their detailed per season statistics, you can also search up past and present NBA teams and get per season team sastitic for specified teams as well</p>

<h2>Requirements</h2>
<hr/>

<p>python3 and Django </p>
<p>Once you have python3 running the command ">pip install django" will install the django package for you.</p>
<p>If you wish to run the populateDB script (will update databse with recent player stastics) you will need to also run the command ">pip install PandasBasketball" aswell as ">pip install pandas" </p>

<hr/>

<h2> instructions </h2>
<p>Once the above requirements are met to start the sever type in cmd within the directory: ">python manage.py runserver" and go to URL: "http://127.0.0.1:8000/mySport/" to access the website. </p>
To run the populateDB script which will repopulate the DB you can run the command: ">python manage.py populateDB" however there will already be a prepopulated database within file.</p>
