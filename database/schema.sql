-- ============================================================
-- Esquema de base de datos para sistema de inventario
-- Motor: SQLite
-- Autor: Miguel Gutierrez, Miguel Scott, Mary Perez
-- Generado a partir del diagrama dbdiagram.io proporcionado.
-- ============================================================

PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------
-- Tablas de catalogo
-- ------------------------------------------------------------

CREATE TABLE compania_telefonica (
    id_compania_telefonica INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(64) NOT NULL UNIQUE,
    descripcion VARCHAR(254)
);

-- ------------------------------------------------------------
-- Tablas de autenticacion
-- ------------------------------------------------------------

-- los roles se gestionan con los grupos de Django (auth_group)
CREATE TABLE usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(128) NOT NULL UNIQUE,
    clave_hash VARCHAR(256) NOT NULL,
    last_login DATETIME,
    is_staff BOOLEAN NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    is_superuser BOOLEAN NOT NULL DEFAULT 0,
    correo_electronico VARCHAR(254) UNIQUE,
    numero_telefonico VARCHAR(32),
    codigo_telefonico VARCHAR(8) DEFAULT '505',
    id_compania_telefonica INTEGER,
    -- nullable solo en usuario: el primer usuario se crea sin creador (el resto NOT NULL)
    creado_por INTEGER,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME,
    actualizado_por INTEGER,

    CHECK (
    	(fecha_actualizacion IS NULL
AND actualizado_por IS NULL)
OR
    	(fecha_actualizacion IS NOT NULL
AND actualizado_por IS NOT NULL)
),
    FOREIGN KEY (id_compania_telefonica) 
    	REFERENCES compania_telefonica(id_compania_telefonica),
    FOREIGN KEY (creado_por) REFERENCES usuario(id_usuario),
    FOREIGN KEY (actualizado_por) REFERENCES usuario(id_usuario)
);

-- ------------------------------------------------------------
-- Tablas de productos
-- ------------------------------------------------------------

CREATE TABLE marca (
    id_marca INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(128) NOT NULL UNIQUE,
    descripcion VARCHAR(254),
    creado_por INTEGER NOT NULL,
    -- nota general: fecha_creacion usa DEFAULT CURRENT_TIMESTAMP; fecha_actualizacion la
    -- llena la aplicación (SQLite no tiene ON UPDATE; Django la asigna en cada save)
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME,
    actualizado_por INTEGER,
    
    CHECK (
    	(fecha_actualizacion IS NULL
AND actualizado_por IS NULL)
OR
    	(fecha_actualizacion IS NOT NULL
AND actualizado_por IS NOT NULL)
),

    FOREIGN KEY (creado_por) REFERENCES usuario(id_usuario),
    FOREIGN KEY (actualizado_por) REFERENCES usuario(id_usuario)
);

CREATE TABLE categoria (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(128) NOT NULL UNIQUE,
    descripcion VARCHAR(254),
    creado_por INTEGER NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME,
    actualizado_por INTEGER,
    
    CHECK (
    	(fecha_actualizacion IS NULL
AND actualizado_por IS NULL)
OR
    	(fecha_actualizacion IS NOT NULL
AND actualizado_por IS NOT NULL)
),

    FOREIGN KEY (creado_por) REFERENCES usuario(id_usuario),
    FOREIGN KEY (actualizado_por) REFERENCES usuario(id_usuario)
);

CREATE TABLE producto (
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    id_marca INTEGER NOT NULL,
    id_categoria INTEGER NOT NULL,
    nombre VARCHAR(254) NOT NULL,
    descripcion VARCHAR(254),
    creado_por INTEGER NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME,
    actualizado_por INTEGER,
    
    CHECK (
    	(fecha_actualizacion IS NULL
AND actualizado_por IS NULL)
OR
    	(fecha_actualizacion IS NOT NULL
AND actualizado_por IS NOT NULL)
),

    FOREIGN KEY (id_marca) REFERENCES marca(id_marca),
    FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria),
    FOREIGN KEY (creado_por) REFERENCES usuario(id_usuario),
    FOREIGN KEY (actualizado_por) REFERENCES usuario(id_usuario)
);

CREATE TABLE variante (
    id_variante INTEGER PRIMARY KEY AUTOINCREMENT,
    id_producto INTEGER NOT NULL,
    nombre VARCHAR(128) NOT NULL,
    descripcion VARCHAR(254),
    creado_por INTEGER NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME,
    actualizado_por INTEGER,
    
    UNIQUE (id_producto, nombre)
    
    CHECK (
    	(fecha_actualizacion IS NULL
AND actualizado_por IS NULL)
OR
    	(fecha_actualizacion IS NOT NULL
AND actualizado_por IS NOT NULL)
),

    FOREIGN KEY (id_producto) REFERENCES producto(id_producto),
    FOREIGN KEY (creado_por) REFERENCES usuario(id_usuario),
    FOREIGN KEY (actualizado_por) REFERENCES usuario(id_usuario)
);

-- ------------------------------------------------------------
-- Tablas de distribuidores
-- ------------------------------------------------------------

