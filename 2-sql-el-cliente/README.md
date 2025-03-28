# El Cliente - Sistema de Gestión de Clientes y Sucursales

Este proyecto implementa un sistema de gestión de clientes y sucursales utilizando PostgreSQL en Docker. El sistema permite gestionar clientes, productos, sucursales y sus relaciones.

## Requisitos Previos

- Docker Desktop instalado y en ejecución
- Docker Compose
- Terminal o Command Prompt

## Configuración de la Base de Datos

### Credenciales

- **Host**: localhost
- **Puerto**: 5432
- **Base de datos**: el_cliente
- **Usuario**: admin
- **Contraseña**: admin123

## Pasos para Ejecutar el Proyecto

1. **Construir e Iniciar el Contenedor Docker**

```bash
cd 2-sql-el-cliente
docker-compose up -d --build
```

2. **Verificar que el Contenedor está Corriendo**

```bash
docker ps | grep el-cliente-db
```

3. **Ejecutar la Consulta SQL**

```bash
docker exec -it el-cliente-db psql -U admin -d el_cliente -f docker-entrypoint-initdb.d/select.sql
```

## Detener el Proyecto

Para detener y eliminar el contenedor:

```bash
docker-compose down
```

3. **Reconstruir el Contenedor**
   Si necesitas reconstruir el contenedor desde cero:
   ```bash
   docker-compose down
   docker-compose up -d --build
   ```
