-- Initial commit

-- Create Cliente table
CREATE TABLE Cliente (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    ciudad VARCHAR(100) NOT NULL
);

-- Create Sucursal table
CREATE TABLE Sucursal (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ciudad VARCHAR(100) NOT NULL
);

-- Create Producto table
CREATE TABLE Producto (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipoProducto VARCHAR(100) NOT NULL
);

-- Create Inscripcion table
CREATE TABLE Inscripcion (
    idProducto INTEGER,
    idCliente INTEGER,
    PRIMARY KEY (idProducto, idCliente),
    FOREIGN KEY (idProducto) REFERENCES Producto(id),
    FOREIGN KEY (idCliente) REFERENCES Cliente(id)
);

-- Create Disponibilidad table
CREATE TABLE Disponibilidad (
    idSucursal INTEGER,
    idProducto INTEGER,
    PRIMARY KEY (idSucursal, idProducto),
    FOREIGN KEY (idSucursal) REFERENCES Sucursal(id),
    FOREIGN KEY (idProducto) REFERENCES Producto(id)
);

-- Create Visitan table
CREATE TABLE Visitan (
    idSucursal INTEGER,
    idCliente INTEGER,
    fechaVisita DATE NOT NULL,
    PRIMARY KEY (idSucursal, idCliente),
    FOREIGN KEY (idSucursal) REFERENCES Sucursal(id),
    FOREIGN KEY (idCliente) REFERENCES Cliente(id)
);

-- Insert sample data
INSERT INTO Cliente (nombre, apellidos, ciudad) VALUES
    ('Juan', 'Pérez', 'Madrid'),
    ('María', 'García', 'Barcelona'),
    ('Carlos', 'López', 'Valencia');

INSERT INTO Sucursal (nombre, ciudad) VALUES
    ('Sucursal Central', 'Madrid'),
    ('Sucursal Norte', 'Barcelona'),
    ('Sucursal Sur', 'Valencia');

INSERT INTO Producto (nombre, tipoProducto) VALUES
    ('Cuenta Ahorro', 'Cuenta'),
    ('Tarjeta Crédito', 'Tarjeta'),
    ('Préstamo Personal', 'Préstamo');

-- Sample inscriptions
INSERT INTO Inscripcion (idProducto, idCliente) VALUES
    (1, 1),
    (2, 1),
    (1, 2);

-- Sample availability
INSERT INTO Disponibilidad (idSucursal, idProducto) VALUES
    (1, 1),
    (1, 2),
    (2, 1),
    (3, 3);

-- Sample visits
INSERT INTO Visitan (idSucursal, idCliente, fechaVisita) VALUES
    (1, 1, '2024-03-28'),
    (2, 2, '2024-03-28'),
    (1, 3, '2024-03-27');