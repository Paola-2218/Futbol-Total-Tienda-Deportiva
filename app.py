import os
import sqlite3

from flask import Flask, render_template, redirect, url_for

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm


app = Flask(__name__)

# Clave secreta necesaria para Flask-WTF y la protección CSRF
app.config["SECRET_KEY"] = "clave-secreta-futbol-total-2026"


# Datos generales del sistema
nombre_tienda = "Fútbol Total"
mensaje_bienvenida = "Tu tienda deportiva especializada en fútbol"


# Ruta de la base de datos SQLite
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATABASE = os.path.join(DATA_DIR, "ferreteria.db")


# Crear la carpeta data y la tabla de productos
def inicializar_base_datos():

    os.makedirs(DATA_DIR, exist_ok=True)

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Inicializar la base de datos al iniciar la aplicación
inicializar_base_datos()


# Clientes de ejemplo
clientes_demo = [
    {
        "nombre": "Carlos Medina",
        "correo": "carlos@email.com",
        "telefono": "099111222"
    },
    {
        "nombre": "Ana Torres",
        "correo": "ana@email.com",
        "telefono": "098333444"
    },
    {
        "nombre": "Luis Vargas",
        "correo": "luis@email.com",
        "telefono": "097555666"
    }
]


# Proveedores de ejemplo
proveedores_demo = [
    {
        "empresa": "Deportes Ecuador",
        "producto": "Balones",
        "ciudad": "Quito"
    },
    {
        "empresa": "Sport Shoes",
        "producto": "Botines",
        "ciudad": "Guayaquil"
    },
    {
        "empresa": "Uniformes Pro",
        "producto": "Camisetas",
        "ciudad": "Cuenca"
    }
]


# Facturas de ejemplo
facturas_demo = [
    {
        "numero": "F001",
        "cliente": "Carlos Medina",
        "total": 63.00
    },
    {
        "numero": "F002",
        "cliente": "Ana Torres",
        "total": 35.00
    },
    {
        "numero": "F003",
        "cliente": "Luis Vargas",
        "total": 93.00
    }
]


# Página de inicio
@app.route("/")
def inicio():

    return render_template(
        "index.html",
        nombre_tienda=nombre_tienda,
        mensaje_bienvenida=mensaje_bienvenida
    )


# Mostrar productos desde SQLite
@app.route("/productos")
def productos():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre, categoria, precio, stock
        FROM productos
        ORDER BY id
    """)

    productos = cursor.fetchall()

    conn.close()

    return render_template(
        "productos.html",
        productos=productos,
        nombre_tienda=nombre_tienda
    )


# Formulario para registrar productos
@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        conn = sqlite3.connect(DATABASE)

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO productos (nombre, categoria, precio, stock)
            VALUES (?, ?, ?, ?)
        """, (
            form.nombre.data,
            form.categoria.data,
            form.precio.data,
            form.stock.data
        ))

        conn.commit()

        conn.close()

        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        form=form,
        nombre_tienda=nombre_tienda
    )


# Mostrar clientes
@app.route("/clientes")
def clientes():

    return render_template(
        "clientes.html",
        clientes=clientes_demo,
        nombre_tienda=nombre_tienda
    )


# Formulario para registrar clientes
@app.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        nuevo = {
            "nombre": form.nombre.data,
            "correo": form.correo.data,
            "telefono": form.telefono.data
        }

        clientes_demo.append(nuevo)

        return redirect(url_for("clientes"))

    return render_template(
        "formulario_cliente.html",
        form=form,
        nombre_tienda=nombre_tienda
    )


# Mostrar proveedores
@app.route("/proveedores")
def proveedores():

    return render_template(
        "proveedores.html",
        proveedores=proveedores_demo,
        nombre_tienda=nombre_tienda
    )


# Formulario para registrar proveedores
@app.route("/proveedores/nuevo", methods=["GET", "POST"])
def nuevo_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        nuevo = {
            "empresa": form.empresa.data,
            "producto": form.producto.data,
            "ciudad": form.ciudad.data
        }

        proveedores_demo.append(nuevo)

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario_proveedor.html",
        form=form,
        nombre_tienda=nombre_tienda
    )


# Mostrar facturación
@app.route("/facturacion")
def facturacion():

    return render_template(
        "facturacion.html",
        facturas=facturas_demo,
        nombre_tienda=nombre_tienda
    )


# Formulario para registrar facturas
@app.route("/facturacion/nuevo", methods=["GET", "POST"])
def nueva_factura():

    form = FacturacionForm()

    if form.validate_on_submit():

        nueva = {
            "numero": form.numero.data,
            "cliente": form.cliente.data,
            "total": form.total.data
        }

        facturas_demo.append(nueva)

        return redirect(url_for("facturacion"))

    return render_template(
        "formulario_facturacion.html",
        form=form,
        nombre_tienda=nombre_tienda
    )


# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True)