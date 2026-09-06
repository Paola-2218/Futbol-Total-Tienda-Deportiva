const productosCatalogo = [
    {
        nombre: "Balones profesionales",
        descripcion: "Balones resistentes para entrenamientos, partidos y competencias.",
        categoria: "Balones",
        imagen: "img/balones.jpg"
    },
    {
        nombre: "Botines deportivos",
        descripcion: "Calzado cómodo y seguro para diferentes tipos de cancha.",
        categoria: "Botines",
        imagen: "img/botines.jpg"
    },
    {
        nombre: "Camisetas oficiales",
        descripcion: "Modelos deportivos para aficionados, equipos y entrenamientos.",
        categoria: "Camisetas",
        imagen: "img/camisetas.jpg"
    }
];

const productosRegistrados = [];

const catalogoProductos = document.getElementById("catalogoProductos");
const spinnerCatalogo = document.getElementById("spinnerCatalogo");
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

const modalProductoTitulo = document.getElementById("modalProductoTitulo");
const modalProductoImagen = document.getElementById("modalProductoImagen");
const modalProductoDescripcion = document.getElementById("modalProductoDescripcion");
const modalProductoCategoria = document.getElementById("modalProductoCategoria");

document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        renderizarCatalogo();

        if (spinnerCatalogo) {
            spinnerCatalogo.style.display = "none";
        }
    }, 1000);

    renderizarProductosRegistrados();
});

if (nombreProducto) {
    nombreProducto.addEventListener("input", validarNombre);
    nombreProducto.addEventListener("blur", validarNombre);
}

if (descripcionProducto) {
    descripcionProducto.addEventListener("input", validarDescripcion);
    descripcionProducto.addEventListener("blur", validarDescripcion);
}

if (categoriaProducto) {
    categoriaProducto.addEventListener("change", validarCategoria);
    categoriaProducto.addEventListener("blur", validarCategoria);
}

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
        renderizarProductosRegistrados();

        formProducto.reset();
        limpiarValidaciones();
        mostrarMensajeGeneral("Producto registrado correctamente.", "success");
    });
}

function renderizarCatalogo() {
    if (!catalogoProductos) {
        return;
    }

    catalogoProductos.innerHTML = "";

    productosCatalogo.forEach(function (producto, indice) {
        const columna = document.createElement("div");
        columna.className = "col-md-6 col-lg-4";

        const tarjeta = document.createElement("div");
        tarjeta.className = "card h-100";

        const imagen = document.createElement("img");
        imagen.src = producto.imagen;
        imagen.alt = producto.nombre;
        imagen.className = "card-img-top";

        const cuerpo = document.createElement("div");
        cuerpo.className = "card-body";

        const titulo = document.createElement("h3");
        titulo.className = "card-title h5";
        titulo.textContent = producto.nombre;

        const descripcion = document.createElement("p");
        descripcion.className = "card-text";
        descripcion.textContent = producto.descripcion;

        const categoria = document.createElement("span");
        categoria.className = "badge bg-success mb-3";
        categoria.textContent = producto.categoria;

        const botonDetalle = document.createElement("button");
        botonDetalle.className = "btn btn-primary btn-sm d-block";
        botonDetalle.textContent = "Ver detalles";
        botonDetalle.setAttribute("data-bs-toggle", "modal");
        botonDetalle.setAttribute("data-bs-target", "#modalProducto");
        botonDetalle.addEventListener("click", function () {
            mostrarDetalleProducto(indice);
        });

        cuerpo.appendChild(titulo);
        cuerpo.appendChild(descripcion);
        cuerpo.appendChild(categoria);
        cuerpo.appendChild(botonDetalle);

        tarjeta.appendChild(imagen);
        tarjeta.appendChild(cuerpo);
        columna.appendChild(tarjeta);
        catalogoProductos.appendChild(columna);
    });
}

function mostrarDetalleProducto(indice) {
    const producto = productosCatalogo[indice];

    if (!producto) {
        return;
    }

    modalProductoTitulo.textContent = producto.nombre;
    modalProductoImagen.src = producto.imagen;
    modalProductoImagen.alt = producto.nombre;
    modalProductoDescripcion.textContent = producto.descripcion;
    modalProductoCategoria.textContent = producto.categoria;
}

