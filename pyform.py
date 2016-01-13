#!usr/bin/env python
import psycopg2
from selenium import webdriver
from bs4 import BeautifulSoup, SoupStrainer

## Start up browser (choose between Firefox/Chrome [Chrome opens window in background])
# See readme about installing chromedriver if opting to use Chrome

browser = webdriver.Firefox()
#browser = webdriver.Chrome('/Applications/Google Chrome.app/Contents/chromedriver')

# Navigate to treasury page

treasury_gov = browser.get("http://treasurydirect.gov/BC/SBCPrice")

'''

Fill out bond calculator form.
Submit multiple inputs.
Update PostGreSQL database with results.

'''

## Adjusting inputs (optional, commented out code to change date of evaluation from now to another date)

# value_as_of = browser.find_element_by_name('RedemptionDate')
# value_as_of.clear()
# value_as_of.send_keys('05/2016')

# Change value from $100 to the denomination that matches the value of your bonds
browser.find_element_by_xpath("//select[@name='Denomination']/option[text()='$100']").click()

def fill_form (serial, date):
	# Grab elements
	serial_number = browser.find_element_by_name('SerialNumber')
	issue_date = browser.find_element_by_name('IssueDate')
	calculate = browser.find_element_by_name('btnAdd.x')
	
	# Populate with serial and date
	serial_number.send_keys(serial)
	issue_date.send_keys(date)

	# Submit form
	calculate.click()

def bond_data():
	## Database connection
	DB = psycopg2.connect("dbname=__DBNAME__")
	cursor = DB.cursor()
	
	# Get list of serial numbers and issue dates of bonds
	# (query order reversed to have them formatted old-new in website results)
	serial_date_query = "SELECT !SERIALNUMBERS, !ISSUEDATES FROM __TABLEWITHBONDINFO__ ORDER BY id desc;"
	cursor.execute(serial_date_query)
	
	# Format database results as a list of dictionaries
	bonds = list(({'serial number': row[0], 'issue date': row[1]} for row in cursor.fetchall()))
	DB.close()

	# Loop through dictionary and run fill_form to submit bond serial numbers and issue dates
	for bond in bonds:
		fill_form(bond['serial number'], bond['issue date'])

def fill_database():
	# Click on 'View All' to navigate to full results table with all bonds
	# Use that HTML as the page source
	view_all = browser.find_element_by_name("btnAll.x")
	view_all.click()
	treasury_results = browser.page_source
	
	# Parse the results and pull apart table into a list of rows
	soup = BeautifulSoup(treasury_results, 'html.parser')
	rows = soup.find("table", { "class" : "bnddata" }).find("tbody").find_all("tr")
	
	# Store info from specific cells as a list of dictionaries
	bond_info = []	
	for row in rows:
		cells = row.find_all("td")
		bond_info.append({'final maturity': cells[5].text, 'interest amount': cells[7].text, 'interest': cells[8].text, 'current value': cells[9].text})

	## Database connection
	DB = psycopg2.connect("dbname=__DBNAME__")
	cursor = DB.cursor()

	# Update database with info gathered within each dictionary
	for idx, bond in enumerate(bond_info):
		cursor.execute("UPDATE __TABLEWITHBONDINFO__ SET !FINALMATURITYCOLUMN = %s, !INTERESTAMOUNTCOLUMN = %s, !INTERESTCOLUMN = %s, !CURRENTVALUECOLUMN = %s WHERE id = " + str(idx + 1), (bond['final maturity'], bond['interest amount'], bond['interest'], bond['current value']))
		DB.commit()	

	DB.close()

# Call the functions to submit the bond data and update the database
bond_data()
fill_database()