
from passlib.hash import sha256_crypt
from flask import Flask, render_template, request, redirect, session, url_for

from funciones import graba_diccionario, graba_diccionario_trabajador ,lee_diccionario_csv,graba_diccionario_id, lee_diccionario_csv_id, lee_diccionario_csv_nombre_mascota, sacar_usuarios,lee_diccionario_csv_trabajadores, lee_diccionario_csv_admin,graba_diccionario_admin
import datetime
#from flask_weasyprint import render_pdf


## 7 de Mayo del 2022
# DESARROLLO DE SISTEMAS IV
#-------------------------
#GRUPO 1
#VAZQUEZ GERMAN JUAN LUIS EXPEDIENTE:220222308 
#-------------------------
#GRUPO 2 
#ANTELO FIGUEROA ANDRES EXPEDIENTE: 220218013   
#QUIRARTE AGÜERO ALEJANDRA EXPEDIENTE:220210793 
#
#
#


diccionario_mascotas={}
archivo_usuarios = 'usuarios.csv'
archivo_animales = 'animales.csv'
archivo_citas = 'citas.csv'
archivo_citas_completas = 'citas_completas.csv'
archivo_trabajadores = 'trabajadores.csv'
archivo_recetas = "recetas.csv"
archivo_admin = "admin.csv"
dicc_admin = lee_diccionario_csv_admin(archivo_admin)
diccionario_usuarios = lee_diccionario_csv(archivo_usuarios)
diccionario_mascotas = lee_diccionario_csv_nombre_mascota(archivo_animales)
diccionario_citas = lee_diccionario_csv_id(archivo_citas)
diccionario_trabajadores = lee_diccionario_csv(archivo_trabajadores)
lista_usuarios = sacar_usuarios(diccionario_usuarios)
diccionario_citas_completas = lee_diccionario_csv_id(archivo_citas_completas)
diccionario_recetas = lee_diccionario_csv_id(archivo_recetas)



logeado = False
first_login = False
first_register_animal = False 
deslog = False
confirmacion = False
id = 0
lista_atencion = ['Ducharlo','Cortarle el pelo','Desparasitarlo','Vacunarlo','Cita con el medico']

app = Flask(__name__)
app.secret_key = "klNmsS679SDqWpñl"

@app.route("/")
def index():
    
    if logeado == True:
        user = session['usuario']
        if user in diccionario_usuarios:
            return render_template("index.html")
        else:
            if user in diccionario_trabajadores:
                return render_template("index_trabajador.html")
    else:
        try:
            user = session['usuario']
            if user in diccionario_usuarios:
                return render_template("index.html")
            else:
                if user in diccionario_trabajadores:
                     return render_template("index_trabajador.html")
        except:
            return render_template("index.html")
        return render_template("index_admin.html")


@app.route("/login/", methods=['GET','POST'])
def ingresar():
    logeado = False
    if "logged_in" in session:
        if session["logged_in"] == True:
            logeado = True

    if logeado == False:        
        if request.method == 'GET':
            msg = ''
            return render_template('login.html',mensaje=msg)
        else:
            if request.method == 'POST':
                usuario = request.form['usuario']

                if usuario in diccionario_usuarios:
                    password_db = diccionario_usuarios[usuario]['password'] # password guardado
                    password_forma = request.form['password'] #password presentado
                    verificado = sha256_crypt.verify(password_forma,password_db)
                    if (verificado == True):
                        session['usuario'] = usuario
                        session['logged_in'] = True
                        first_login = True
                        logeado = True
                        return render_template("index.html", first = first_login)
                    else:
                        msg = f'El password de {usuario} no corresponde'
                        return render_template('login.html',mensaje=msg)
                else:
                    if usuario in diccionario_trabajadores:
                           password_db = diccionario_trabajadores[usuario]['password'] # password guardado
                           password_forma = request.form['password'] #password presentado
                           verificado = sha256_crypt.verify(password_forma,password_db)
                           if (verificado == True):
                                session['usuario'] = usuario
                                session['logged_in'] = True
                                first_login = True
                                logeado = True
                                return render_template("index_trabajador.html", first = first_login)
                           else:
                                 msg = f'El password de {usuario} no corresponde'
                                 return render_template('login.html',mensaje=msg)
            
                    else:
                        if usuario in dicc_admin:
                           password_db = dicc_admin[usuario]['password'] # password guardado
                           password_forma = request.form['password'] #password presentado
                           verificado = sha256_crypt.verify(password_forma,password_db)
                           if (verificado == True):
                                session['usuario'] = usuario
                                session['logged_in'] = True
                                first_login = True
                                logeado = True
                                return render_template("index_admin.html", first = first_login)
                           else:
                                 msg = f'El password de {usuario} no corresponde'
                                 return render_template('login.html',mensaje=msg)

                        
                        else:
                            msg = f'usuario {usuario} no existe'
                            return render_template('login.html',mensaje=msg)
    else:
        msg = 'YA ESTA LOGEADO'
        return render_template('index.html')
   
    

