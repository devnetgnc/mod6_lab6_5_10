# You can add to this file in the editor 
from sqlite3.dbapi2 import IntegrityError
import pyotp
import sqlite3
import hashlib
from flask import Flask, request
import uuid

app = Flask(__name__)
# creamos la base de datos
db_name = '/datos/test.db'

@app.route("/")
def index():
    return 'Bienvenidos  al lab preactico para  una evolución de los sistemas de contraseña!\n'


# Metod registrar usuario
@app.route('/signup/v1', methods=['POST'])
def signup():
    #conexion a la base de datos 
    conn = sqlite3.connect(db_name)
    #creo un cursor
    c = conn.cursor()
    #Creo la tabla si no existe -  primera ejecución
    c.execute('''
    CREATE TABLE IF NOT EXISTS USER_PLAIN
    (USER_NAME TEXT PRIMARY KEY  NOT NULL,
     PASSWORD TEXT NOT NULL);
    ''')

    #confirmo creación
    conn.commit()
    try:
      #Registro el usuario          
      c.execute('''
        INSERT INTO USER_PLAIN (USER_NAME, PASSWORD)
        VALUES ('{0}','{1}')
        '''.format(request.form['username'],request.form['password'])
      )
      #Confirmo insert de registro de usuario
      conn.commit()  
    #Atrapo excepcion en caso de  datos duplicado (username)
    except sqlite3.IntegrityError:
            return 'El username ya ha sido registrado\n'  
    #imprimo  datos registrado        
    print('username:',request.form['username'], 'password:',request.form['password'])
    # devuelvo success 
    return 'signup success\n'      

#Validar login por password
def  verify_plain(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    query = "SELECT PASSWORD FROM  USER_PLAIN WHERE USER_NAME= '{0}'".format(username)
    c.execute(query)
    records = c.fetchone()
    if not records :
        return False
    return records[0] == password

@app.route('/login/v1', methods=['GET', 'POST'])
def login_v1():
    error= None
    if request.method == 'POST':
        if verify_plain(request.form['username'],request.form['password']):
            error = 'Login success \n'
        else:
            error = 'Invalid username/password \n'
    else:
        error = 'Invalid Method \n'            
    return error


@app.route('/signup/v2',methods=['POST'])
def signup_v2():
    conn = sqlite3.connect(db_name)
    c= conn.cursor()
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS USER_HASH
        (USER_NAME TEXT PRIMARY KEY NOT NULL,
        HASH TEXT NOT NULL);
        ''')
    conn.commit()

    try:
        hash_value = hashlib.sha256(request.form['password'].encode()).hexdigest()
        c.execute(
            '''
            INSERT INTO USER_HASH (USER_NAME, HASH)
            VALUES ('{0}','{1}')
            '''.format(request.form['username'],hash_value))
        conn.commit()
    except sqlite3.IntegrityError:
        return 'El username ya ha sido registrado\n'
    print('username',request.form['username'],'password:',request.form['password'])
    return 'signup success\n'

def verify_hash(username, password):
    conn=sqlite3.connect(db_name)
    c= conn.cursor()
    query="SELECT HASH FROM USER_HASH WHERE USER_NAME= '{0}'".format(username) 
    c.execute(query)
    records = c.fetchone()
    conn.close()
    if not records:
        False
    return records[0] == hashlib.sha256(password.encode()).hexdigest() 


@app.route('/login/v2',methods=['GET','POST'])
def login_v2():
    error=None
    if request.method == 'POST':
        if verify_hash(request.form['username'],request.form['password']):
            error='Login success\n'
        else:
            error='Invalid username/password\n'
    else:
        error= 'Invalid method\n'

    return error

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context ='adhoc')