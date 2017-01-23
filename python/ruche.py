#!/usr/bin/python
#-*- coding: utf-8 -*-
#### Import des librairies Python #############

## Librairies pour lecture capteurs de type DHT11, DHT22 et AM2302.
import Adafruit_DHT			

## Librairies pour récupérer lheure et la date.
import time
from datetime import datetime

## Librairies pour envoi emails.
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

maintenant = datetime.now()

#### Récupération date et heure actuelles #############
timestamp = time.strftime("%H:%M")
daystamp = time.strftime("%Y-%m-%d")



#### creation du fichier pour collecter les données chaque jour #############
#### si le fichier existe, il n'est pas écrasé
filename = "".join(["/home/pi/beebox/data/ruche/ruche-", daystamp, ".csv"])

#### Definition des seuils température et humidité #############
templow = 10.0
temphigh = 40.0
humlow = 50.0
humhigh = 80.0


#### Definition paramètres email #############
fromaddr = "beebox.eco@gmail.com"
toaddr = "your-email@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
title = "Alerte Ruche: Seuil atteint "


# Adafruit_DHT.DHT11, Adafruit_DHT.DHT22 or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT22	 	## Type de capteur
pin = 4   						## RPI GPIO Pin

# Lecture de la temperature et de l'humidité du capteur DHT22.
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)


#### A supprimer pour l'experimentation : juste pour les tests si les capteurs ne sont pas connectés ###################
#### génère une valeur aléatoire pour la température et l'humidité pour simuler les capteurs #####
import random
temperature = random.randint(15, 18)
humidity = random.randint(63, 68)
#print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
#################


# si temperature = None ( probleme capteur) on met la valeur à zéro pour  éviter une entrée vide dans le fichier de données .csv
if temperature == None:
	str_temp = "0"

	# si humidity = None ( probleme capteur) on met la valeur à zéro pour  éviter une entrée vide dans le fichier de données .csv
if humidity == None:
	str_hum = "0"

# si les valeurs des capteurs ne sont pas "None" ( capteurs OK) 
if not humidity == None and not temperature == None:
    
	temperature = float(temperature)
	humidity = float(humidity)
	temperature = format(temperature, '.1f')
	humidity = format(humidity, '.2f')
	
	str_temp = str(temperature)
	str_hum = str(humidity)

# génération d'une chaine de caractères à insérer dans le fichier csv comprenant l'heure, la température et l'humidité
str_chain = timestamp +";" + str_temp +";" + str_hum 


# ouverture du fichier et écritures des données en ajoutant une ligne à la fin
fichier = open(filename, "a")      
fichier.write(str_chain +"\n")
fichier.close()
 
 

#### Email d'alerte si seuil température ou humidité est atteint #############"
#### Si la temperature ou l'humidité n'est pas comprise dans les valeurs limites définies, un email d'alerte est envoyé à l'adresse configurée.
if not (templow < temperature < temphigh) or not (humlow < humidity < humhigh):

	msg['Subject'] = title
	body = "Alerte Ruche:  le " +str(daystamp) +" à " +str(timestamp) +" la température = " +str(temperature) +" °C et l'humidité = " +str(humidity) + " %" 
	msg.attach(MIMEText(body, 'plain','utf-8'))
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "yourpwd")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
	

#### Email d'alerte si problème capteur #############
if humidity == None or temperature == None:
    title = title + " Problème capteur"
    msg['Subject'] = title
    body = "Alerte Ruche:  le " +str(daystamp) +" à " +str(timestamp) + " il y a eu un problème capteur dans la lecture de la temperature et de l'humidité"
    msg.attach(MIMEText(body, 'plain','utf-8'))
 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "yourpwd")
    text = msg.as_string()

    server.sendmail(fromaddr, toaddr, text)
    server.quit()
