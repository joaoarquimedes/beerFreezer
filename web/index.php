<?php
$limitPrint = 30;
$fileJson = "report/beerFreezer.json";

$temperatura_termometro = array();
$temperatura_setado = array();
$limite_temperatura_alta = array();
$limite_temperatura_baixa = array();
$status_do_freezer = array();
$data = array();


# Lendo arquivo json e separando os dados
$file = new SplFileObject($fileJson, 'r');

$file->seek(PHP_INT_MAX);
$last_line = $file->key();
$lines = new LimitIterator($file, $last_line - $limitPrint, $last_line);
$array = iterator_to_array($lines);

foreach ($array as $value) {
    if (!empty($value)) {
        $output = str_replace("'",'"',$value);
        $output = utf8_encode($output);
        $json = json_decode($output);
        //print_r($json);
        array_push($temperatura_termometro, $json->{'temperatura termometro'});
        array_push($temperatura_setado, $json->{'temperatura setado'});
        array_push($limite_temperatura_alta, $json->{'limite temperatura alta'});
        array_push($limite_temperatura_baixa, $json->{'limite temperatura baixa'});
        array_push($status_do_freezer, $json->{'status do freezer'});
        array_push($data, $json->{'data'});
    }
}

$result_temperatura_termometro = json_encode(array_values($temperatura_termometro));
$result_temperatura_setado =json_encode(array_values($temperatura_setado));
$result_limite_temperatura_alta = json_encode(array_values($limite_temperatura_alta));
$result_limite_temperatura_baixa = json_encode(array_values($limite_temperatura_baixa));
$result_status_do_freezer = json_encode(array_values($status_do_freezer));
$result_data = json_encode(array_values($data));
?>

<!DOCTYPE html>
<html lang="pt_BR">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="300">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>beerFreezer</title>

    <!-- Bootstrap -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

    <link rel="stylesheet" type="text/css" href="https://bootswatch.com/yeti/bootstrap.min.css">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    <div class="container">
      <div class="row">
        <h1>beerFreezer</h1>
        <div width="10" height="10">
          <canvas id="myChart"></canvas>
        </div>
      </div>
    </div>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>

    <!-- Chart.js (http://www.chartjs.org/) -->
    <script type="text/javascript" src="Chart.min.js"></script>
    <script>
      var ctx = document.getElementById("myChart");
      var myChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: <?php echo $result_data?>,
          datasets: [{
            label: 'Temperatura do sensor',
            fill: false,
            lineTension: 0.3,
            data: <?php echo $result_temperatura_termometro; ?>,
            backgroundColor: "rgb(82.7%,33.3%,17.6%)",
            borderColor: "rgb(82.7%,33.3%,17.6%)"
          }, {
            label: 'Temperatura indicado',
            fill: false,
            lineTension: 0.3,
            data: <?php echo $result_temperatura_setado; ?>,
            backgroundColor: "rgb(35.7%,62%,46.7%)",
            borderColor: "rgb(35.7%,62%,46.7%)"
          }, {
            label: 'Temperatura máxima tolerável',
            fill: false,
            lineTension: 0.3,
            data: <?php echo $result_limite_temperatura_alta; ?>,
            backgroundColor: "rgb(92.5%,92.2%,67.5%)",
            borderColor: "rgb(92.5%,92.2%,67.5%)"
          }, {
            label: 'Temperatura mínima tolerável',
            fill: false,
            lineTension: 0.3,
            data: <?php echo $result_limite_temperatura_baixa; ?>,
            backgroundColor: "rgb(80.8%,87.8%,94.9%)",
            borderColor: "rgb(80.8%,87.8%,94.9%)"
          }]
        },
        options: {
          title: {
            display: true,
            text: 'Gráfico de temperaturas em graus Celsius'
          }
        }
      });
    </script>
  </body>
</html>
