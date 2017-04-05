<?php
$limitPrint = 120;
$fileJson = "report/beerFreezer.json";
$alert = null;

# Verifica se o arquivo já foi gerado
if (! file_exists($fileJson)) {
  $alert = "Arquivo <code>$fileJson</code> ainda não gerado para demonstração de relatório gráfico. Verifique se o comando <code>python3 beerFreezer.py</code> foi executado com sucesso.";
} else {
  # Lendo arquivo json e separando os dados
  $file = new SplFileObject($fileJson, 'r');
  $file->seek(PHP_INT_MAX);
  $last_line = $file->key();

  if ($last_line < $limitPrint) {
      $limitPrint = $last_line;
  }

  $lines = new LimitIterator($file, $last_line - $limitPrint, $last_line);
  $array = iterator_to_array($lines);

  if ($limitPrint >= 30) {
      for ($i = $last_line; $i > $last_line - $limitPrint; $i -= 2) {
          unset($array[$i]);
      }
  }

  # Variáveis de retorno no arquivo json
  $temperatura_termometro = array();
  $temperatura_setado = array();
  $limite_temperatura_alta = array();
  $limite_temperatura_baixa = array();
  $status_do_freezer = array();
  $tempo_freezer_status = array();
  $data = array();

  $countON = 0;
  $countOFF = 0;
  $countPrevious = null;
  $countCurrent = null;

  foreach ($array as $key => $value) {
    if (!empty($value)) {
      $output = str_replace("'",'"',$value);
      $output = utf8_encode($output);
      $json = json_decode($output);

      array_push($temperatura_termometro, $json->{'temperatura termometro'});
      array_push($temperatura_setado, $json->{'temperatura setado'});
      array_push($limite_temperatura_alta, $json->{'limite temperatura alta'});
      array_push($limite_temperatura_baixa, $json->{'limite temperatura baixa'});
      array_push($status_do_freezer, $json->{'status do freezer'});
      array_push($tempo_freezer_status, $json->{'tempo freezer status'});
      array_push($data, $json->{'data'});

      $countCurrent = $json->{'status do freezer'};
      if ($countCurrent != $countPrevious) {
        if ($json->{'status do freezer'} == 0) {
          $countOFF++;
        } else {
          $countON++;
        }
      }
      $countPrevious = $countCurrent;
    }
  }

  $result_temperatura_termometro = json_encode(array_values($temperatura_termometro));
  $result_temperatura_setado =json_encode(array_values($temperatura_setado));
  $result_limite_temperatura_alta = json_encode(array_values($limite_temperatura_alta));
  $result_limite_temperatura_baixa = json_encode(array_values($limite_temperatura_baixa));
  $result_status_do_freezer = array_values($status_do_freezer);
  $result_tempo_freezer_status = array_values($tempo_freezer_status);
  $result_data = json_encode(array_values($data));
}
?>

<!DOCTYPE html>
<html lang="pt_BR">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="180">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>beerFreezer</title>

    <!-- Bootstrap -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">

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


        <!-- HEADER -->
        <div class="row">
          <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12 page-header">
           <h1>beerFreezer</h1>
          </div>
        </div>
        <!-- / HEADER -->



        <!-- CONTENT -->
        <div class="row">

          <!-- Alert -->
          <?php if ($alert != null) : ?>
          <div class="col-lg-2 col-md-2"></div>
          <div class="col-lg-7 col-md-7 col-sm-12 col-xs-12 text-center">
            <p style="font-size: 72px; color: #3b3a39;"><i class="fa fa-frown-o" aria-hidden="true"></i></p>
            <p style="font-size: 18px; color: #3b3a39;"><?="$alert"?></p>
          </div>
          <!-- / Alert -->

          <?php else : ?>

          <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="col-lg-4 col-md-4 col-sm-4 col-xs-4">
              <h3>
                Freezer:
                <?php if (end($result_status_do_freezer) == 0) : ?>
                <span style="color:#cc3300;"><i class="fa fa-power-off" aria-hidden="true"></i> OFF <small><?=end($result_tempo_freezer_status)." ($countOFF)x"?></small></span>
                <?php else : ?>
                <span style="color:#00cc33;"><i class="fa fa-power-off" aria-hidden="true"></i> ON <small><?=end($result_tempo_freezer_status)." ($countON)x"?></small></span>
                <?php endif ?>
              </h3>
            </div>
          </div>

          <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="panel panel-default">
              <div class="panel-heading text-center">Gráfico de temperaturas</div>
              <div class="panel-body">
                <canvas id="chartTemperatura"></canvas>
              </div>
            </div>
          </div>

          <?php endif ?>
        </div>
        <!-- / CONTENT -->
      </div>
    </div>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>

    <!-- Chart.js (http://www.chartjs.org/) -->
    <script type="text/javascript" src="Chart.min.js"></script>
    <script>
      var ctx = document.getElementById("chartTemperatura");
      var chartTemperatura = new Chart(ctx, {
        type: 'line',
        data: {
          labels: <?php echo $result_data?>,
          datasets: [{
            label: 'Temperatura do sensor',
            fill: false,
            lineTension: 0,
            data: <?php echo $result_temperatura_termometro; ?>,
            backgroundColor: "rgba(204, 51, 51, 0.25)",
            borderColor: "rgba(204, 51, 51, 0.74)"
          }, {
            label: 'Temperatura indicado',
            fill: false,
            lineTension: 0,
            data: <?php echo $result_temperatura_setado; ?>,
            backgroundColor: "rgba(51, 204, 102, 0.25)",
            borderColor: "rgba(51, 204, 102, 0.74)"
          }, {
            label: 'Temperatura máxima tolerável',
            fill: false,
            lineTension: 0,
            data: <?php echo $result_limite_temperatura_alta; ?>,
            backgroundColor: "rgba(255, 153, 51, 0.25)",
            borderColor: "rgba(255, 153, 51, 0.74)"
          }, {
            label: 'Temperatura mínima tolerável',
            fill: false,
            lineTension: 0,
            data: <?php echo $result_limite_temperatura_baixa; ?>,
            backgroundColor: "rgba(51, 153, 204, 0.25)",
            borderColor: "rgba(51, 153, 204, 0.74)"
          }]
        },
        options: {}
      });
    </script>
  </body>
</html>
