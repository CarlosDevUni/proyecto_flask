from flask import Flask, jsonify, request
from api.db.test_db import persons_db

app = Flask(__name__)

@app.route('/test')
def test():
    return jsonify({"mesagge" : "test ok"})

@app.route('/persons', methods = ['GET'])
def get_all_persons():
    # consulta a la BD SELECT * FROM persons
    return jsonify( { "persons" : persons_db})

@app.route('/persons/<int:id>', methods = ['GET'])
def get_person_by_id(id):
    # consulta a la BD SELECT * FROM persons WHERE id = id
    person = [person for person in persons_db if person["id"]== id]
    return jsonify( {"person" : person[0]})
    # 
    #lista = []
    #for person in persons_db:
    #    if person["id"] == id:
    #        lista.append(person)

@app.route('/persons', methods = ['POST'])
def create_person():
    # simula INSERT INTO persons VALUES(name, surname, email, dni)
    # Control de datos recibidos
    name = request.get_json()["name"]
    surname = request.get_json()["surname"]
    email = request.get_json()["email"]
    dni = request.get_json()["dni"]

    # Control: no se permite dni repetido
    existe = False
    for person in persons_db:
        if person["dni"] == dni:
            existe = True
    
    if not existe:
        # simulamos id autoincremental en BD
        max_id = 0
        for person in persons_db:
            if person["id"] > max_id:
                max_id = person["id"]

        new_person = {
            'dni' : dni,
            'name' : name,
            'surname' : surname,
            'email' : email,
            'id' : max_id + 1
        }    

        persons_db.append(new_person)

        return jsonify({ "person" : new_person}), 201
    
    else:
        return jsonify( {"message" : "Error: ya existe una persona con ese dni"}), 400
    
@app.route('/persons/<int:id>', methods = ['PUT'])
def update_person(id):
    # simula UPDATE ... SET ... WHERE
    # Control de datos recibidos (se debería verificar que existan todas las claves, que sean del tipo correcto, etc)
    name = request.get_json()["name"]
    surname = request.get_json()["surname"]
    email = request.get_json()["email"]
    dni = request.get_json()["dni"]

    # Ubicar el recurso con el id correspondiente
    index_person = [index for index in range(len(persons_db)) if persons_db[index]["id"]== id]

    # Controlar si existe
    if len(index_person) > 0:
        index = index_person[0] 
        
        # Aquí se deberían implementar otros controles
        # Por ejemplo si existen columnas que restringen valor único
        # En este caso, no se podría actualizar cualquier valor en el dni
        # Correspondería controlar que el nuevo valor no pertenece a otro registro
        # (sin implementar acá)
        persons_db[index]["dni"] = dni
        persons_db[index]["name"] = name
        persons_db[index]["surname"] = surname
        persons_db[index]["email"] = email

        uptaded = persons_db[index]

        return jsonify({"person" : uptaded}), 200
    else:
        return jsonify( {"message" : "Error: no existe una persona con ese id"}), 400
    
@app.route('/persons/<int:id>', methods = ['DELETE'])
def delete_person(id):
    # simula DELETE ... FROM ... WHERE
    
    # Ubicar el recurso con el id correspondiente
    index_person = [index for index in range(len(persons_db)) if persons_db[index]["id"]== id]

    # Controlar si existe
    if len(index_person) > 0:
        index = index_person[0] 
        
        # La confirmación para eliminar se implementa en las interfaces de usuario
        # Una vez enviada la solicitud al servidor, la eliminación se efectúa directamente
        deleted = persons_db.pop(index)

        return jsonify({"person" : deleted}), 200
    else:
        return jsonify( {"message" : "Error: no existe una persona con ese id"}), 400    
