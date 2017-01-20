<?php
include('./phpgraphlib/phpgraphlib.php');	// Utilisation de librairies pour générer des graphiques
include_once "settings.php";

//Récupération de la date du jour et l'heure actuelle
$datetime = date("Y-m-d");
$graphdate = date("Y-m-d H:i:s");  

// Sélection du fichier du jour de la ruche de la forme /home/pi/beebox/data/ruche/ruche-2017-01-19.csv par exemple
$file1 = $folder1.$datetime.'.csv';

// Sélection du fichier du jour de lu capteur extérieur de la forme /home/pi/beebox/data/exterieur/exterieur-2017-01-19.csv par exemple
$file2 = $folder2.$datetime.'.csv';

	// Lecture ligne par ligne du fichier de données de la ruche
	 IF(($handle = fopen($file1, "r")) !== FALSE)
    {      
 
		WHILE(($column = fgetcsv($handle, 1000, ';', '"')) !== FALSE)
        {
            // copie dans le tableau set1 de l'heure ( première valeur venant de $column[0]) et de l'humidité (troisième valeur venant $column[2] )
			$set1[$column[0]] = $column[2];
	
        }
    }

	// Lecture ligne par ligne du fichier de données du capteur extérieur
	 IF(($handle = fopen($file2, "r")) !== FALSE)
    {      

		WHILE(($column = fgetcsv($handle, 1000, ';', '"')) !== FALSE)
        {
         	// copie dans le tableau set2 de l'heure ( première valeur venant de $column[0]) et de l'humidité (troisième valeur venant $column[2] )
			$set2[$column[0]] = $column[2];

        }
    }

// Généation des 2 courbes de l'humidité de la ruche et exterieur en utilsant les fonctions de la librairie phpgraphlib
$graph = new PHPGraphLib(1800, 600);
$graph->addData($set1,$set2);
$graph->setTitleLocation('left');
$graph->setTitle("Humidite de la ruche : $graphdate");
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