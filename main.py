from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///avestruces.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de Avestruz
class Avestruz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'nombre': self.nombre, 'edad': self.edad, 'peso': self.peso}

# Crear la base de datos
with app.app_context():
    db.create_all()

# Rutas CRUD
@app.route('/api/avestruces', methods=['GET'])
def get_avestruces():
    avestruces = Avestruz.query.all()
    return jsonify([avestruz.to_dict() for avestruz in avestruces])

@app.route('/api/avestruces/<int:avestruz_id>', methods=['GET'])
def get_avestruz(avestruz_id):
    avestruz = Avestruz.query.get(avestruz_id)
    if avestruz:
        return jsonify(avestruz.to_dict())
    return jsonify({'error': 'Avestruz no encontrado'}), 404

@app.route('/api/avestruces', methods=['POST'])
def create_avestruz():
    data = request.get_json()
    
    # Valiadcion
    if not data or not isinstance(data.get('nombre'), str) or not data.get('nombre') \
            or not isinstance(data.get('edad'), int) or data['edad'] <= 0 \
            or not isinstance(data.get('peso'), (int, float)) or data['peso'] <= 0:
        return jsonify({'error': 'Datos inválidos'}), 400
    
    nuevo_avestruz = Avestruz(nombre=data['nombre'], edad=data['edad'], peso=data['peso'])
    db.session.add(nuevo_avestruz)
    db.session.commit()
    return jsonify(nuevo_avestruz.to_dict()), 201


@app.route('/api/avestruces/<int:avestruz_id>', methods=['DELETE'])
def delete_avestruz(avestruz_id):
    avestruz = Avestruz.query.get(avestruz_id)
    if avestruz:
        db.session.delete(avestruz)
        db.session.commit()
        return jsonify({'mensaje': 'Avestruz eliminado'}), 204
    return jsonify({'error': 'Avestruz no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
