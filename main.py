from base import *
from blueprint_routes.publisher import publisher as publisher
from blueprint_routes.auth import auth as auth
from blueprint_routes.common import common as common

app=Flask(__name__)

app.register_blueprint(publisher)
app.register_blueprint(auth)
app.register_blueprint(common)


CORS(app)


load_dotenv()

if(os.environ.get("SECRET")):
    app.run(debug=True)
else:
    print("Please Create .env file")