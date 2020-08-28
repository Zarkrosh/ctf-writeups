# Write-up RESTCON CTF

* [Forensics - Magic](#forensics---magic)
* [Forensics - Dance Monkey](#forensics---dance-monkey)
* [Forensics - Dumpster Diving 1](#forensics---dumpster-diving-1)
* [Forensics - Mirror](#forensics---mirror)
* [Forensics - Binod](#forensics---binod)
* [Forensics - Bad Cat](#forensics---bad-cat)
* [Misc - QR Code](#misc---qr-code)
* [Web - I am secure](#web---i-am-secure)
* [Web - Developer Be Careful](#web---developer-be-careful)
* [Web - Play With Django](#web---play-with-django)
* [Basic - In Plain Sight](#basic---in-plain-sight)
* [Basic - Weirdo](#basic---weirdo)


## Forensics - Magic

Archivos: <a href="challs/forensics/magic/output.png">output.png</a>

El QR contiene la flag y en su interior un MD5 asociado a la cadena "mirr0r".

**RESTCON{mirr0r}**


## Forensics - Dance Monkey

Archivos: <a href="challs/forensics/dance_monkey/monkey.gif">monkey.gif</a>

La flag se encuentra en los metadatos del GIF, codificada en Base32. 

**RESTCON{SMIL3_L!K3_4_M0NK3Y}**


## Forensics - Dumpster Diving 1

Archivos: <a href="challs/forensics/dumpster_diving/firefox.zip">firefox.zip</a>

El ZIP contiene un dump de Firefox. La flag se obtiene consultando el contenido de la base de datos **places.sqlite** en x2p79maw.default-esr, la cual contiene el historial en la tabla **moz_places**. Entre las páginas visitadas se encuentran varias peticiones a Cyberchef con la entrada "d753753464f533f413539513f59533f4f41335f525437515b795a5e454440534". Aplicando las operaciones Reverse - From Hex - ROT13 se obtiene la flag.

**RESTCON{FL4G_H1DD3N_1N51D3_URL5}**


## Forensics - Mirror

Archivos: <a href="challs/forensics/mirror/Armin_van_Buuren_-_Blah_Blah_Blah_Official.mp3">Armin_van_Buuren_-\_Blah_Blah_Blah_Official.mp3</a>

Se analiza el MP3 en Sonic Visualizer y se detectan cortes en el espectrograma: en el primero se oye una voz diciendo "pastebin.com/" y luego se oye un mensaje en código Morse: ```--.. .- .-- . .-- --... -.-- --...``` -> ```ZAWEW7Y7```.

Como el código Morse no distingue entre mayúsculas y minúsculas, genero una lista de peticiones a realizar con todas las combinaciones posibles de mayúscula/minúscula. Automatizo el proceso con curl observando el código de respuesta.

```
for url in $(echo https://pastebin.com/{Z,z}{A,a}{W,w}{E,e}{W,w}7{Y,y}7); 
  do curl -sL -w "%{http_code}" -I $url -o /dev/null | grep 200 && echo $url;
done
```

La página que da un 200 contiene un enlace a una imagen PNG en Google Drive, la cual no se previsualiza. Al descargarla compruebo con file que no se detecta ningún formato. Abro el archivo en un editor hexadecimal y sí tiene el formato PNG pero el nombre del chunk IHDR está en minúsculas. Al modificarlo se puede visualizar la imagen, la cual está del revés con la flag escrita.

**RESTCON{r3v3rs3_m!rr0ring}**


## Forensics - Binod

Archivos: <a href="challs/forensics/binod/logs.pcapng">logs.pcapng</a>

El archivo es un log de tráfico. En algunos paquetes TCP se puede ver una conversación, y luego una descarga HTTP de un archivo llamado binod.exe. Transformo el PCAPNG a PCAP con tshark (```tshark -F pcap -r logs.pcapng -w logs.pcap```) para extraer los archivos con NetworkMiner.

Con file compruebo que no se trata de un EXE sino de un PDF. Al cambiar la extensión y al abrirlo se ve un mensaje y una larga cadena en Base64 que al decodificarla es la palabra "Binod" repetida muchas veces. No parece haber esteganografía visual por lo que paso a analizar el PDF con **peepdf** (```peepdf -i binod.pdf```). Me da un error, por lo que fuerzo el análisis (```peepdf -if archivo.pdf```)

La flag está contenida en el objeto 3. En la consola interactiva de peepdf: (object 3)
```
<< /Type /Action
/S /JavaScript
/JS alert("resetcon{b1n0d_1$_c00l_1$n7_h3?}");
>>
```

**resetcon{b1n0d_1$\_c00l_1$n7_h3?}**


## Forensics - Bad Cat

Archivos: <a href="challs/forensics/bad_cat/cat.png">cat.png</a> 

Con zsteg sale directa la flag:
```
b1,r,lsb,xy         .. text: "tU>vW~Q;<"
b1,rgb,lsb,xy       .. text: "You pressed my belly and got some fish heads and Flag RESTCON{1_eaten_Y0ur_Fl4g}"
b2,g,msb,xy         .. text: "TU@UUUUU"
b2,b,msb,xy         .. file: Apple DiskCopy 4.2 image \212\302\011\336\212, 1347769685 bytes, 0x5000050 tag size, 0x15 encoding, 0x0 format                                                                                         
b2,rgb,msb,xy       .. text: "l{<M`U\t<}"
b2,bgr,msb,xy       .. text: "@UUUUUUUUU"
b2,abgr,msb,xy      .. text: "GGGGGGSSSSSSSSSSSSSS"
b3,b,lsb,xy         .. text: "Fv)b[6`AliQ"
b3,rgb,lsb,xy       .. file: old packed data
b3,bgr,msb,xy       .. text: "0{v-~4!D"
b4,r,lsb,xy         .. text: "wfEDTFggvfgf"
b4,r,msb,xy         .. text: "3swwwwwwwww"
b4,g,lsb,xy         .. text: "wwvTB#\"3"
b4,g,msb,xy         .. text: "UUU5UUUUU533333333333333333333SUUUUUU"
b4,b,lsb,xy         .. text: "WTFffvfi"
b4,b,msb,xy         .. text: "DDDDD$\"\"\"\"\"\"\"\"bff"
b4,rgb,lsb,xy       .. text: "#c'3bW%sF5cv'cg6cf&"
b4,bgr,lsb,xy       .. text: "C&#c7Re'Cu6sg&cf7cf&b"
b4,rgba,lsb,xy      .. text: "b?c/s?b_r_sOc_c"
```

**RESTCON{1_eaten_Y0ur_Fl4g}**


## Misc - QR Code

Archivos: <a href="challs/misc/qr_code/QRCODE.zip">QRCODE.zip</a>

El ZIP contiene 5000 imágenes de códigos QR, de los cuales uno contiene la flag y el resto contienen una flag falsa "RESTCON{FAKEFLAGX}". Con el comando **zbarimg** decodifico los QR y hago un grep inverso de una subcadena común en las flags falsas.

```zbarimg * | grep -v "FAKE"```   

**RESTCON{LMAO_YOU_GOT_ME}**


## Web - I am secure

El archivo **robots.txt** contiene:
```
User-agent: *

allow : /

Disallow: /b026324c6904b2a9cb4b88d6d61c81d1
Disallow: /26ab0db90d72e28ad0ba1e22ee510510
Disallow: /6d7fce9fee471194aa8b5b6e47267f03
Disallow: /48a24b70a0b376535542b996af517398
Disallow: /1dcca23355272056f04fe8bf20edfce0
Disallow: /9ae0ea9e3c9c6e1b9b6252c8395efdc1
Disallow: /84bc3da1b3e33a18e8d5e1bdd7a18d7a
Disallow: /c30f7472766d25af1dc80b3ffc9a58c7
Disallow: /7c5aba41f53293b712fd86d08ed5b36e
Disallow: /31d30eea8d0968d6458e0ad0027c9f80 
```

Pruebo las URLs hasta que una da resultado: /9ae0ea9e3c9c6e1b9b6252c8395efdc1
La flag está al final del código fuente, tras unas cuantas líneas en blanco.

**RESTCON{R0bots_can't_prevent_from_1337_hacker}**


## Web - Developer Be Careful

La página principal da la pista "I told the developer to be careful while making a git commit". Pruebo a ver si existe el directorio /.git, sin éxito. La página contiene un enlace al blog personal del desarrollador, y en ella un enlace a su GitHub. En los últimos repositorios modificados veo uno con la descripción <a href="https://github.com/altafshaikh/past_never_leaves">Restcon 2020 CTF Challenge</a>.

En el commit "removed" se ve la eliminación de la flag.

**RESTCON{g1t_ch3ck0ut}**

## Web - Play With Django

Archivos: <a href="challs/misc/web/play_with_django/findme.zip">findme.zip</a>

El ZIP contiene un servidor web con una BD SQLITE. Tras trastear creando un superusuario e inspeccionando los contenidos de la BD, encuentro la flag en el template de la página de inicio /core/templates/core/index.html), la cual debería aparecer en la página si estuviera loggeado como el usuario "sudo".

**RESTCON{intr0_t0_djang0}**


## Basic - In Plain Sight

Archivos: <a href="challs/basic/in_plain_sight/bum_tam_tam.txt">bum_tam_tam.txt</a>

La descripción contiene un '.' con un enlace a un TXT con una canción, la cual está en minúsculas pero hay algunas letras en mayúsculas. Extrayendo las que son mayúsculas se obtiene la cadena "YOUGOTTHEFLAGFROMBUMTAMTAM". Como el reto pide que la flag esté en L33T SPEAK, utilizo https://www.dcode.fr/leet-speak-1337

**RESTCON{Y0U6077H3F146Fr0M8UM74M74M}**


## Basic - Weirdo

Archivos: <a href="challs/basic/weirdo/weirdo.txt">weirdo.txt</a>

El archivo de texto contiene instrucciones en el lenguaje esotérico **Malbolge**. Con un <a href="http://malbolge.doleczek.pl/">intérprete online</a> se ejecuta el programa, que imprime la flag.

**RESTCON{Malb0lg3_is_cool}**