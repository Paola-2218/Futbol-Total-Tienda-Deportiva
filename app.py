import os

from flask import Flask, render_template, redirect, url_for, flash
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg.errors import UniqueViolation

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.usuario_form import UsuarioForm
from forms.login_form import LoginForm

from conexion.conexion import obtener_conexion
from models import Usuario


app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "clave-local-futbol-total-2026"
)


# ============================================================
# CONFIGURACIÓN DE LOGIN
# ============================================================

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"

login_manager.login_message = (
    "Debe iniciar sesión para acceder a esta página."
)

login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(id_usuario):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_usuario, usuario, password
        FROM usuarios
        WHERE id_usuario = %s
    """, (id_usuario,))

    datos = cursor.fetchone()

    cursor.close()
    conn.close()

    if datos is None:
        return None

    return Usuario(
        datos[0],
        datos[1],
        datos[2]
    )


# ============================================================
# DATOS GENERALES
# ============================================================

nombre_tienda = "Fútbol Total"

mensaje_bienvenida = (
    "Tu tienda deportiva especializada en fútbol"
)


# ============================================================
# INICIO
# ============================================================

@app.route("/")
def inicio():

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id_producto,
            nombre,
            categoria,
            precio,
            stock
        FROM productos
        ORDER BY id_producto
    """)

    productos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "index.html",
        nombre_tienda=nombre_tienda,
        mensaje_bienvenida=mensaje_bienvenida,
        productos=productos
    )


# ============================================================
# REGISTRO DE USUARIOS
# ============================================================

@app.route("/registro", methods=["GET", "POST"])
def registro():

    form = UsuarioForm()

    if form.validate_on_submit():

        password_hash = generate_password_hash(
            form.password.data
        )

        conn = obtener_conexion()
        cursor = conn.cursor()

        try:

            cursor.execute("""
                INSERT INTO usuarios (
                    usuario,
                    password
                )
                VALUES (%s, %s)
            """, (
                form.usuario.data,
                password_hash
            ))

            conn.commit()

            flash(
                "Usuario registrado correctamente. "
                "Ahora puede iniciar sesión.",
                "success"
            )

            return redirect(url_for("login"))

        except UniqueViolation:

            conn.rollback()

            flash(
                "El nombre de usuario ya está registrado.",
                "danger"
            )

        finally:

            cursor.close()
            conn.close()

    return render_template(
        "registro.html",
        form=form,
        nombre_tienda=nombre_tienda
    )


# ============================================================
# LOGIN
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:

        return redirect(
            url_for("dashboard")
        )

    form = LoginForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id_usuario,
                usuario,
                password
            FROM usuarios
            WHERE usuario = %s
        """, (
            form.usuario.data,
        ))

        datos = cursor.fetchone()

        cursor.close()
        conn.close()

        if datos is not None:

            password_correcta = check_password_hash(
                datos[2],
                form.password.data
            )

            if password_correcta:

                usuario = Usuario(
                    datos[0],
                    datos[1],
                    datos[2]
                )

                login_user(usuario)

                flash(
                    "Inicio de sesión correcto.",
                    "success"
                )

                return redirect(
                    url_for("dashboard")
                )

        flash(
            "Usuario o contraseña incorrectos.",
            "danger"
        )

    return render_template(
        "login.html",
        form=form,
        nombre_tienda=nombre_tienda
    )


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html",
        nombre_tienda=nombre_tienda
    )


# ============================================================
# CERRAR SESIÓN
# ============================================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Sesión cerrada correctamente.",
        "success"
    )

    return redirect(
        url_for("login")
    )


# ============================================================
# PRODUCTOS - LISTAR
# ============================================================

@app.route("/productos")
@login_required
def productos():

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.id_producto,
            p.nombre,
            p.categoria,
            p.precio,
            p.stock,
            pr.nombre AS proveedor
        FROM productos p
        INNER JOIN proveedores pr
            ON p.id_proveedor = pr.id_proveedor
        ORDER BY p.id_producto
    """)

    productos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "productos.html",
        productos=productos,
        nombre_tienda=nombre_tienda
    )


# ============================================================
# PRODUCTOS - CREAR
# ============================================================

@app.route(
    "/productos/nuevo",
    methods=["GET", "POST"]
)
@login_required
def nuevo_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO productos (
                nombre,
                categoria,
                precio,
                stock,
                id_proveedor
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.categoria.data,
            form.precio.data,
            form.stock.data,
            1
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Producto registrado correctamente.",
            "success"
        )

        return redirect(
            url_for("productos")
        )

    return render_template(
        "formulario_producto.html",
        form=form,
        nombre_tienda=nombre_tienda,
        editar=False
    )


