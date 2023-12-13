from flask import Flask

from modelo.pacientes import inicializar_pacientes
from modelo.medicos import inicializar_medicos
from modelo.turnos import inicializar_turnos
from modelo.agenda_medicos import inicializar_agenda_medicos

# from modelo.sucursal import inicializar_sucursales

from controlador.rutas_paciente import pacientes_bp
from controlador.rutas_medico import medicos_bp
from controlador.rutas_turno import turnos_bp
from controlador.rutas_agenda_medicos import agenda_medicos_bp

# from controlador.rutas_sucursal import sucursales_bp

app = Flask(__name__)  # creamos una instancia de la clase Flask

# inicializar_productos()
inicializar_pacientes()
inicializar_medicos()
inicializar_turnos()
inicializar_agenda_medicos()

# registramos el blueprint

app.register_blueprint(pacientes_bp)
app.register_blueprint(medicos_bp)
app.register_blueprint(turnos_bp)
app.register_blueprint(agenda_medicos_bp)
# app.register_blueprint(sucursales_bp)

if __name__ == "__main__":
    app.run(debug=True)  # iniciamos la aplicación
