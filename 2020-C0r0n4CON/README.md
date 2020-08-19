# Write-up C0r0n4CON

* [Welcome](#welcome)
* [Stego - Paperrolling](#stego---paperrolling)
* [Stego - DNACovid19](#stego---dnacovid19)
* [Stego - TODOVAASALIRBIEN](#stego---todovaasalirbien)
* [Forensics - wall_paint](forensics---wall_paint)


## Welcome
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

**flag{welcome_b00mer_&lt;redacted>!}**


## Stego - Paperrolling
<p align="center">
  <img src="images/paperrolling.png">
</p>

Archivos: <a href="challs/stego/paperrolling.gif.gz">paperrolling.gif.gz</a>

Extraigo el archivo comprimido. Le paso binwalk al GIF veo que hay un zip. Lo extraigo con `dd if=paperrolling.gif of=extracted.zip bs=1 skip=820154` y al tratar de descomprimirlo veo que tiene pass, por lo que intento forzarlo con `zip2john extracted.zip > john.hash; john --wordlist=/usr/share/wordlists/rockyou.txt john.hash`, lo cual no da resultado. Le paso un `strings` y un `exiftool` pero no da nada de información, por lo que pienso que igual está en las imagenes del GIF. 

Veo que el gif tiene un frame que aparece algo y saco los frames con `ffmpeg -i paperrolling.gif -vsync 0 temp/temp%d.png`. Un frame contiene el link: https://es.wikipedia.org/wiki/COVID-19, por lo que igual la contraseña es una palabra de esta página. 

Hago un diccionario con cewl de la página: `cewl https://es.wikipedia.org/wiki/COVID-19 -w covid19.txt`. Tras un rato que no acababa, lo decido parar y pruebo de nuevo con john y este diccionario, resultando que la contraseña es "cuarentenas". El zip contiene la flag.

**flag{maXiroll&lt;redacted>}**


## Stego - DNACovid19
<p align="center">
  <img src="images/dnacovid19.png">
</p>

Archivos: <a href="challs/stego/seqfragment.zip">seqfragment.zip</a>

La imagen contiene una secuencia de nucleótidos, lo que me hace pensar en algún tipo de esteganografía basada en esto. Encuentro varios materiales por Internet, y este script en Python me permite decodificar la cadena que extraigo a mano de la imagen: https://raw.githubusercontent.com/omemishra/DNA-Genetic-Python-Scripts-CTF/master/dnacode.py

La salida es una cadena en Base32, ya que está todo en mayúsculas, y al decodificarla genera una secuencia hexadecimal que al decodificarla de nuevo proporciona la flag.

**flag{MuRcIeLaG0_&lt;redacted>}**


## Stego - TODOVAASALIRBIEN
<p align="center">
  <img src="images/todovaasalirbien.png">
</p>

Archivos: <a href="challs/stego/EL-4RCOIRIS-TODO-VA-A-SALIR-BIEN-.zip">EL-4RCOIRIS-TODO-VA-A-SALIR-BIEN-.zip</a>

Dentro del zip hay un PDF, que al abrirlo veo que en la segunda hay un archivo adjunto llamado "sin_barreras.txt". Al abrirlo se ve una cadena en Base64, que al decodificarla genera una imagen PNG. Al abrirla veo que se trata de un código de barras, y mediante la página https://zxing.org/w/decode lo decodifico y obtengo la flag.

**flag{r3sistir3_&lt;redacted>}**

## Forensics - wall_paint
<p align="center">
  <img src="images/wall_paint.png">
</p>

El reto pesa más de 2GB, por lo que dejo los enlaces que proporcionaban.
<ul>
  <li><a href="https://drive.google.com/file/d/10HlcmXQeWzBbAd7v-wCwXvUmENnkZ3am/view?usp=sharing">Mirror 1</a></li>
  <li><a href="https://drive.google.com/file/d/1UQj-Xal06qRWEuGZYYAMrDOT5DzeizXi/view?usp=sharing">Mirror 2</a></li>
  <li><a href="https://mega.nz/file/BqZEwQ7I#SIKDb8CQPhp18FUzT6gk00Bv-YoszfoNmsXoUSZGtB8">Mirror 3</a></li>
</ul>


Descomprimo la imagen con gunzip y la meto en Autopsy. Veo que se trata de una imagen de un Debian 10.3. El resumen del análisis me indica que hay 3 mensajes de correo. En el primero hay un mensaje del usuario en el que pide unos paquetes de unos nuevos proyectos. El siguiente es la respuesta (con faltas de ortografía, típico de los malos) al correo anterior, en el que va adjunto un archivo llamado "corpwallpaper_1.0.deb" y le indica una contraseña de instalación. El último correo es un mensaje de alarma de que se ha producido una intrusión y de que se ignore cualquier correo que provenga de su cuenta o de alguna que se le parezca. Me fijo que la dirección de ambas cuentas difiere en que una 'o' es un '0', por lo que está claro que el paquete debe ser el malware.

Lo extraigo de Autopsy y con `dpkg -e corpwallpaper_1.0.deb` vuelco los scripts que se ejecutan al instalarlo. En el script de post-instalación (postinst), veo que hay un descifrado de un archivo .sh con el comando `openssl aes-256-cbc -a -salt -d -in /tmp/st.sh -pass pass:$password 2>/dev/null`. Extraigo el contenido del paquete con `7z x corpwallpaper_1.0.deb; tar -xvf data.tar`, y descifro el archivo "st.sh" con el mismo comando del script y la contraseña del correo: `openssl aes-256-cbc -a -salt -d -in tmp/st.sh -pass pass:YTM0NGNmZDdjY2NhYTc5OGVmZmQ5NTZlNWUyYTA3YTUgIC0K`. La salida es un echo con la flag.

**flag{ur_1nf3ct3d_&lt;redacted>}**

ph -> pphh
```
Luego se organizaría en la forma: <payload_cr><payload_ed>s.<payload_ph>p

En python se puede generar bien rápido así: (img)

Este es el input que use en el reto: `cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrreeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddds.ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppphhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhp:1337@lol.lol`

Cuyo SHA1 es: 9e64b58bf2f273142a77ce091a00555f04bfa717

Finalmente, para conseguir dumpear la variable "info", ejecuto los siguientes comandos: