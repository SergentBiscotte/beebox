#!/usr/bin/python
#-*- coding: utf-8 -*-
#### Import des librairies Python #############

## Librairies pour lecture capteurs de type DHT11, DHT22 et AM2302.
import Adafruit_DHT			

## Librairies pour récupérer lheure et la date.
import time
from datetime import datetime

## Librairies pour envoie emails.
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
toaddr = "laurent.velez@free.fr"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
title = "Alerte Ruche: Seuil atteint "


# Adafruit_DHT.DHT11, Adafruit_DHT.DHT22 or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT22	 	## Type de capteur
pin = 4   						## RPI GPIO Pin

# Lecture de la temperature et de l'humidité du capteur DHT22.
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)


#### A SUPPRIMER dans le cas d'une réelle experimentation : a utiliser uniquement pour les tests si les capteurs ne sont pas connectés ###################
#### génère une valeur aléatoire pour la température et l'humidité pour simuler les capteurs #####
import random
temperature = random.randint(15, 18)
humidity = random.randint(63, 68)
#print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
########################################################################################################################"




#### Email d'alerte si problème capteur #############
if ((humidity == None) or (temperature == None)):
	title = "Alerte Ruche:  Problème capteur"
	msg['Subject'] = title
	body = "Alerte Ruche:  le " +str(daystamp) +" à " +str(timestamp) + " il y a eu un problème capteur dans la lecture de la temperature et de l'humidité"
	msg.attach(MIMEText(body, 'plain','utf-8'))
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "Ecobox06")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
	
	# si temperature = None ( probleme capteur) on met la valeur à zéro pour  éviter une entrée vide dans le fichier de données .csv
	if temperature == None:
		str_temp = "0"
		temperature = 0
		
	# si humidity = None ( probleme capteur) on met la valeur à zéro pour  éviter une entrée vide dans le fichier de données .csv
	if humidity == None:
		str_hum = "0"
		humidity = 0;
	
	str_chain = timestamp +";0;0" 
	
	# ouverture du fichier et écritures des données en ajoutant une ligne à la fin
	fichier = open(filename, "a")      
	fichier.write(str_chain +"\n")
	fichier.close()
	




# si les valeurs des capteurs ne sont pas "None" ( capteurs OK) 
#if (not (humidity == None) and not (temperature == None)):
else:    
	
	fl_temperature = temperature
	fl_humidity = humidity
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
	#if not (templow < temperature < temphigh) or not (humlow < humidity < humhigh):

	if (fl_temperature < templow):
		bodytemp = "Alerte température ! La température de votre ruche est passée en dessous du seuil de " + str(templow) + " °C . Cette ruche doit être surveillée d'urgence. Température de la ruche le " +str(daystamp) + " à " +str(timestamp) + " est de " +  str(temperature) + " °C "
		
	elif (fl_temperature > temphigh):
		bodytemp = "Alerte température ! La température de votre ruche est passée au dessus du seuil de " + str(temphigh) + " °C . Cette ruche doit être surveillée d'urgence. Température de la ruche le " +str(daystamp) + " à " +str(timestamp) + " est de " +  str(temperature) + " °C "
		

	if (fl_humidity < humlow):
		bodyhum = "Alerte humidité ! L'humidité de votre ruche est passée en dessous du seuil de " + str(humlow) + " % . Cette ruche doit être surveillée d'urgence. Humidité de la ruche le " +str(daystamp) + " à " +str(timestamp) + " est de " +  str(humidity) + " % "
		
	elif (fl_humidity > humhigh):
		bodyhum = "Alerte humidité ! L'humidité de votre ruche est passée au dessus du seuil de " + str(humhigh) + " % . Cette ruche doit être surveillée d'urgence. Humidité de la ruche le " +str(daystamp) + " à " +str(timestamp) + " est de " +  str(humidity) + " % "

		
	if not (templow < fl_temperature < temphigh):
		msg['Subject'] = title
		msg.attach(MIMEText(bodytemp, 'plain','utf-8'))
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(fromaddr, "Ecobox06")
		text = msg.as_string()
		server.sendmail(fromaddr, toaddr, text)
		server.quit()

	if not (humlow < fl_humidity < humhigh):
		msg['Subject'] = title
		msg.attach(MIMEText(bodyhum, 'plain','utf-8'))
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(fromaddr, "Ecobox06")
		text = msg.as_string()
		server.sendmail(fromaddr, toaddr, text)
		server.quit()	


