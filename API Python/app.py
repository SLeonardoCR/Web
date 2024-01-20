from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import time
from flask_cors import CORS
from flask import Flask, jsonify, request
import csv
import os

app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/apphorarios'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Profesor(db.Model):
    __tablename__ = 'profesores'
    NoEmpleado = db.Column(db.Integer, primary_key=True)
    Nombres = db.Column(db.String(255))
    ApellidoPaterno = db.Column(db.String(15))
    ApellidoMaterno = db.Column(db.String(15))
    FechaNacimiento = db.Column(db.String(10))
    RFC = db.Column(db.String(10))


class MateriaDisponible(db.Model):
    __tablename__ = 'materias_disponibles'
    id = db.Column(db.Integer, primary_key=True)
    ClaveMateria = db.Column(db.String(7))
    HoraInicio = db.Column(db.Time)
    HoraFin = db.Column(db.Time)
    Disponibilidad = db.Column(db.Boolean)
    ProfesorAsignado = db.Column(db.Integer, db.ForeignKey('profesores.NoEmpleado'))

    profesor = db.relationship('Profesor', backref=db.backref('materias_asignadas', cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'id': self.id,
            'ClaveMateria': self.ClaveMateria,
            'ProfesorAsignado': self.ProfesorAsignado,
            'ProfesorNombres': self.profesor.Nombres,
            'ProfesorApellidoPaterno': self.profesor.ApellidoPaterno,
            'ProfesorApellidoMaterno': self.profesor.ApellidoMaterno
        }


class ProfesorMateria(db.Model):
    __tablename__ = 'profesor_materia'
    NoEmpleado = db.Column(db.Integer, db.ForeignKey('profesores.NoEmpleado'), primary_key=True)
    ClaveMateria = db.Column(db.String(7), db.ForeignKey('materias.ClaveMateria'), primary_key=True)

    profesor = db.relationship('Profesor', backref=db.backref('materias_dadas', cascade='all, delete-orphan'))


class Materia(db.Model):
    __tablename__ = 'materias'
    ClaveMateria = db.Column(db.String(7), primary_key=True)
    NombreMateria = db.Column(db.String(45))
    Carrera = db.Column(db.String(255))
    Reticula = db.Column(db.String(255))


class HorarioProfesor(db.Model):
    __tablename__ = 'horario_profesor'
    id = db.Column(db.Integer, primary_key=True)
    NoEmpleado = db.Column(db.Integer, db.ForeignKey('profesores.NoEmpleado'))
    HoraInicio = db.Column(db.Time)
    HoraFin = db.Column(db.Time)


import os
import csv

@app.route('/horarios', methods=['GET'])
def obtener_horarios():
    # Ruta del directorio del proyecto Angular
    angular_directory = os.path.join('D:', 'USER', 'Programming', 'Web', 'AppHorarios')

    csv_filename = 'horarios.csv'

    # Ruta completa del archivo CSV
    csv_path = os.path.join(angular_directory, 'src', 'assets', csv_filename)

    print(csv_path)

    # Obtener las materias disponibles sin profesor asignado
    materias_disponibles = MateriaDisponible.query.filter_by(Disponibilidad=0).all()

    # Obtener los nombres de las columnas
    columnas = set()
    for materia_disponible in materias_disponibles:
        columnas.add(materia_disponible.HoraInicio.strftime('%H:%M'))
        columnas.add(materia_disponible.HoraFin.strftime('%H:%M'))

    # Obtener los nombres de las filas y construir la tabla
    tabla = {}
    for materia_disponible in materias_disponibles:
        clave_materia = materia_disponible.ClaveMateria
        if clave_materia not in tabla:
            materia = Materia.query.get(clave_materia)
            tabla[clave_materia] = {
                'Materia': materia.NombreMateria,
                'Profesores': {}
            }
        profesor = Profesor.query.get(materia_disponible.ProfesorAsignado)
        nombre_profesor = f'{profesor.Nombres} {profesor.ApellidoPaterno} {profesor.NoEmpleado}'
        tabla[clave_materia]['Profesores'][nombre_profesor] = True

    # Crear el archivo CSV
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Escribir los nombres de las columnas
        writer.writerow(['Materia'] + sorted(columnas))
        # Escribir las filas
        for clave_materia, fila in tabla.items():
            profesores = fila['Profesores']
            # Crear una lista con los valores de las celdas para la fila actual
            valores_fila = [fila['Materia']]
            for columna in sorted(columnas):
                if columna in profesores:
                    valores_fila.append('X')
                else:
                    valores_fila.append('')
            # Escribir la fila en el archivo CSV
            writer.writerow(valores_fila)

    return jsonify({'message': 'Archivo CSV creado correctamente'})


@app.route('/profesores', methods=['POST'])
def crear_profesor():
    data = request.json
    nuevo_profesor = Profesor(
        NoEmpleado=data['NoEmpleado'],
        Nombres=data['Nombres'],
        ApellidoPaterno=data['ApellidoPaterno'],
        ApellidoMaterno=data['ApellidoMaterno'],
        FechaNacimiento=data['FechaNacimiento'],
        RFC=data['RFC']
    )
    db.session.add(nuevo_profesor)
    db.session.commit()
    return jsonify({'message': 'Profesor creado exitosamente'})

@app.route('/profesores', methods=['GET'])
def obtener_profesores():
    profesores = Profesor.query.all()
    resultado = []
    for profesor in profesores:
        resultado.append({
            'NoEmpleado': profesor.NoEmpleado,
            'Nombres': profesor.Nombres,
            'ApellidoPaterno': profesor.ApellidoPaterno,
            'ApellidoMaterno': profesor.ApellidoMaterno,
            'FechaNacimiento': profesor.FechaNacimiento,
            'RFC': profesor.RFC
        })
    return jsonify(resultado)

@app.route('/profesores/<int:no_empleado>', methods=['GET'])
def obtener_profesor(no_empleado):
    profesor = Profesor.query.get(no_empleado)
    if profesor:
        return jsonify({
            'NoEmpleado': profesor.NoEmpleado,
            'Nombres': profesor.Nombres,
            'ApellidoPaterno': profesor.ApellidoPaterno,
            'ApellidoMaterno': profesor.ApellidoMaterno,
            'FechaNacimiento': profesor.FechaNacimiento,
            'RFC': profesor.RFC
        })
    return jsonify({'message': 'Profesor no encontrado'})

@app.route('/profesores/<int:no_empleado>', methods=['PUT'])
def actualizar_profesor(no_empleado):
    profesor = Profesor.query.get(no_empleado)
    if profesor:
        data = request.json
        profesor.Nombres = data['Nombres']
        profesor.ApellidoPaterno = data['ApellidoPaterno']
        profesor.ApellidoMaterno = data['ApellidoMaterno']
        profesor.FechaNacimiento = data['FechaNacimiento']
        profesor.RFC = data['RFC']
        db.session.commit()
        return jsonify({'message': 'Profesor actualizado exitosamente'})
    return jsonify({'message': 'Profesor no encontrado'})

@app.route('/profesores/<int:no_empleado>', methods=['DELETE'])
def eliminar_profesor(no_empleado):
    profesor = Profesor.query.get(no_empleado)
    if profesor:
        db.session.delete(profesor)
        db.session.commit()
        return jsonify({'message': 'Profesor eliminado exitosamente'})
    return jsonify({'message': 'Profesor no encontrado'})


@app.route('/materias', methods=['POST'])
def crear_materia():
    data = request.json
    nueva_materia = Materia(
        ClaveMateria=data['ClaveMateria'],
        NombreMateria=data['NombreMateria'],
        Carrera=data['Carrera'],
        Retícula=data['Reticula']
    )
    db.session.add(nueva_materia)
    db.session.commit()
    return jsonify({'message': 'Materia creada exitosamente'})

@app.route('/materias', methods=['GET'])
def obtener_materias():
    materias = Materia.query.all()
    resultado = []
    for materia in materias:
        resultado.append({
            'ClaveMateria': materia.ClaveMateria,
            'NombreMateria': materia.NombreMateria,
            'Carrera': materia.Carrera,
            'Reticula': materia.Reticula
        })
    return jsonify(resultado)

@app.route('/materias/<string:clave_materia>', methods=['GET'])
def obtener_materia(clave_materia):
    materia = Materia.query.get(clave_materia)
    if materia:
        return jsonify({
            'ClaveMateria': materia.ClaveMateria,
            'NombreMateria': materia.NombreMateria,
            'Carrera': materia.Carrera,
            'Reticula': materia.Reticula
        })
    return jsonify({'message': 'Materia no encontrada'})

@app.route('/materias/<string:clave_materia>', methods=['PUT'])
def actualizar_materia(clave_materia):
    materia = Materia.query.get(clave_materia)
    if materia:
        data = request.json
        materia.NombreMateria = data['NombreMateria']
        materia.Carrera = data['Carrera']
        materia.Reticula = data['Reticula']
        db.session.commit()
        return jsonify({'message': 'Materia actualizada exitosamente'})
    return jsonify({'message': 'Materia no encontrada'})

@app.route('/materias/<string:clave_materia>', methods=['DELETE'])
def eliminar_materia(clave_materia):
    materia = Materia.query.get(clave_materia)
    if materia:
        db.session.delete(materia)
        db.session.commit()
        return jsonify({'message': 'Materia eliminada exitosamente'})
    return jsonify({'message': 'Materia no encontrada'})


if __name__ == "__main__":
    app.run(debug=True, port=8080)
