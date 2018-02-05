#!/usr/bin/python
#-*- coding: utf-8 -*-
import Adafruit_DHT
import time
from datetime import datetime

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

maintenant = datetime.now()

#### Récupération date et heure #############
timestamp = time.strftime("%H:%M")
daystamp = time.strftime("%Y-%m-%d")



#### creation du fichier de données pour chaque jour #############
filename = "".join(["/home/pi/beebox/data/exterieur/exterieur-", daystamp, ".csv"])


#### Definition paramètres email pour les alertes #############
fromaddr = "beebox.eco@gmail.com"
toaddr = "your-email@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
title = "Alerte : "


# Adafruit_DHT.DHT11, Adafruit_DHT.DHT22 or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.AM2302	## Type de capteur
pin = 22						## RPI GPIO Pin

# Lecture de la temperature et de l'humidité du capteur AMT2302
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

#### A supprimer pour l'expérimentation : juste pour les tests si les capteurs ne sont pas connectés ###################
#### génère une valeur aléatoire pour la température et l'humidité pour simuler les capteurs #####
import random
temperature = random.randint(2,10 )
humidity = random.randint(80, 95)
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
    
	temperature = format(temperature, '.1f')
	humidity = format(humidity, '.2f')
	
	
	str_temp = str(temperature)
	str_hum = str(humidity)

# génération d'une chaine de caractères à insérer dans le fichier csv comprenant l'heure, la température et l'humidité
str_chain = timestamp +";" + str_temp +";" + str_hum 

# Ouverture du fichier et écritures des données en ajoutant une ligne à la fin
fichier = open(filename, "a")      
fichier.write(str_chain +"\n")
fichier.close() 


#### Email d'alerte si problème capteur #############"
if humidity == None or temperature == None:
    title = title + " Problème capteur exterieur"
    msg['Subject'] = title
    body = "Alerte capteur exterieur:  le " +str(daystamp) +" à " +str(timestamp) + " il y a eu un problème capteur dans la lecture de la temperature et de l'humidité"
    msg.attach(MIMEText(body, 'plain','utf-8'))
 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "yourpwd")
    text = msg.as_string()

    server.sendmail(fromaddr, toaddr, text)
    server.quit()	

