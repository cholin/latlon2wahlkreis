import json
from flask import Flask
from flask_restful import Resource, Api
from shapely.geometry import shape, Point

app = Flask(__name__)
api = Api(app)

# load data
data = []
with open('wahlkreise.geojson', 'r') as f:
    geojson = json.load(f)
    if 'features' in geojson:
        data = [(f, shape(f['geometry'])) for f in geojson['features']]

class Wahlkreis(Resource):
    def get(self, lat, lon):
        point = Point(float(lon), float(lat))
        hits = filter(lambda x: x[1].contains(point), data)
        for f,s in hits:
            return {
                'number': f['properties']['WKR_NR'],
                'name:': f['properties']['WKR_NAME']
            }

api.add_resource(Wahlkreis, '/<float:lat>/<float:lon>')

if __name__ == '__main__':
    app.run(debug=True)
