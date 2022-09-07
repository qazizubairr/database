
from turtle import heading
import pandas as pd
import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
import psycopg2.extras
from config import config


list_of_info =[]
params = config()

        # connect to the PostgreSQL server
print('Connecting to the PostgreSQL database...')
conn = psycopg2.connect(**params)
		
        # create a cursor
cur = conn.cursor()

with open("countries1.csv", 'r',encoding='utf-8') as file:
  csvreader = csv.reader(file)

  for row in csvreader:
    options = Options()
    options.add_argument("--headless") # Runs Chrome in headless mode.
    # options.add_argument('--no-sandbox') # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    # options.add_argument('start-maximized') # 
    # options.add_argument('disable-infobars')
    # options.add_argument("--disable-extensions")
    options.add_argument('--log-level=1')
    driver = webdriver.Chrome(chrome_options=options, executable_path=r'C:\Program Files (x86)\chromedriver')
    url='https://en.wikipedia.org/wiki/'+row[0]
    driver.get(url)
    dict_of_info = {'Country':row[0]}
    Country = row[0]
    try:
        time.sleep(3)
        headings=driver.find_elements(By.XPATH,"//table[@class='infobox ib-country vcard']/tbody/tr/th[@scope='row']")
        for i, heading in enumerate(headings):
            if  'capital'in heading.text.lower() or 'languages' in heading.text.lower()  or 'religion' in heading.text.lower()   or 'currency' in heading.text.lower() or 'time zone' in heading.text.lower() or'calling code' in heading.text.lower():
                info = heading.find_element(By.XPATH,'../td')
            #     if 'religion' in heading.text.lower():
            #         dict_of_info['Religion']= info.text.replace("\n"," ") 
            #     if 'languages' in heading.text.lower():
            #         dict_of_info['Languages']= info.text.replace("\n"," ") 
            #     if 'capital' in heading.text.lower():
            #         dict_of_info['Capital']= info.text.replace("\n"," ")
            #     if 'currency' in heading.text.lower():
            #         dict_of_info['Currency']= info.text.replace("\n"," ")
            #     if 'time zone' in heading.text.lower():
            #         dict_of_info['Time Zone']= info.text.replace("\n"," ")
            #     if 'calling code' in heading.text.lower():
            #         dict_of_info['Calling code']= info.text.replace("\n"," ")
                if 'religion' in heading.text.lower():
                    Religion= info.text.replace("\n"," ") 
                if 'languages' in heading.text.lower():
                    Languages= info.text.replace("\n"," ") 
                if 'capital' in heading.text.lower():
                    Capital= info.text.replace("\n"," ")
                if 'currency' in heading.text.lower():
                    Currency= info.text.replace("\n"," ")
                if 'time zone' in heading.text.lower():
                    TimeZone= info.text.replace("\n"," ")
                if 'calling code' in heading.text.lower():
                    CallingCode= info.text.replace("\n"," ")
             
        postgres_insert_query = """ INSERT INTO countries_info (country,capital,languages,religion,currency,timezone,callingcode) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (Country,Capital,Languages,Religion,Currency,TimeZone,CallingCode)
        cur.execute(postgres_insert_query, record_to_insert)
        conn.commit()
        count = cur.rowcount
        print(count, "Record inserted successfully into countries_info table")
        # list_of_info.append(dict_of_info)         
    except (Exception, psycopg2.Error) as error:
        
        print("Failed to insert record into countries_info table", error)

    finally:
        driver.quit()
if conn:
    cur.close()
    conn.close()
    print("PostgreSQL connection is closed")
# print(list_of_info)       
# keys = list_of_info[0].keys()
# fieldss=["Country",	"Capital",	"Major languages"	,"Religion",	"Currency",	"Time zone",	"Calling code"]

    
# with open('countries1.csv', 'w+', newline='',encoding="utf-8") as output_file:
#     dict_writer = csv.DictWriter(output_file, keys,extrasaction='ignore')
#     dict_writer.writeheader()
#     dict_writer.writerows(list_of_info)
#     print("CSV UPDATED....")