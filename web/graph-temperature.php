<?php
include('./phpgraphlib/phpgraphlib.php'); // Utilisation de librairies pour générer des graphiques
include_once "settings.php";

//Récupération de la date sélectionnée dans le calendrier de l'index.php et envoyée par la methode summit (bouton "Envoyer")
$date = $_POST['date'];

//mise en forme de la date au format YYYY-MM-dd
$date1 = explode("/", $date);
$graphdate=$date1[2].'-'.$date1[0].'-'.$date1[1];

// Sélection du fichier de la ruche de la forme /home/pi/beebox/data/ruche/ruche-YYYY-MM-dd.csv selon la date choisie
$file1 = $folder1.$graphdate.'.csv';

// Sélection du fichier du capteur extérieur de la forme /home/pi/beebox/data/exterieur/exterieur-YYYY-MM-dd.csv selon la date choisie
$file2 = $folder2.$graphdate.'.csv';

// Lecture ligne par ligne du fichier de données de la ruche
	 IF(($handle = fopen($file1, "r")) !== FALSE)
    {      
		WHILE(($column = fgetcsv($handle, 1000, ';', '"')) !== FALSE)
        {
			// copie dans le tableau set1 de l'heure ( première valeur venant de $column[0]) et de la température (seconde valeur venant $column[1] ) 	
			$set1[$column[0]] = $column[1];
        }
    }

// Lecture ligne par ligne du fichier de données du capteur extérieur
	 IF(($handle = fopen($file2, "r")) !== FALSE)
    {      
 
		WHILE(($column = fgetcsv($handle, 1000, ';', '"')) !== FALSE)
        {
         	// copie dans le tableau set2 de l'heure ( première valeur venant de $column[0]) et de la température (seconde valeur venant $column[1] ) 	
			$set2[$column[0]] = $column[1];
        }
    }

// Généation des 2 courbes de température ruche et exterieur en utilsant les fonctions de la librairie phpgraphlib
$graph = new PHPGraphLib(1800, 600);
$graph->addData($set1,$set2);
$graph->setTitleLocation('left');
$graph->setTitle("Temperature de la ruche : $graphdate");
$graph->setBars(false);
$graph->setLine(true);
$graph->setDataPoints(false);
$graph->setLineColor('red','blue');
$graph->setDataValues(false);
$graph->setXValuesInterval(1);
$graph->setDataValueColor('red','blue');
$graph->setLegend(true);
$graph->setLegendTitle("Ruche,Exterieur");
$graph->createGraph();



?>