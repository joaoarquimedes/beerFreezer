<!DOCTYPE HTML>
<html lang="pt_br">
  <head>
    <meta charset="utf-8">
  </head>
  <body>
    <h1>Em desenvolvimento</h1>
  </body>
</html>



<?php
$limitPrint = 3;
$fileJson = "report/beerFreezer.json";

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
        //var_dump($json);
    }
}
?>