@app.route('/logout', methods=['GET'])
@app.route('/logout/', methods=['GET'])
def logout():
    if request.method == 'GET':
        session.clear()
        session["logged_in"] = False
        deslog = True
        logeado = False
        return render_template("index.html", deslogeado = deslog)



@app.route("/register/", methods=['POST','GET'])
def registrarse():
    if request.method == 'POST':
                valor = request.form['enviar']
                if valor == 'Entrar':
                    nombre  =  request.form['ncompleto']
                    correo    =  request.form['correo']
                    usuario =  request.form['usuario']
                    password = request.form['password']
                    password = sha256_crypt.hash(password)
                    tipo = "usuario"
                    
                    if usuario not in diccionario_usuarios and usuario not in diccionario_trabajadores:
                        diccionario_usuarios[usuario] = {
                            'nombre': nombre,
                            'correo'  : correo,
                            'usuario' : usuario,
                            'password' : password,
                            'tipo' : tipo
                        }
                    lista_usuarios = usuario
                    graba_diccionario(diccionario_usuarios,'usuario',archivo_usuarios)
                #return render_template('lista_usuarios.html',dicc_usuarios=diccionario_usuarios)
                return redirect('/')
    else:
     return render_template("register.html")


@app.route("/register_trabajadores/", methods=['POST','GET'])
def registrar_trabajadores():
    if request.method == 'POST':
                valor = request.form['enviar']
                if valor == 'Entrar':
                    nombre  =  request.form['ncompleto']
                    correo    =  request.form['correo']
                    usuario =  request.form['usuario']
                    password = request.form['password']
                    password = sha256_crypt.hash(password)
                    tipo = "trabajador"
                    
                    if usuario not in diccionario_usuarios and usuario not in diccionario_trabajadores:
                        diccionario_trabajadores[usuario] = {
                            'nombre': nombre,
                            'correo'  : correo,
                            'usuario' : usuario,
                            'password' : password,
                            'tipo' : tipo
                        }
                    
                    graba_diccionario(diccionario_trabajadores,'usuario',archivo_trabajadores)
                #return render_template('lista_usuarios.html',dicc_usuarios=diccionario_usuarios)
                return redirect('/')
    else:
     return render_template("register_trabajadores.html")


#@app.route("/admin/", methods=['POST','GET'])
#def admin():
#    if request.method == 'POST':
 #               valor = request.form['enviar']
  #              if valor == 'Entrar':
   #                 admin  =  request.form['ncompleto']
    #                correo    =  request.form['correo']
     #               nombre =  request.form['usuario']
      #              password = request.form['password']
       #             password = sha256_crypt.hash(password)
        #            tipo = "admin"
                    
             #       if admin not in diccionario_usuarios and admin not in diccionario_trabajadores:
              #          dicc_admin[admin] = {
              #              'admin': admin,
              #              'correo'  : correo,
              #              'nombre' : nombre,
          #                  'password' : password,
               #             'tipo' : tipo
          #              }
                    
         #           graba_diccionario_admin(dicc_admin,'admin',archivo_admin)
       #         #return render_template('lista_usuarios.html',dicc_usuarios=diccionario_usuarios)
     #           return redirect('/')
  #  else:
  #   return render_template("register.html")

@app.route("/animales/", methods=['POST','GET'])
def registrar_animal():
    if request.method == 'POST':
               
                valor = request.form['enviar']
                if valor == 'Registrar':
                    usuario =  session['usuario']
                    nombre  =  request.form['nombre_mascota']
                    animal    =  request.form['animales']
                    diccionario_mascotas[nombre] = {
                            'nombre_mascota': nombre,
                            'usuario':usuario,
                            'animal':animal     
                        }
                graba_diccionario(diccionario_mascotas,'nombre_mascota',archivo_animales)
                #return render_template('lista_usuarios.html',dicc_usuarios=diccionario_usuarios)
                first_register_animal = True
                dic_animales2 = lee_diccionario_csv(archivo_animales)
                
                return render_template('index.html',first_animal = first_register_animal, dicc_animales=dic_animales2)
    
    else:
     return render_template("register_animales.html")


@app.route("/lista_mascotas/", methods=['GET'])
def dar_lista():
     if request.method == 'GET':
        dic_animales2 = lee_diccionario_csv_nombre_mascota(archivo_animales)
        return render_template("lista_mascotas.html",dicc_animales=dic_animales2)

@app.route("/lista_usuarios/", methods=['GET'])
def lista_users():
     if request.method == 'GET':
        dic_users = lee_diccionario_csv(archivo_usuarios)
        return render_template("lista_usuarios.html",dicc_usuario=dic_users)

