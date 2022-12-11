from sanic import Sanic
from sanic.response import json
from api import api
from components import Base
from sanic_cors import CORS

app = Sanic('chess-api')
cors = CORS(app)

@app.route("/")
async def test(request):
    return json({"hello": "world"})

if __name__ == "__main__":
    Base.metadata.create_all()
    app.blueprint(api)
    app.run(host="0.0.0.0", port=5000)