CREATE TABLE distribuidor (
    id_distribuidor INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(64) NOT NULL UNIQUE,
    descripcion VARCHAR(254),
    correo_electronico VARCHAR(254) UNIQUE,
    numero_telefonico VARCHAR(32),
    codigo_telefonico VARCHAR(4) DEFAULT '505',
    id_compania_telefonica INTEGER,
    creado_por INTEGER NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME,
    actualizado_por INTEGER,

    CHECK (
    	(fecha_actualizacion IS NULL
AND actualizado_por IS NULL)
OR
    	(fecha_actualizacion IS NOT NULL
AND actualizado_por IS NOT NULL)
),

    FOREIGN KEY (id_compania_telefonica)
        REFERENCES compania_telefonica(id_compania_telefonica),
    FOREIGN KEY (creado_por) REFERENCES usuario(id_usuario),
    FOREIGN KEY (actualizado_por) REFERENCES usuario(id_usuario)
);

-- ------------------------------------------------------------
-- Tablas de gestion de compras
-- ------------------------------------------------------------

CREATE TABLE estado_compra (
    id_estado_compra INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(32) NOT NULL UNIQUE,
    descripcion VARCHAR(254)
);

CREATE TABLE compra (
    id_compra INTEGER PRIMARY KEY AUTOINCREMENT,
    id_distribuidor INTEGER NOT NULL,
    id_estado_compra INTEGER NOT NULL,
    subtotal DECIMAL(12, 2) NOT NULL,
    descuento DECIMAL(12, 2) NOT NULL DEFAULT 0,
    impuesto DECIMAL(12, 2) NOT NULL DEFAULT 0,
    total DECIMAL(12, 2) NOT NULL,
    fecha DATETIME NOT NULL,
    descripcion VARCHAR(254),
    creado_por INTEGER NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME,
    actualizado_por INTEGER,
	
    CHECK (subtotal >= 0),
    CHECK (descuento >= 0),
    CHECK (impuesto >= 0),
    CHECK (total >= 0),
    CHECK (
    	(fecha_actualizacion IS NULL
AND actualizado_por IS NULL)
OR
    	(fecha_actualizacion IS NOT NULL
AND actualizado_por IS NOT NULL)
),
    FOREIGN KEY (id_distribuidor)
        REFERENCES distribuidor(id_distribuidor),
    FOREIGN KEY (id_estado_compra)
        REFERENCES estado_compra(id_estado_compra),
    FOREIGN KEY (creado_por) REFERENCES usuario(id_usuario),
    FOREIGN KEY (actualizado_por) REFERENCES usuario(id_usuario)
);

CREATE TABLE detalle_compra (
    id_detalle_compra INTEGER PRIMARY KEY AUTOINCREMENT,
    id_compra INTEGER NOT NULL,
    id_variante INTEGER NOT NULL,
    cantidad DECIMAL(13, 2) NOT NULL,
    costo_unitario DECIMAL(12, 2) NOT NULL,
    descuento DECIMAL(12, 2) NOT NULL DEFAULT 0,
    impuesto DECIMAL(12, 2) NOT NULL DEFAULT 0,
    subtotal DECIMAL(12, 2) NOT NULL,
    descripcion VARCHAR(254),
    creado_por INTEGER NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME,
    actualizado_por INTEGER,
	
    UNIQUE (id_compra, id_variante)
    
    CHECK (subtotal >= 0),
    CHECK (descuento >= 0),
    CHECK (impuesto >= 0),
    CHECK (cantidad >= 0),
    CHECK (costo_unitario >= 0),
    CHECK (
    	(fecha_actualizacion IS NULL
AND actualizado_por IS NULL)
OR
    	(fecha_actualizacion IS NOT NULL
AND actualizado_por IS NOT NULL)
),
   
    FOREIGN KEY (id_compra) REFERENCES compra(id_compra),
    FOREIGN KEY (id_variante) REFERENCES variante(id_variante),
    FOREIGN KEY (creado_por) REFERENCES usuario(id_usuario),
    FOREIGN KEY (actualizado_por) REFERENCES usuario(id_usuario)
);

-- ------------------------------------------------------------
-- Tablas de gestion de ventas
-- ------------------------------------------------------------

CREATE TABLE venta (
    id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
    subtotal DECIMAL(12, 2) NOT NULL,
    descuento DECIMAL(12, 2) NOT NULL DEFAULT 0,
    impuesto DECIMAL(12, 2) NOT NULL DEFAULT 0,
    total DECIMAL(12, 2) NOT NULL,
    fecha DATETIME NOT NULL,
    descripcion VARCHAR(254),
    creado_por INTEGER NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME,
    actualizado_por INTEGER,
    
    CHECK (subtotal >= 0),
    CHECK (descuento >= 0),
    CHECK (impuesto >= 0),
    CHECK (total >= 0),
    CHECK (
    	(fecha_actualizacion IS NULL
AND actualizado_por IS NULL)
OR
    	(fecha_actualizacion IS NOT NULL
AND actualizado_por IS NOT NULL)
),
    
    FOREIGN KEY (creado_por) REFERENCES usuario(id_usuario),
    FOREIGN KEY (actualizado_por) REFERENCES usuario(id_usuario)
);