@app.route("/lista_trabajadores/", methods=['GET'])
def lista_trabajadores():
     if request.method == 'GET':
        dic_trabajadores = lee_diccionario_csv(archivo_trabajadores)
        return render_template("lista_trabajadores.html",dicc_trabajadores=dic_trabajadores)

@app.route("/citas/", methods=['GET','POST'])
def citas():
     if request.method == 'GET':
        print(diccionario_mascotas)
        hoy_completo = datetime.datetime.today()
        fecha_hoy  = datetime.datetime.strftime(hoy_completo,"%Y-%m-%d")
        return render_template("calendario.html",dicc_animales=diccionario_mascotas, lista=lista_atencion, hoy=fecha_hoy)
     else:
        if request.method == 'POST':
            
            valor = request.form['enviar']
            if valor == 'Entrar':
                mascota =  request.form['mascota']
                atencion  =  request.form['accion']
                fecha    =  request.form['fecha']
                usuario =  session['usuario']
                diccionario_citas = lee_diccionario_csv_id(archivo_citas)
                id = len(diccionario_citas)
                if id not in diccionario_citas:
                        diccionario_citas[id] = {
                            'id': id,
                            'mascota': mascota,
                            'atencion'  : atencion,
                            'fecha': fecha,
                            'usuario':usuario
                        }
                id = id+1
                graba_diccionario_id(diccionario_citas,'id',archivo_citas)
                dic_animales2 = lee_diccionario_csv_nombre_mascota(archivo_animales)
                confirmacion = True
            return render_template("index.html",dicc_animales=dic_animales2, confi = confirmacion)

@app.route("/lista_citas/", methods=['GET'])
def lista_citas():
    if request.method == 'GET':
        dic_citas = lee_diccionario_csv_id(archivo_citas)
        return render_template("lista_citas_users.html",dicc_citas=dic_citas)


@app.route("/lista_recetas_usuario/", methods=['GET'])
def lista_receta_usuario():
    if request.method == 'GET':
        dic_citas = lee_diccionario_csv_id('receta_completa.csv')
        return render_template("lista_recetas.html",dicc_citas=dic_citas)


@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")       

@app.route("/receta/", methods=['GET','POST'])
def receta():
    dic_completa=lee_diccionario_csv_id('receta_completa.csv')
    if request.method == 'GET':
        dic_receta = lee_diccionario_csv_id(archivo_recetas)
        
        return render_template("receta.html",dic_receta=dic_receta)
    else:
        if request.method == 'POST':
            dic_receta = lee_diccionario_csv_id(archivo_recetas)
            ids = str(len(dic_completa)+1)
            
            print(dic_receta)
            print(ids)
            dic_receta_new = dic_receta[ids]
            valor = request.form['enviar']
            if valor == 'Entrar':
                
                datos = request.form['detalles']
                print(ids)
                if ids not in dic_completa:
                        dic_completa[ids] = {
                            'id': ids,
                            'mascota': dic_receta_new['mascota'],
                            'atencion'  : dic_receta_new['atencion'],
                            'datos': datos,
                            'usuario':dic_receta_new['usuario']
                        }
                        graba_diccionario_id(dic_completa,'id','receta_completa.csv')
                        dic_receta.pop(ids)
                        print(dic_receta)
                        
                        if len(dic_receta) == 0:
                                dic_receta[0] = {
                                'id': 0,
                                'mascota': '',
                                'atencion'  : '',
                                'datos': '',
                                'usuario':''
                                }
                        graba_diccionario_id(dic_receta,'id',archivo_recetas)
                        return render_template("index_trabajador.html")
                else:
                    return render_template("index.html",dicc_citas=dic_receta)
                        

                  
                  


@app.route("/Citas_por_cumplir/", methods=['GET','POST'])
def lista_citas_pendientes():
    dic_citas = lee_diccionario_csv_id(archivo_citas)
    if request.method == 'GET':  
        return render_template("lista_citas.html",dicc_citas=dic_citas)
    else:
       if request.method == 'POST':
            valor = request.form['enviar']
            if valor == 'Entrar':
                verificado = request.form['cita']
                if verificado == "cita":
                    id = request.form['id']
                    dicc_copia = dic_citas[id]
                    diccionario_citas_completas[id]=dicc_copia
                    
                    ## borrar cita
                    dic_citas.pop(id)
                    if len(dic_citas) == 0:
                        diccionario_citas[0] = {
                            'id': 0,
                            'mascota': '',
                            'atencion'  : '',
                            'fecha': '',
                            'usuario':''
                        }
                        graba_diccionario_id(diccionario_citas,'id',archivo_citas)
                    else:
                        graba_diccionario_id(dic_citas,'id',archivo_citas) 

                    graba_diccionario_id(diccionario_citas_completas,'id',archivo_recetas)
                
                    

                return redirect("/receta/")


#@app.route("/pdf/", methods=['GET'])
#def pedefe():
 
#    return render_pdf(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)
    session['logged_in'] = False