# pyform
##An efficient way to use TreasuryDirect's bond calculator

**Note!** - This script isn't user-friendly and will require knowledge of using the PostGreSQL database, data insertion, and will require tweaking of the script to work with your database. A minor adjustment of the code may also have to be made to change the denomination on the form to match your bonds. The line that sets the bond denomination can be copied/pasted and used to change the bond series. This script was written to calculate the default, series EE bonds.

> Comments are written into the code, in conjunction with this readme, to help an end user understand how the script works and make their own changes

**Procedure**

1. Open Terminal *(cmd + space, search for 'Terminal' or go to Applications/Utilities)*

2. This module needs three external Python libraries installed one by one. To install them, copy and paste each of the following into Terminal and hit enter *(you'll have to enter your password to install these as an administrator)*

	`sudo pip install selenium`

	`sudo pip install beautifulsoup`

	`sudo pip install psycopg2`

	Selenium allows the manipulation of the web form, BeautifulSoup grabs data from the resulting output table from the form, and Psycopg2 does two things: 1. it allows the retrieval of bond date/serial information from the PostGres database's table to populate the web form and 2. it lets us write the calculations to our PostGres table from treasury direct's website.

3. To run this script, you must create a database in PostGreSQL.

	You can do this in the command line via
	`createdb __DBNAME__`

	You can also connect to `psql` and enter the command (or write it into your schema.sql)
	`CREATE DATABASE __DBNAME__;`

	Where `__DBNAME__` is the name you choose for your database. This mix of underscores/caps will be the format for table naming in upcoming instructions as well. *Note- the underscores and caps aren't necessary, but are only there to help identify where a user needs to insert this info in the python code for this program*

4. Then, you must create a single table in this database.
	
	To connect to the database you created from the command line type
	`psql __DBNAME__`

	Alternatively after running `psql` from the command line, type
	`\c __DBNAME__`

	*If you wrote a schema.sql file, then you may run it via `psql __SCHEMA-NAME__.sql`, but this tutorial will direct an end user to create tables directly within `psql` and terminal*

	Once connected, create your table in `psql` using the following format
	`CREATE TABLE __TABLEWITHBONDINFO__ (id SERIAL PRIMARY KEY, !SERIALNUMBERS VARCHAR(13), !ISSUEDATES VARCHAR(7), !ACTUALDATE DATE, !INTERESTCOLUMN VARCHAR(5), !CURRENTVALUECOLUMN VARCHAR(8), !INTERESTAMOUNTCOLUMN VARCHAR(8), !FINALMATURITYCOLUMN VARCHAR(7));`
	
	These are the column names you will have to replace in the query and match in the pyform.py code. This lets us provide info to the webform from our DB and lets us update our tables with information calculated from treasury direct
	* *!SERIALNUMBERS - [inserted by user]* The serial number of each bond will be stored in this column and will have to be manually inserted into this table
	* *!ISSUEDATES - [inserted by user]* The issue date of each bond will be stored in this column and will have to be manually inserted into this table
	* *!ACTUALDATE [optional (but recommended), inserted by user]* - The actual date of issue, also a good way to organize the data if things are mistakenly inserted out of order (making the id column unreliable to sort by), but also requires manual insertion into this table
	* *!INTERESTCOLUMN -* The interest rate a bond grows at determined by treasury direct's bond calculator after the above information is entered into it. Will be updated into the database automatically via pyform.py
	* *!CURRENTVALUECOLUMN -* The total value of the bond as of the 'Value as of' date, also updated automatically in the database via pyform.py
	* *!INTERESTAMOUNTCOLUMN -* The amount of money that has been made solely in interest collected, automatically updated in the PostGres DB/table via pyform.py
	* *!FINALMATURITYCOLUMN -* The month and year that the bond will reach its final maturity, automatically updated via pyform.py

5. You must manually insert information into the `__TABLEWITHBONDINFO__` table via the command

	`INSERT INTO __TABLEWITHBONDINFO__ (!SERIALNUMBERS, !ISSUEDATES, !ACTUALDATE) VALUES ('X18230880ABC', 'MM/YYYY', 'YYYY-MM-DD');`

	Replacing the table name and column names with the ones you chose and the values according to the information on a single bond. *Note that you can press the ^(up) key to access the last command you ran and can edit that query with the values from the next bond you want to insert*

	*Also take note of the format for the optional !ACTUALDATE column. This is how PostGreSQL stores dates that can be used to order a table or isolate a specific year, year and month, or month. You must follow this format when entering the actual date printed on each bond if you chose to include this column.*

6. Once this information has been inserted, you can open the `pyform.py` file and replace the `__DBNAME__`, `__TABLEWITHBONDINFO__`, !SERIALNUMBERS, !ISSUEDATES, !ACTUALDATE, !INTERESTCOLUMN, !CURRENTVALUECOLUMN, !INTERESTAMOUNTCOLUMN, and !FINALMATURITYCOLUMN variables in the script with the names you chose while creating your table and PostGreSQL database.

7. Additionally on line 31 of the code, you can change the value from the default of '$100' to a different denomination according to what your bonds are valued at.

	*If you have bonds at different values, it'd be a good idea to put them in separate tables and edit the code to work with one table or another at a specific denomination.*

	**This is the optional line that can be copied/pasted and can be used to change the bond series if you aren't calculating series EE bonds.**

	You might also notice that lines 26-8 are commented out, but they will allow you to change the 'Value as of' field. *Note that you can only go as far as 4 months into the future (ie. it's 01/2016, so up to 05/2016) with treasury direct's calculator, or any date in the past. The explanation to this is that interest rates after '95 for series EE bonds are based on a weird calculation that's based on the economy at a specific time.*

8. To run this script once the heavy lifting has been done simply `cd` into the pyform directory and run the command

	`python pyform.py`

	**This will open the web browser, populate, submit each bond, and update the database with the info from the resulting table generated by treasury direct's calculator.**

**Final Note!** This script was written to work with FireFox by Mozilla as it has native compatibility with the Selenium library and will open its window focused so you can see everything happen in front of you once the script begins to run.

You can switch this to work with Google Chrome by downloading chromedriver [here](https://sites.google.com/a/chromium.org/chromedriver/downloads), moving the chromedriver file into Google Chrome/Contents (right click on Google Chrome in Applications, click 'Show Package Contents', double click the 'Contents' folder, and drop the file in there [or use the `mv` command]), comment out line 9 in the script and uncomment line 10.

*Note- Google Chrome will open in the background, which will result in the awkward experience of navigating to the window yourself as the script is running. It will run a bit faster than Firefox, but if you're going with Chrome, then that's my forewarning*

**Congrats!** You got this script working for whatever reason you needed to make it work. The great thing is that if you want to, you can run this script over and over to show it off, or just to have a rapid way to evaluate your savings again at another time in the future. Either way, pat yourself on the back and get yourself a well earned iced coffee! Or a milkshake if you're not into that.