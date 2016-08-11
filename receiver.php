<?php

$index0 = $_POST["index0"];
$index1 = $_POST["index1"];
#str_replace ( mixed $search , mixed $replace , mixed $subject [, int &$count ] )
#$data = str_replace(" ", "WHITESPACE", $data);
#echo $data;
#$data = utf8_encode($data);
echo '<br>';
echo '<br>';
#$data = json_encode($data);
#var_dump($data);

$result = shell_exec('python sfGenNoun.py '.str($index0). ' '. str($index1));
echo $result;
echo '에이에스디에프';
?>