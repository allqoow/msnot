<?php

$data = $_POST["sourcetext"];
#str_replace ( mixed $search , mixed $replace , mixed $subject [, int &$count ] )
$data = str_replace(" ", "WHITESPACE", $data);
#echo $data;
#$data = utf8_encode($data);
echo '<br>';
echo $data;
echo '<br>';
#$data = json_encode($data);
#var_dump($data);

$result = shell_exec('python front.py '.$data);
echo $result;
echo '에이에스디에프';
?>