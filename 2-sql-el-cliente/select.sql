-- Initial commit

SELECT DISTINCT c.nombre, c.apellidos
FROM Cliente c
INNER JOIN Inscripcion i ON c.id = i.idCliente
INNER JOIN Disponibilidad d ON i.idProducto = d.idProducto
INNER JOIN Visitan v ON c.id = v.idCliente AND d.idSucursal = v.idSucursal
WHERE NOT EXISTS (
    SELECT 1
    FROM Disponibilidad d2
    WHERE d2.idProducto = i.idProducto
    AND d2.idSucursal NOT IN (
        SELECT v2.idSucursal
        FROM Visitan v2
        WHERE v2.idCliente = c.id
    )
);