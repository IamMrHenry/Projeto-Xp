from controladores.app_controlador import create_app
from utils.criar_db import criar_db

if __name__ == "__main__":
    app = create_app()
    criar_db(app)
    app.run(host='0.0.0.0', port=8080, debug=True)