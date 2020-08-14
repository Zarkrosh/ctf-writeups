# Write-up C0r0n4CON

[Welcome](#Welcome)
[Stego - Paperrolling](#Stego-Paperrolling)
[Stego - DNACovid19](#Stego-DNACovid19)
[Stego - TODOVAASALIRBIEN](#Stego-TODOVAASALIRBIEN)



## Welcome (1)
En una de las IPs que proporcionan para el reto, veo que indican que el objetivo es llegar a welcome() y nos dan el código fuente para ello.

```
<!DOCTYPE HTML>
<?php
  require("flag.php");

  if (isset($_GET['source'])) {
    highlight_file(__FILE__);
    die();
  }

  if (isset($_GET['hole'])) {

    $rabbit = $_GET['hole'];
    $boomer = 'boomerrabbit';
    $holly = preg_replace(
            "/$boomer/", '', $rabbit);

    if ($holly === $boomer) {
      welcome();
    }
  }
?>

<html>
  <head>
    <title>Welcome</title>
  </head>
  <body>
    <h1>Welcome to Fwhibbit MiniCTF Quarantine Edition 2020</h1>
    <p>Try to reach <code>welcome()</code></p>
    <a target="_blank" href="?source">View source code</a>

  </body>
</html>
```

La cosa está en conseguir que la entrada que se le proporcione a través del parámetro GET 'hole', tras eliminar la cadena 'boomerrabbit' de ella, quede la palabra 'boomerrabbit'. Esto se puede conseguir incluyendo la palabra dentro de la propia palabra: 'boomerboomerrabbitrabbit' -> 'boomerrabbit'.

**flag{welcome_b00mer_<redacted>!}**


## Stego - Paperrolling (50)
<p align="center">
  <img src="images/paperrolling.png">
</p>

Archivos: <a href="challs/stego/paperrolling.gif.gz">paperrolling.gif.gz</a>

Extraigo el archivo comprimido. Le paso binwalk al GIF veo que hay un zip. Lo extraigo con `dd if=paperrolling.gif of=extracted.zip bs=1 skip=820154` y al tratar de descomprimirlo veo que tiene pass, por lo que intento forzarlo con `zip2john extracted.zip > john.hash; john --wordlist=/usr/share/wordlists/rockyou.txt john.hash`, lo cual no da resultado. Le paso un `strings` y un `exiftool` pero no da nada de información, por lo que pienso que igual está en las imagenes del GIF. 

Veo que el gif tiene un frame que aparece algo y saco los frames con `ffmpeg -i paperrolling.gif -vsync 0 temp/temp%d.png`. Un frame contiene el link: https://es.wikipedia.org/wiki/COVID-19, por lo que igual la contraseña es una palabra de esta página. 

Hago un diccionario con cewl de la página: `cewl https://es.wikipedia.org/wiki/COVID-19 -w covid19.txt`. Tras un rato que no acababa, lo decido parar y pruebo de nuevo con john y este diccionario, resultando que la contraseña es "cuarentenas". El zip contiene la flag.

**flag{maXiroll<censored>}**


## Stego - DNACovid19 (100)
<p align="center">
  <img src="images/dnacovid19.png">
</p>

Archivos: <a href="challs/stego/seqfragment.zip">seqfragment.zip</a>

La imagen contiene una secuencia de nucleótidos, lo que me hace pensar en algún tipo de esteganografía basada en esto. Encuentro varios materiales por Internet, y este script en Python me permite decodificar la cadena que extraigo a mano de la imagen: https://raw.githubusercontent.com/omemishra/DNA-Genetic-Python-Scripts-CTF/master/dnacode.py

La salida es una cadena en Base32, ya que está todo en mayúsculas, y al decodificarla genera una secuencia hexadecimal que al decodificarla de nuevo proporciona la flag.

**flag{MuRcIeLaG0_<censored>}**


## Stego - TODOVAASALIRBIEN (100)
<p align="center">
  <img src="images/todovaasalirbien.png">
</p>

Archivos: <a href="challs/stego/EL-4RCOIRIS-TODO-VA-A-SALIR-BIEN-.zip">EL-4RCOIRIS-TODO-VA-A-SALIR-BIEN-.zip</a>

Dentro del zip hay un PDF, que al abrirlo veo que en la segunda hay un archivo adjunto llamado "sin_barreras.txt". Al abrirlo se ve una cadena en Base64, que al decodificarla genera una imagen PNG. Al abrirla veo que se trata de un código de barras, y mediante la página https://zxing.org/w/decode lo decodifico y obtengo la flag.

**flag{r3sistir3_<censored>}**

