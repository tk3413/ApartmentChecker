# -*- coding: utf-8 -*-
from selenium import webdriver
import smtplib
import datetime
import time

# Starting the Chrome Webdriver and sending us straight to floor plans
driver = webdriver.Chrome('C:/chromedriver.exe')
driver.get("http://www.vitatysons.com/floor-plans/")

# Checks to see if any studio apartments are found and if so, then will
# call the checkPrice() method to see if they are affordable or not
def checkStudios():
    print("Checking for studios...")
    driver.find_element_by_class_name("block-0").click()
    found = driver.find_element_by_class_name("results-found").text
    if "Apartments found: " in found:
        print(found)
        checkPrice()
        driver.back()
    else:
        print("None available")
        driver.back()

# Checks to see if any one bedrooms are found and if so, will
# call the checkPrice() method to see if they are affordable or not
def checkOneBeds():
    print("Checking for one bedrooms...")
    driver.find_element_by_class_name("block-1").click()
    found = driver.find_element_by_class_name("results-found").text
    if "Apartments found: " in found:
        print(found)
        checkPrice()
        driver.back()
    else:
        print("None available")
        driver.back()

# This finds and sends the price to be split into something more searchable
def checkPrice():
    print("Checking the prices...")
    try:
        price = driver.find_element_by_css_selector("body > div.container-fluid > div.floorplans.list > div > section.inner-section > div.section-2 > div > div:nth-child(3) > a > figure > figcaption > div > ul > li:nth-child(4)").text
        splitForPice(price)
    except:
        print("Couldn't find the price")

# This method is splitting the format from "STARTING FROM $3,000/MONTH"
# to just $3,000, which is then parsed to see if it is affordable or not
# If it is affordable, then it will call the sendEmail() method to send
# me a notification
def splitForPice(text):
    words = text.split("/")
    amount = words[0].split()
    price = amount[1]
    
    if "1," in price:
        print(amount[1])
        print("BUY NOW")
        sendEmail()
    if "2,0" in price:
        print(amount[1])
        sendEmail()
    else:
        print("Everything is too expensive right now!")

# Method establishes a server and will send me an email, letting me know
# that something affordable is available 
def sendEmail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    fromadd = 'khan.taimore@gmail.com'
    toadd = 'khan.taimore@gmail.com'
    subject = "AFFORDABLE APARTMENT ALERT"
    text = "GO ONLINE NOW AND CHECK IT OUT! http://www.vitatysons.com/floor-plans/"
    server.login("khan.taimore@gmail.com", "PASSWORDGOESHERE")
    msg = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (fromadd, toadd, subject, text)

    server.sendmail(fromadd, toadd, msg)
    server.quit()

# This method just prints out the date and time so I can see when I last
# ran it
def printDate():
	print(time.strftime("%m-%d-%Y %H:%M:%S"))

printDate()
checkStudios()
checkOneBeds()

driver.close()