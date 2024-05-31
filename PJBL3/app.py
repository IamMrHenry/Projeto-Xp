from controladores.app_controlador import create_app
from utils.criar_db import criar_db

if __name__ == "__main__":
    # 0. Todos os processos do site são separados em diferentes arquivos para separar e melhorar a localização
    # de diferentes partes desse código, para continuar a endenter o código vá para o ponto 1. no arquivo 
    # app_controlador.py na pasta controladores.
    app = create_app()
    criar_db(app)
    app.run(host='0.0.0.0', port=8080, debug=True)