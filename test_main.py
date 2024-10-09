import unittest
import json
from main import app, db, Avestruz

class AvestruzAPITestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db.create_all()  # Crear la base de datos para las pruebas
            self.populate_data()

    def populate_data(self):
        avestruz1 = Avestruz(nombre='Avestruz Común', edad=5, peso=90)
        avestruz2 = Avestruz(nombre='Avestruz del Sur', edad=3, peso=80)
        db.session.add(avestruz1)
        db.session.add(avestruz2)
        db.session.commit()

    # Pruebas unitarias
    def test_get_avestruces(self):
        response = self.app.get('/api/avestruces')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data), list)

    def test_get_avestruz(self):
        response = self.app.get('/api/avestruces/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('nombre', json.loads(response.data))

    # Prueba de integración
    def test_integration_create_and_get_avestruz(self):
        response = self.app.post('/api/avestruces', 
                                 data=json.dumps({'nombre': 'Avestruz Africano', 'edad': 4, 'peso': 85}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        avestruz_id = json.loads(response.data)['id']
        response = self.app.get(f'/api/avestruces/{avestruz_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['nombre'], 'Avestruz Africano')

    # Prueba funcional
    def test_functional_get_all_avestruces(self):
        response = self.app.get('/api/avestruces')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.data)), 2)  # Debería haber 2 avestruces

    # Prueba de seguridad
    def test_security_invalid_data(self):
        response = self.app.post('/api/avestruces', 
                                 data=json.dumps({'nombre': '', 'edad': -1, 'peso': -10}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    # Prueba de rendimiento
    def test_performance_get_avestruces(self):
        import time
        start_time = time.time()
        response = self.app.get('/api/avestruces')
        end_time = time.time()
        self.assertEqual(response.status_code, 200)
        self.assertLess(end_time - start_time, 1)  # Debería ser menos de 1 segundo

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()  # Eliminar la base de datos después de las pruebas

if __name__ == '__main__':
    unittest.main()
