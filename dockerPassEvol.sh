#!/bin/bash
mkdir tempdir
cp password-evolution.py tempdir/.
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
echo " RUN pip install pyopenssl" >> tempdir/DockerFile
#6 instalar pyotp
echo " RUN pip install pyotp" >> tempdir/DockerFile
#7 copiar el programa a la imagen  COPY /home/myapp2
echo "COPY password-evolution.py /home/myapp2" >> tempdir/DockerFile
#8 ejecutar el programa 
echo "CMD /home/myapp2/password-evolution.py" >> tempdir/DockerFile
#9 exponer el puerto  EXPOSE
echo "EXPOSE 5151" >> tempdir/DockerFile
#10 crear la imagen  build
cd tempdir
docker build -t passevolapp

#11  crear el contenedor donde  expongo un puerto y el volumen
docker run -it -d --rm -p 5151:5000 -v "$PWD/db":/datos --name passevolapprunning passevolapp
#listar los contenedores
docker ps -a