# ============================================================
# PRODUCTOS - MODIFICAR
# ============================================================

@app.route(
    "/productos/editar/<int:id_producto>",
    methods=["GET", "POST"]
)
@login_required
def editar_producto(id_producto):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id_producto,
            nombre,
            categoria,
            precio,
            stock
        FROM productos
        WHERE id_producto = %s
    """, (
        id_producto,
    ))

    producto = cursor.fetchone()

    if producto is None:

        cursor.close()
        conn.close()

        flash(
            "Producto no encontrado.",
            "danger"
        )

        return redirect(
            url_for("productos")
        )

    form = ProductoForm()

    if form.validate_on_submit():

        cursor.execute("""
            UPDATE productos
            SET
                nombre = %s,
                categoria = %s,
                precio = %s,
                stock = %s
            WHERE id_producto = %s
        """, (
            form.nombre.data,
            form.categoria.data,
            form.precio.data,
            form.stock.data,
            id_producto
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Producto modificado correctamente.",
            "success"
        )

        return redirect(
            url_for("productos")
        )

    if not form.is_submitted():

        form.nombre.data = producto[1]
        form.categoria.data = producto[2]
        form.precio.data = producto[3]
        form.stock.data = producto[4]

    cursor.close()
    conn.close()

    return render_template(
        "formulario_producto.html",
        form=form,
        nombre_tienda=nombre_tienda,
        editar=True
    )


# ============================================================
# PRODUCTOS - ELIMINAR
# ============================================================

@app.route(
    "/productos/eliminar/<int:id_producto>",
    methods=["POST"]
)
@login_required
def eliminar_producto(id_producto):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM productos
        WHERE id_producto = %s
    """, (
        id_producto,
    ))

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Producto eliminado correctamente.",
        "success"
    )

    return redirect(
        url_for("productos")
    )


# ============================================================
# CLIENTES - LISTAR
# ============================================================

@app.route("/clientes")
@login_required
def clientes():

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id_cliente,
            nombre,
            cedula,
            telefono,
            correo
        FROM clientes
        ORDER BY id_cliente
    """)

    clientes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "clientes.html",
        clientes=clientes,
        nombre_tienda=nombre_tienda
    )


# ============================================================
# CLIENTES - CREAR
# ============================================================

@app.route(
    "/clientes/nuevo",
    methods=["GET", "POST"]
)
@login_required
def nuevo_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO clientes (
                nombre,
                cedula,
                telefono,
                correo
            )
            VALUES (%s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.cedula.data,
            form.telefono.data,
            form.correo.data
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Cliente registrado correctamente.",
            "success"
        )

        return redirect(
            url_for("clientes")
        )

    return render_template(
        "formulario_cliente.html",
        form=form,
        nombre_tienda=nombre_tienda,
        editar=False
    )


# ============================================================
# CLIENTES - MODIFICAR
# ============================================================

@app.route(
    "/clientes/editar/<int:id_cliente>",
    methods=["GET", "POST"]
)
@login_required
def editar_cliente(id_cliente):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id_cliente,
            nombre,
            cedula,
            telefono,
            correo
        FROM clientes
        WHERE id_cliente = %s
    """, (
        id_cliente,
    ))

    cliente = cursor.fetchone()

    if cliente is None:

        cursor.close()
        conn.close()

        flash(
            "Cliente no encontrado.",
            "danger"
        )

        return redirect(
            url_for("clientes")
        )

    form = ClienteForm()

    if form.validate_on_submit():

        cursor.execute("""
            UPDATE clientes
            SET
                nombre = %s,
                cedula = %s,
                telefono = %s,
                correo = %s
            WHERE id_cliente = %s
        """, (
            form.nombre.data,
            form.cedula.data,
            form.telefono.data,
            form.correo.data,
            id_cliente
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Cliente modificado correctamente.",
            "success"
        )

        return redirect(
            url_for("clientes")
        )

    if not form.is_submitted():

        form.nombre.data = cliente[1]
        form.cedula.data = cliente[2]
        form.telefono.data = cliente[3]
        form.correo.data = cliente[4]

    cursor.close()
    conn.close()

    return render_template(
        "formulario_cliente.html",
        form=form,
        nombre_tienda=nombre_tienda,
        editar=True
    )


# ============================================================
# CLIENTES - ELIMINAR
# ============================================================

@app.route(
    "/clientes/eliminar/<int:id_cliente>",
    methods=["POST"]
)
@login_required
def eliminar_cliente(id_cliente):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM clientes
        WHERE id_cliente = %s
    """, (
        id_cliente,
    ))

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Cliente eliminado correctamente.",
        "success"
    )

    return redirect(
        url_for("clientes")
    )


# ============================================================
# PROVEEDORES - LISTAR
# ============================================================

@app.route("/proveedores")
@login_required
def proveedores():

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id_proveedor,
            nombre,
            telefono,
            correo
        FROM proveedores
        ORDER BY id_proveedor
    """)

    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "proveedores.html",
        proveedores=proveedores,
        nombre_tienda=nombre_tienda
    )