function renderizarProductosRegistrados() {
    if (!listaProductos || !totalProductos) {
        return;
    }

    listaProductos.innerHTML = "";
    totalProductos.textContent = productosRegistrados.length;

    if (productosRegistrados.length === 0) {
        if (mensajeEstadoRegistros) {
            mensajeEstadoRegistros.innerHTML = "";

            const alerta = document.createElement("div");
            alerta.className = "alert alert-warning";
            alerta.textContent = "Aún no hay productos registrados.";

            mensajeEstadoRegistros.appendChild(alerta);
        }

        return;
    }

    if (mensajeEstadoRegistros) {
        mensajeEstadoRegistros.innerHTML = "";
    }

    productosRegistrados.forEach(function (producto, indice) {
        const columna = document.createElement("div");
        columna.className = "col-md-6";

        const tarjeta = document.createElement("div");
        tarjeta.className = "card h-100 border";

        const cuerpo = document.createElement("div");
        cuerpo.className = "card-body";

        const titulo = document.createElement("h4");
        titulo.className = "card-title h5";
        titulo.textContent = producto.nombre;

        const descripcion = document.createElement("p");
        descripcion.className = "card-text";
        descripcion.textContent = producto.descripcion;

        const categoria = document.createElement("span");
        categoria.className = "badge bg-success mb-3";
        categoria.textContent = producto.categoria;

        const botonEliminar = document.createElement("button");
        botonEliminar.className = "btn btn-danger btn-sm d-block";
        botonEliminar.textContent = "Eliminar";
        botonEliminar.addEventListener("click", function () {
            eliminarProducto(indice);
        });

        cuerpo.appendChild(titulo);
        cuerpo.appendChild(descripcion);
        cuerpo.appendChild(categoria);
        cuerpo.appendChild(botonEliminar);

        tarjeta.appendChild(cuerpo);
        columna.appendChild(tarjeta);
        listaProductos.appendChild(columna);
    });
}

function eliminarProducto(indice) {
    productosRegistrados.splice(indice, 1);
    renderizarProductosRegistrados();
    mostrarMensajeGeneral("Producto eliminado correctamente.", "danger");
}

function validarNombre() {
    const nombre = nombreProducto.value.trim();

    if (nombre === "") {
        mostrarError(nombreProducto, errorNombre, "El nombre del producto es obligatorio.");
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

function mostrarError(campo, contenedorError, mensaje) {
    if (!campo) {
        return;
    }

    campo.classList.remove("is-valid");
    campo.classList.add("is-invalid");

    if (contenedorError) {
        contenedorError.textContent = mensaje;
    }
}

function mostrarCorrecto(campo, contenedorError) {
    if (!campo) {
        return;
    }

    campo.classList.remove("is-invalid");
    campo.classList.add("is-valid");

    if (contenedorError) {
        contenedorError.textContent = "";
    }
}

function limpiarValidaciones() {
    if (nombreProducto) {
        nombreProducto.classList.remove("is-valid", "is-invalid");
    }

    if (descripcionProducto) {
        descripcionProducto.classList.remove("is-valid", "is-invalid");
    }

    if (categoriaProducto) {
        categoriaProducto.classList.remove("is-valid", "is-invalid");
    }

    if (errorNombre) {
        errorNombre.textContent = "";
    }

    if (errorDescripcion) {
        errorDescripcion.textContent = "";
    }

    if (errorCategoria) {
        errorCategoria.textContent = "";
    }
}

function mostrarMensajeGeneral(texto, tipo) {
    if (!mensajeValidacion) {
        return;
    }

    mensajeValidacion.innerHTML = "";

    const alerta = document.createElement("div");
    alerta.className = "alert alert-" + tipo;
    alerta.textContent = texto;

    mensajeValidacion.appendChild(alerta);

    setTimeout(function () {
        mensajeValidacion.innerHTML = "";
    }, 3000);
}