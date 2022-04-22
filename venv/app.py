from flask import Flask, jsonify, request
from flask_cors import CORS
import MySQLdb
import datetime

app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


# METODO POST - INSERTAMOS NOTA


@app.route('/api/newTask', methods=['POST'])
def NewNote():
    db = MySQLdb.connect('eu-cdbr-west-02.cleardb.net', 'b3f860ff058543', 'ca5426e1', 'api')        
    data = (request.headers.get('user'),request.headers.get('title'),request.headers.get('description'))
    cursor = db.cursor()
    query = "insert into todo (user, title, description) values (%s, %s, %s)"
    try:
        cursor.execute(query, data)
        db.commit()
        db.close()
        return 'OK, Tarea insertada!'
    except Exception as e:
        return str(e)


# METODO GET - MUESTRA TODAS LAS NOTAS


@app.route('/api/tasks', methods=['GET'])
def GetNotes():
    db = MySQLdb.connect('eu-cdbr-west-02.cleardb.net', 'b3f860ff058543', 'ca5426e1', 'api')
    cursor = db.cursor()
    cursor.execute('select * from todo')
    result = jsonify(cursor.fetchall())
    db.close()
    return result


# METODO GET ID - MUESTRA ÚNICAMENTE NOTA POR ID 


@app.route('/api/getTask/<id>', methods=['GET'])
def GetNoteDescription(id):
    db = MySQLdb.connect('eu-cdbr-west-02.cleardb.net', 'b3f860ff058543', 'ca5426e1', 'api')
    cursor = db.cursor()
    cursor.execute('select * from todo where id = %s', id)
    result = jsonify(cursor.fetchall())
    db.close()
    return result


# METODO DELETE - ELIMINAMOS NOTA POR ID


@app.route('/api/deleteTask/<id>', methods=['DELETE'])
def DeleteNote(id):
    db = MySQLdb.connect('eu-cdbr-west-02.cleardb.net', 'b3f860ff058543', 'ca5426e1', 'api')        
    cursor = db.cursor()
    query = "delete from todo where id = %s"    
    try:
        cursor.execute(query, (id))
        db.commit()
        db.close()
        return 'OK, Registro eliminado!'
    except Exception as e:
        return str(e)


# METODO PUT - UPDATE DE REGISTO POR ID 


@app.route('/api/updateTask/<id>', methods=['PUT'])
def UpdateNote(id):
    db = MySQLdb.connect('eu-cdbr-west-02.cleardb.net', 'root', 'root', 'api')  
    #json = request.get_json()   
    data = (request.headers.get('user'),request.headers.get('title'),request.headers.get('description'))
    cursor = db.cursor()
    query = "update todo set user = %s, title = %s, description = %s where id = " + id    
    try:
        cursor.execute(query, (data))
        db.commit()
        db.close()
        return 'OK, Registro actualizado!'
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)