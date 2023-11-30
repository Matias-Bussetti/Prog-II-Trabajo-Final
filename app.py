from flask import Flask
from modelo.producto import inicializar_productos
from modelo.sucursal import inicializar_sucursales

from controlador.rutas_producto import productos_bp
from controlador.rutas_sucursal import sucursales_bp

app = Flask(__name__)  # creamos una instancia de la clase Flask

inicializar_productos()
inicializar_sucursales()

# registramos el blueprint

app.register_blueprint(productos_bp)
app.register_blueprint(sucursales_bp)

if __name__ == "__main__":
    app.run(debug=True)  # iniciamos la aplicación
