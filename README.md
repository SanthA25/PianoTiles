# PianoTiles

Se deben instalar los siguientes paquetes para el correcto funcionamiento del juego.

Para pygame y la reproducción de la canción:
```
pip3 install pygame --upgrade

sudo apt install libsdl2-mixer-2.0

sudo apt-get install python3-sdl2
```

Para el funcionamiento de la OLED, seguir los pasos en el siguiene repositorio: [OLED](https://github.com/selfbg/pyMOD-OLED)

Al iniciar el juego, se le pide al usuario seleccionar la dificultad del juego. 
* [1] - Facil
* [2] - Normal
* [3] - Difícil
* [4] - Imposible

Cada una de las columnas donde aparecen los Tiles representan una tecla, la cual debe er presionada represenando el tile
* [a] - columna 1
* [s] - columna 2
* [d] - columna 3
* [f] - columna 4

Si se llega a presionar una letra equivocada o se presiona una columna cuando no haya ningún Tile en ella, se perderá el juego y se cerrará el programa.

El puntaje se desplegará a un OLED display 128x62, el cual funciona por I2C. De la misma manera, un LED estará parpadeando a la misma velocidad que se haya seleccionado la dificultad del juego.

Todos los archivos de la carpeta *sources* deben permancer ahí.
El archivo de la carpeta *deskFile* se debe mover al escritorio, ya que este representa el acceso directo al juego.

### _VIDEO DEMO_ [PyTiles](https://youtu.be/mjjx0b9AaOU)

![pyTILES](https://user-images.githubusercontent.com/70683976/120878150-26a89400-c580-11eb-8ae9-b24986b29e4a.png)

![OLED_LED](https://user-images.githubusercontent.com/70683976/120878548-db43b500-c582-11eb-80eb-77deeb0b1b3e.jpg)

