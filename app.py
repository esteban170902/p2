from flask import Flask, request, jsonify, abort
app = Flask(__name__)

# Lista de objetos
directories = []

# Función auxiliar para obtener un objeto por id
def get_object(id):
    for obj in directories:
        if obj["id"] == id:
            return obj
    return None

# Función auxiliar para validar un objeto
def validate_object(obj):
    if not isinstance(obj, dict):
        return False
    if not "name" in obj or not isinstance(obj["name"], str):
        return False
    if not "emails" in obj or not isinstance(obj["emails"], list):
        return False
    for email in obj["emails"]:
        if not isinstance(email, str):
            return False
    return True

# Ruta para obtener el estado del servicio
@app.route("/status/", methods=["GET"])
def status():
    return jsonify("pong")

# Ruta para obtener el listado de objetos
@app.route("/directories/", methods=["GET"])
def get_directories():
    # Obtener los parámetros de paginación (opcional)
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))
    # Calcular el índice inicial y final de la página
    start = (page - 1) * page_size
    end = start + page_size
    # Obtener la página correspondiente de la lista de objetos
    results = directories[start:end]
    # Construir la respuesta con el conteo, los links y los resultados
    response = {
        "count": len(directories),
        "next": f"/directories/?page={page + 1}&page_size={page_size}" if end < len(directories) else None,
        "previous": f"/directories/?page={page - 1}&page_size={page_size}" if start > 0 else None,
        "results": results
    }
    return jsonify(response)

# Ruta para crear un objeto
@app.route("/directories/", methods=["POST"])
def create_object():
    # Obtener los datos del request
    data = request.get_json()
    # Validar que los datos sean un objeto válido
    if not validate_object(data):
        abort(400) # Bad request
    # Asignar un id al objeto
    data["id"] = len(directories) + 1
    # Agregar el objeto a la lista de objetos
    directories.append(data)
    # Devolver el objeto creado con código 201 (Created)
    return jsonify(data), 201

# Ruta para obtener un objeto por id
@app.route("/directories/<int:id>/", methods=["GET"])
def get_object_by_id(id):
    # Obtener el objeto por id
    obj = get_object(id)
    # Si no existe, devolver código 404 (Not found)
    if not obj:
        abort(404)
    # Si existe, devolver el objeto con código 200 (OK)
    return jsonify(obj)

# Ruta para actualizar un objeto por id
@app.route("/directories/<int:id>/", methods=["PUT"])
def update_object_by_id(id):
    # Obtener el objeto por id
    obj = get_object(id)
    # Si no existe, devolver código 404 (Not found)
    if not obj:
        abort(404)
    # Obtener los datos del request
    data = request.get_json()
    # Validar que los datos sean un objeto válido
    if not validate_object(data):
        abort(400) # Bad request
    # Actualizar el objeto con los datos del request
    obj["name"] = data["name"]
    obj["emails"] = data["emails"]
    # Devolver el objeto actualizado con código 200 (OK)
    return jsonify(obj)

# Ruta para actualizar parcialmente un objeto por id
@app.route("/directories/<int:id>/", methods=["PATCH"])
def patch_object_by_id(id):
    # Obtener el objeto por id
    obj = get_object(id)
    # Si no existe, devolver código 404 (Not found)
    if not obj:
        abort(404)
    # Obtener los datos del request
    data = request.get_json()
    # Validar que los datos sean un diccionario
    if not isinstance(data, dict):
        abort(400) # Bad request
    # Actualizar solo los campos que estén en el request
    if "name" in data and isinstance(data["name"], str):
        obj["name"] = data["name"]
    if "emails" in data and isinstance(data["emails"], list):
        for email in data["emails"]:
            if not isinstance(email, str):
                abort(400) # Bad request
        obj["emails"] = data["emails"]
    # Devolver el objeto actualizado con código 200 (OK)
    return jsonify(obj)

# Ruta para eliminar un objeto por id
@app.route("/directories/<int:id>/", methods=["DELETE"])
def delete_object_by_id(id):
    # Obtener el objeto por id
    obj = get_object(id)
    # Si no existe, devolver código 404 (Not found)
    if not obj:
        abort(404)
    # Eliminar el objeto de la lista de objetos
    directories.remove(obj)
    # Devolver código 204 (No content)
    return "", 204
