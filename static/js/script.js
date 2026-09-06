const productosRegistrados = [];

const formProducto = document.getElementById("formProducto");
const nombreProducto = document.getElementById("nombreProducto");
const descripcionProducto = document.getElementById("descripcionProducto");
const categoriaProducto = document.getElementById("categoriaProducto");

const errorNombre = document.getElementById("errorNombre");
const errorDescripcion = document.getElementById("errorDescripcion");
const errorCategoria = document.getElementById("errorCategoria");

const mensajeValidacion = document.getElementById("mensajeValidacion");
const listaProductos = document.getElementById("listaProductos");
const totalProductos = document.getElementById("totalProductos");
const mensajeEstadoRegistros = document.getElementById("mensajeEstadoRegistros");

if (formProducto) {
    formProducto.addEventListener("submit", function (evento) {
        evento.preventDefault();

        const nombreValido = validarNombre();
        const descripcionValida = validarDescripcion();
        const categoriaValida = validarCategoria();

        if (!nombreValido || !descripcionValida || !categoriaValida) {
            mostrarMensajeGeneral("Revise los campos marcados antes de registrar.", "danger");
            return;
        }

        const nuevoProducto = {
            nombre: nombreProducto.value.trim(),
            descripcion: descripcionProducto.value.trim(),
            categoria: categoriaProducto.value.trim()
        };

        productosRegistrados.push(nuevoProducto);
        renderizarProductos();

        formProducto.reset();
        limpiarValidaciones();
        mostrarMensajeGeneral("Producto registrado correctamente.", "success");
    });

    nombreProducto.addEventListener("input", validarNombre);
    descripcionProducto.addEventListener("input", validarDescripcion);
    categoriaProducto.addEventListener("change", validarCategoria);

    renderizarProductos();
}

function validarNombre() {
    const nombre = nombreProducto.value.trim();

    if (nombre === "") {
        mostrarError(nombreProducto, errorNombre, "El nombre es obligatorio.");
        return false;
    }

    if (nombre.length < 3) {
        mostrarError(nombreProducto, errorNombre, "El nombre debe tener al menos 3 caracteres.");
        return false;
    }

    mostrarCorrecto(nombreProducto, errorNombre);
    return true;
}

function validarDescripcion() {
    const descripcion = descripcionProducto.value.trim();

    if (descripcion === "") {
        mostrarError(descripcionProducto, errorDescripcion, "La descripción es obligatoria.");
        return false;
    }

    if (descripcion.length < 10) {
        mostrarError(descripcionProducto, errorDescripcion, "La descripción debe tener al menos 10 caracteres.");
        return false;
    }

    mostrarCorrecto(descripcionProducto, errorDescripcion);
    return true;
}

function validarCategoria() {
    const categoria = categoriaProducto.value.trim();

    if (categoria === "") {
        mostrarError(categoriaProducto, errorCategoria, "Debe seleccionar una categoría.");
        return false;
    }

    mostrarCorrecto(categoriaProducto, errorCategoria);
    return true;
}

function mostrarError(campo, contenedor, mensaje) {
    campo.classList.remove("is-valid");
    campo.classList.add("is-invalid");
    contenedor.textContent = mensaje;
}

function mostrarCorrecto(campo, contenedor) {
    campo.classList.remove("is-invalid");
    campo.classList.add("is-valid");
    contenedor.textContent = "";
}

function limpiarValidaciones() {
    nombreProducto.classList.remove("is-valid", "is-invalid");
    descripcionProducto.classList.remove("is-valid", "is-invalid");
    categoriaProducto.classList.remove("is-valid", "is-invalid");

    errorNombre.textContent = "";
    errorDescripcion.textContent = "";
    errorCategoria.textContent = "";
}

function mostrarMensajeGeneral(texto, tipo) {
    mensajeValidacion.innerHTML = "";

    const alerta = document.createElement("div");
    alerta.className = "alert alert-" + tipo;
    alerta.textContent = texto;

    mensajeValidacion.appendChild(alerta);

    setTimeout(function () {
        mensajeValidacion.innerHTML = "";
    }, 3000);
}

function renderizarProductos() {
    listaProductos.innerHTML = "";
    totalProductos.textContent = productosRegistrados.length;

    if (productosRegistrados.length === 0) {
        mensajeEstadoRegistros.innerHTML = '<div class="alert alert-warning">Aún no hay productos registrados.</div>';
        return;
    }

    mensajeEstadoRegistros.innerHTML = "";

    productosRegistrados.forEach(function (producto, indice) {
        const columna = document.createElement("div");
        columna.className = "col-md-6";

        columna.innerHTML = `
            <div class="card h-100">
                <div class="card-body">
                    <h4 class="h5">${producto.nombre}</h4>
                    <p>${producto.descripcion}</p>
                    <span class="badge bg-success mb-3">${producto.categoria}</span>
                    <button class="btn btn-danger btn-sm" onclick="eliminarProducto(${indice})">Eliminar</button>
                </div>
            </div>
        `;

        listaProductos.appendChild(columna);
    });
}

function eliminarProducto(indice) {
    productosRegistrados.splice(indice, 1);
    renderizarProductos();
    mostrarMensajeGeneral("Producto eliminado correctamente.", "danger");
}