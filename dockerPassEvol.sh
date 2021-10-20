#!/bin/bash
mkdir tempdir
cp password-evolution tempdir/.
#Crear el DockerFile
#1 Con que  imagen me  voy a basar, python
echo "FROM python" >> tempdir/DockerFile
#2 Crear un volumen VOLUME <path> /datos
echo "VOLUME /datos" >> tempdir/DockerFile
#3 Instalar el gestor de paquetes de python pip 
echo "RUN python3 -m pip install --upgrade pip" >> tempdir/DockerFile
#4 instala flash con pip
echo " RUN pip install flask" >> tempdir/DockerFile
#5 instalar pyopenssl con pip
#6 instalar pyotp
#7 copiar el programa a la imagen  COPY /home/myapp2
#8 ejecutar el programa 
#9 exponer el puerto  EXPOSE
#10 crear la imagen  build
#11  crear el contenedor donde  expongo un puerto y el volumen