# ============================================================
# PROVEEDORES - CREAR
# ============================================================

@app.route(
    "/proveedores/nuevo",
    methods=["GET", "POST"]
)
@login_required
def nuevo_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO proveedores (
                nombre,
                telefono,
                correo
            )
            VALUES (%s, %s, %s)
        """, (
            form.nombre.data,
            form.telefono.data,
            form.correo.data
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Proveedor registrado correctamente.",
            "success"
        )

        return redirect(
            url_for("proveedores")
        )

    return render_template(
        "formulario_proveedor.html",
        form=form,
        nombre_tienda=nombre_tienda,
        editar=False
    )


# ============================================================
# PROVEEDORES - MODIFICAR
# ============================================================

@app.route(
    "/proveedores/editar/<int:id_proveedor>",
    methods=["GET", "POST"]
)
@login_required
def editar_proveedor(id_proveedor):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id_proveedor,
            nombre,
            telefono,
            correo
        FROM proveedores
        WHERE id_proveedor = %s
    """, (
        id_proveedor,
    ))

    proveedor = cursor.fetchone()

    if proveedor is None:

        cursor.close()
        conn.close()

        flash(
            "Proveedor no encontrado.",
            "danger"
        )

        return redirect(
            url_for("proveedores")
        )

    form = ProveedorForm()

    if form.validate_on_submit():

        cursor.execute("""
            UPDATE proveedores
            SET
                nombre = %s,
                telefono = %s,
                correo = %s
            WHERE id_proveedor = %s
        """, (
            form.nombre.data,
            form.telefono.data,
            form.correo.data,
            id_proveedor
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Proveedor modificado correctamente.",
            "success"
        )

        return redirect(
            url_for("proveedores")
        )

    if not form.is_submitted():

        form.nombre.data = proveedor[1]
        form.telefono.data = proveedor[2]
        form.correo.data = proveedor[3]

    cursor.close()
    conn.close()

    return render_template(
        "formulario_proveedor.html",
        form=form,
        nombre_tienda=nombre_tienda,
        editar=True
    )


# ============================================================
# PROVEEDORES - ELIMINAR
# ============================================================

@app.route(
    "/proveedores/eliminar/<int:id_proveedor>",
    methods=["POST"]
)
@login_required
def eliminar_proveedor(id_proveedor):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM proveedores
        WHERE id_proveedor = %s
    """, (
        id_proveedor,
    ))

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Proveedor eliminado correctamente.",
        "success"
    )

    return redirect(
        url_for("proveedores")
    )


# ============================================================
# FACTURACIÓN - LISTAR
# ============================================================

@app.route("/facturacion")
@login_required
def facturacion():

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            f.id_factura,
            c.nombre AS cliente,
            f.fecha,
            f.total
        FROM facturas f
        INNER JOIN clientes c
            ON f.id_cliente = c.id_cliente
        ORDER BY f.id_factura
    """)

    facturas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "facturacion.html",
        facturas=facturas,
        nombre_tienda=nombre_tienda
    )


# ============================================================
# FACTURACIÓN - CREAR
# ============================================================

@app.route(
    "/facturacion/nuevo",
    methods=["GET", "POST"]
)
@login_required
def nueva_factura():

    form = FacturacionForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO facturas (
                id_cliente,
                total
            )
            VALUES (%s, %s)
        """, (
            1,
            form.total.data
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Factura registrada correctamente.",
            "success"
        )

        return redirect(
            url_for("facturacion")
        )

    return render_template(
        "formulario_facturacion.html",
        form=form,
        nombre_tienda=nombre_tienda
    )


# ============================================================
# EJECUTAR APLICACIÓN
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)