CREATE TABLE detalle_venta (
    id_detalle_venta INTEGER PRIMARY KEY AUTOINCREMENT,
    id_venta INTEGER NOT NULL,
    id_variante INTEGER NOT NULL,
    cantidad DECIMAL(13, 2) NOT NULL,
    precio_unitario DECIMAL(12, 2) NOT NULL,
    descuento DECIMAL(12, 2) NOT NULL DEFAULT 0,
    impuesto DECIMAL(12, 2) NOT NULL DEFAULT 0,
    subtotal DECIMAL(12, 2) NOT NULL,
    descripcion VARCHAR(254),
    creado_por INTEGER NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME,
    actualizado_por INTEGER,

    UNIQUE (id_venta, id_variante)
    
    CHECK (subtotal >= 0),
    CHECK (descuento >= 0),
    CHECK (impuesto >= 0),
    CHECK (cantidad >= 0),
    CHECK (precio_unitario >= 0)
    CHECK (
    	(fecha_actualizacion IS NULL
AND actualizado_por IS NULL)
OR
    	(fecha_actualizacion IS NOT NULL
AND actualizado_por IS NOT NULL)
),
    
    FOREIGN KEY (id_venta) REFERENCES venta(id_venta),
    FOREIGN KEY (id_variante) REFERENCES variante(id_variante),
    FOREIGN KEY (creado_por) REFERENCES usuario(id_usuario),
    FOREIGN KEY (actualizado_por) REFERENCES usuario(id_usuario)
);

-- ------------------------------------------------------------
-- Tablas de movimientos de inventario
-- ------------------------------------------------------------

CREATE TABLE inventario (
    id_inventario INTEGER PRIMARY KEY AUTOINCREMENT,
    id_variante INTEGER NOT NULL UNIQUE,
    stock_actual DECIMAL(13, 2) NOT NULL DEFAULT 0,
    stock_minimo DECIMAL(13, 2) NOT NULL DEFAULT 0,
    creado_por INTEGER NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME,
    actualizado_por INTEGER,

    CHECK (stock_actual >= 0),
    CHECK (stock_minimo >= 0),
    CHECK (
    	(fecha_actualizacion IS NULL
AND actualizado_por IS NULL)
OR
    	(fecha_actualizacion IS NOT NULL
AND actualizado_por IS NOT NULL)
),

    FOREIGN KEY (id_variante) REFERENCES variante(id_variante),
    FOREIGN KEY (creado_por) REFERENCES usuario(id_usuario),
    FOREIGN KEY (actualizado_por) REFERENCES usuario(id_usuario)
);

CREATE TABLE tipo_movimiento (
    id_tipo_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(32) NOT NULL UNIQUE,
    descripcion VARCHAR(254)
);

CREATE TABLE movimiento_inventario (
    id_movimiento_inventario INTEGER PRIMARY KEY AUTOINCREMENT,
    id_tipo_movimiento INTEGER NOT NULL,
    id_compra INTEGER,
    id_venta INTEGER,
    fecha DATETIME NOT NULL,
    descripcion VARCHAR(254),
    creado_por INTEGER NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME,
    actualizado_por INTEGER,

    CHECK (id_compra IS NULL OR id_venta IS NULL),
    CHECK (
    	(fecha_actualizacion IS NULL
AND actualizado_por IS NULL)
OR
    	(fecha_actualizacion IS NOT NULL
AND actualizado_por IS NOT NULL)
),
    FOREIGN KEY (id_tipo_movimiento)
        REFERENCES tipo_movimiento(id_tipo_movimiento),
    FOREIGN KEY (id_compra) REFERENCES compra(id_compra),
    FOREIGN KEY (id_venta) REFERENCES venta(id_venta),
    FOREIGN KEY (creado_por) REFERENCES usuario(id_usuario),
    FOREIGN KEY (actualizado_por) REFERENCES usuario(id_usuario)
);

CREATE TABLE detalle_movimiento (
    id_detalle_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
    id_movimiento_inventario INTEGER NOT NULL,
    id_variante INTEGER NOT NULL,
    cantidad DECIMAL(13, 2) NOT NULL,
    descripcion VARCHAR(254),
    creado_por INTEGER NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME,
    actualizado_por INTEGER,
	
    UNIQUE (id_movimiento_inventario, id_variante)
    
    CHECK (cantidad >= 0),
    CHECK (
    	(fecha_actualizacion IS NULL
AND actualizado_por IS NULL)
OR
    	(fecha_actualizacion IS NOT NULL
AND actualizado_por IS NOT NULL)
),

    FOREIGN KEY (id_movimiento_inventario)
        REFERENCES movimiento_inventario(id_movimiento_inventario),
    FOREIGN KEY (id_variante) REFERENCES variante(id_variante),
    FOREIGN KEY (creado_por) REFERENCES usuario(id_usuario),
    FOREIGN KEY (actualizado_por) REFERENCES usuario(id_usuario)
);

-- ------------------------------------------------------------
-- Fin del esquema
-- ------------------------------------------------------------
