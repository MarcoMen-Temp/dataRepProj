from flask import Flask, jsonify, request, abort
from filmDAO import filmDAO

app = Flask(__name__, static_url_path='', static_folder='.')



# curl "http://127.0.0.1:5000/books"
@app.route('/films')
def getAll():
    results = filmDAO.getAll()

    return jsonify(results)


# curl "http://127.0.0.1:5000/books/2"
@app.route('/films/<int:id>')
def findById(id):
    foundFilms = filmDAO.findByID(id)

    return jsonify(foundFilms)

#  curl -i -H "Content-Type:application/json" -X POST -d  '{"Title":"Jackie Brown","Genre":"Action","Director":"Quentin Tarentino","Price":8}' http://localhost:5000/films

# curl -i -H "Content-Type:application/json" -X POST -d  '{"Title":"Pulp Fiction","Genre":"Action","Director":"Quentin Taraentino","Price":8 }'  http://localhost:5000/films

# curl  -i -H "Content-Type:application/json" -X POST -d "{\"Title\":\"hello\",\"Author\":\"someone\",\"Price\":123}" http://127.0.0.1:5000/books
@app.route('/films', methods=['POST'])
def create():

    if not request.json:
        abort(400)
    # other checking
    film = {

        "Title": request.json['Title'],
        "Genre": request.json['Genre'],
        "Director": request.json['Director'],
        "Price": request.json['Price'],
    }

    values = (film['Title'], film['Genre'], film['Director'], film['Price'])
    new_id = filmDAO.create(values)
    film['id'] = new_id
    return jsonify(film)


# curl -i -H "Content-Type:application/json" -X PUT -d "{"Title":"The Shayshank Redemption","Genre":"Drama","Director":"Frank Tarabont","Price":3}" http://localhost:5000/films/1

# curl  -i -H "Content-Type:application/json" -X PUT -d "{\"Title\":\"hello\",\"Author\":\"someone\",\"Price\":123}" http://127.0.0.1:5000/books/1
@app.route('/films/<int:id>', methods=['PUT'])
def update(id):

    foundFilm = filmDAO.findByID(id)
    if not foundFilm:
        abort(404)

    if not request.json:
        abort(400)
    reqJson = request.json
    if 'Price' in reqJson and type(reqJson['Price']) is not int:
        abort(400)

    if 'Title' in reqJson:
        foundFilm['Title'] = reqJson['Title']
    if 'Genre' in reqJson:
        foundFilm['Genre'] = reqJson['Genre']
    if 'Director' in reqJson:
        foundFilm['Director'] = reqJson['Director']
    if 'Price' in reqJson:
        foundFilm['Price'] = reqJson['Price']

    values = (foundFilm['Title'], foundFilm['Genre'], foundFilm['Director'], foundFilm['Price'], foundFilm['id'])
    filmDAO.update(values)

    return jsonify(foundFilm)

# curl -i -H "Content-Type:application/json" -X PUT -d  '{"Title":"The Shawshank Redemption","Genre":"Drama","Director":"Frank Tarabont","Price":8}' http://localhost:5000/films/5




@app.route('/films/<int:id>', methods=['DELETE'])
def delete(id):
    foundFilm = filmDAO.findByID(id)
    if not foundFilm:
        abort(404)

    filmDAO.delete(id)
    return jsonify({"done": True})

 # curl -X DELETE "http://127.0.0.1:5000/films/1"


if __name__ == '__main__':
    app.run(debug=True)
