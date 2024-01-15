from flask import Flask, request
from flask_restful import Api, Resource
import pandas as pd

app = Flask(__name__)
api = Api(app)

class Users(Resource):
    def get(self):
        data = pd.read_csv('kullanici.csv')
        data = data.to_dict('records')
        return {'data': data}, 200

    def post(self):
        name = request.args['name']
        age = request.args['age']
        city = request.args['city']
        # Yeni değişkenler eklendi
        country = request.args['country']
        email = request.args['email']
        req_data = pd.DataFrame({
            'name': [name],
            'age': [age],
            'city': [city],
            # Yeni değişkenler eklendi
            'country': [country],
            'email': [email]
        })
        data = pd.read_csv('kullanici.csv')
        data = data.append(req_data, ignore_index=True)
        data.to_csv('kullanici.csv', index=False)
        return {'message': 'Kayıt başarıyla eklendi.'}, 200

    def delete(self):
        name = request.args['name']
        data = pd.read_csv('kullanici.csv')

        if name in data['name'].values:
            data = data[data['name'] != name]
            data.to_csv('kullanici.csv', index=False)
            return {'message': 'Kayıt başarıyla silindi.'}, 200
        else:
            return {'message': 'Kayıt bulunamadı.'}, 404

class Cities(Resource):
    def get(self):
        data = pd.read_csv('kullanici.csv', usecols=[2])
        data = data.to_dict('records')
        return {'data': data}, 200

class Name(Resource):
    def get(self, name):
        data = pd.read_csv('kullanici.csv')
        data = data.to_dict('records')
        for entry in data:
            if entry['name'] == name:
                return {'data': entry}, 200
        return {'message': 'Bu isimle kayıt bulunamadı!'}, 401
# add email variables, check method
class Email(Resource):
    def get(self, email):
        data = pd.read_csv('kullanici.csv')
        data = data.to_dict('records')
        for entry in data:
            if entry['email'] == email:
                return {'data': entry}, 200
        return {'message': 'Bu isimle kayıt bulunamadı!'}, 401

# add country variables
class Country(Resource):
    def get(self):
        data = pd.read_csv('kullanici.csv', usecols=[3])
        data = data.to_dict('records')
        return {'data': data}, 200

# Add URL endpoints
api.add_resource(Users, '/users')
api.add_resource(Cities, '/cities')
api.add_resource(Name, '/isim/<string:name>')

# add new endpoints
api.add_resource(Country, '/country')
api.add_resource(Email, '/email/<string:email>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6767)
    app.run()