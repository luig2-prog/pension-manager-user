# LUIS MANUEL HERNANDEZ JIMENEZ

# Parte 1 – Fondos - 80% - Plataforma de Gestión de Fondos Voluntarios

Aplicación web para gestionar fondos de inversión y pensión voluntaria.

## Descripción

Esta aplicación permite a los usuarios:

1. Suscribirse a nuevos fondos (aperturas)
2. Salirse de fondos actuales (cancelaciones)
3. Ver el historial de últimas transacciones (aperturas y cancelaciones)
4. Enviar notificaciones por email o SMS cuando se subscribe a un fondo

## Tecnologías Utilizadas

### Backend

- Python con FastAPI
- DynamoDB para la base de datos
- AWS SES/SNS para notificaciones
- Unittest para pruebas
- Mangum para soporte de AWS Lambda

### Frontend

- React
- Material-UI para componentes de interfaz
- Axios para comunicación con la API

### Infraestructura

- Docker para desarrollo local
- AWS ECS para despliegue
- CloudFormation para IaC (Infraestructura como Código)

## Ejecución Local

### Requisitos

- Docker y Docker Compose
- Python 3.9+
- Node.js 16+

### Ejecución con Docker Compose

Para ejecutar la aplicación sigue estos pasos:

1. Clona o descarga el repositorio completo a tu computadora:

```bash
git clone https://github.com/luig2-prog/pension-manager-user
cd pension-manager-user/1-fondo-v-pensiones
```

2. Levanta todos los servicios con Docker Compose:

```bash
docker-compose up -d
```

3. Una vez que los contenedores estén en ejecución, accede a:

   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Documentación API: http://localhost:8000/docs
   - DynamoDB local: http://localhost:8001

4. Detener todos los servicios con:

```bash
docker-compose down
```

# Parte 2 - 20 % - SQL - Sistema de Gestión de Clientes y Sucursales

Este proyecto implementa un sistema de gestión de clientes y sucursales utilizando PostgreSQL en Docker. El sistema permite gestionar clientes, productos, sucursales y sus relaciones.

## Requisitos Previos

- Docker Desktop instalado y en ejecución
- Docker Compose
- Terminal o Command Prompt

## Configuración de la Base de Datos

### Credenciales de la Base de Datos

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

1. Para detener y eliminar el contenedor:

```bash
docker-compose down
```

2. **Reconstruir el Contenedor**

Si necesitas reconstruir el contenedor desde cero:

```bash
docker-compose down
docker-compose up -d --build
```
