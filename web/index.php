<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
 
<html xmlns="http://www.w3.org/1999/xhtml">

<?php
// Global settings
include_once "settings.php";
?>

<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>BeeBox</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
	<link rel="stylesheet" href="/resources/demos/style.css">     
  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
 

 <!-- Fonction Javascript pour afficher un calendrier  -->
 <!-- Script utilisé pour selectionner une date pour afficher les graphiques correspondant au jour choisi  -->
 <script>
  $( function() {
    $( "#datepicker" ).datepicker();
  } );
  </script>
</head>
<body>
 
<?php  


$choice = '';
 
// bouton radio pour selectionner le graphique de temperature ou d'humidité pour la date selectionnée 
echo "    <form name= 'graphchoice' method='post' enctype='multipart/form-data'>";
echo "		<input type='radio' name='choice' value='Temperature'/>Temperature -";
echo "		<input type='radio' name='choice' value='Humidite'/>Humidite -";
echo "		<input type = 'submit' value = 'Selectionner'> ";
echo "      <br />";
echo "    </form>";


// Récupération de la valeur du choix bouton radio temperature/humidite et affichage
$choice = $_POST['choice'];
echo "<b><blockquote><font color=\"blue\">  ".$choice."</font></blockquote></b>";
	

	
// Selection de l'action à réaliser selon le choix du bouton radio (temperature ou humidite)	
if ($choice == 'Temperature') {
	$graphfile = 'graph-temperature.php';
	}
else if ($choice == 'Humidite')
	{
	$graphfile = 'graph-humidite.php';
	}	
else {
	$graphfile = '';
}


//affichage calendrier et selection de la date
// selon le choix du bouton radio, generation du graphique correspondant pour la date choisie
if ( ($choice == 'Humidite') || ($choice == 'Temperature') ) {
	
	echo "    <form name= 'formgraph' action='".$graphfile."' method='post' enctype='multipart/form-data'>";
  
// selection de la date et passage de la variable à l'action php choisie (graph-humidite.php ou graph-temperature.php)

	echo "		<p>Selectionnez une date: <input type='text' name='date' id='datepicker'></p>";
// l'action est déclenché avec le bouton "Envoyer"
	echo "		<input type = 'submit' value = 'Envoyer'> ";
  
	echo "      <br />";

	echo "    </form>";
	
}


//Récupération de la date selectionnée dans le calendrier
$date = $_POST['date'];
$datecurrent = date("Y-m-d H:i:s");   // récupération de la date du jour

// Mise en forme de la date au format YYY-MM-dd
$date1 = explode("/", $date);
$graphdate=$date1[2].'-'.$date1[0].'-'.$date1[1];


	echo "<br />";
	
//Affichage de la date et heure
		echo "<b><blockquote><font color=\"red\">Graphiques de la temperature et l'humidité : Aujourd'hui =>  ".$datecurrent."</font></blockquote></b>";
  
echo "<br />";


// Génération et affichage du graphique des températures du jour de la ruche et exterieur
echo '<img src="graph-temperature-current.php" class="overflowingVertical"></img>';

// Génération et affichage du graphique de l'humidité du jour de la ruche et exterieur
echo '<img src="graph-humidite-current.php" class="overflowingVertical"></img>';



?> 

 
  
  </body>
</html>
