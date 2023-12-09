from flask import Flask

from modelo.pacientes import inicializar_pacientes
from modelo.medicos import inicializar_medicos

# from modelo.sucursal import inicializar_sucursales

from controlador.rutas_paciente import pacientes_bp
from controlador.rutas_medico import medicos_bp

# from controlador.rutas_sucursal import sucursales_bp

app = Flask(__name__)  # creamos una instancia de la clase Flask

# inicializar_productos()
inicializar_pacientes()
inicializar_medicos()

# registramos el blueprint

app.register_blueprint(pacientes_bp)
app.register_blueprint(medicos_bp)
# app.register_blueprint(sucursales_bp)

if __name__ == "__main__":
    app.run(debug=True)  # iniciamos la aplicación
