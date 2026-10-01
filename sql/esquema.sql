-- ============================================================
-- BASE DE DATOS: FÚTBOL TOTAL
-- Proyecto: Desarrollo de Aplicaciones Web
-- Semana 15 - CRUD, relaciones y consultas JOIN
-- ============================================================


-- ============================================================
-- TABLA: PROVEEDORES
-- ============================================================

CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(100)
);


-- ============================================================
-- TABLA: CLIENTES
-- ============================================================

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    cedula VARCHAR(20),
    telefono VARCHAR(20),
    correo VARCHAR(100)
);


-- ============================================================
-- TABLA: PRODUCTOS
-- ============================================================

CREATE TABLE IF NOT EXISTS productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(100),
    precio DECIMAL(10,2) NOT NULL,
    stock INTEGER NOT NULL,
    id_proveedor INTEGER NOT NULL,

    CONSTRAINT fk_producto_proveedor
        FOREIGN KEY (id_proveedor)
        REFERENCES proveedores(id_proveedor)
);


-- ============================================================
-- TABLA: FACTURAS
-- ============================================================

CREATE TABLE IF NOT EXISTS facturas (
    id_factura SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL,
    fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    total DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_factura_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
);


-- ============================================================
-- TABLA: USUARIOS
-- Sistema de autenticación
-- ============================================================

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario SERIAL PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);