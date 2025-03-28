# Plataforma de Gestión de Fondos Voluntarios
# LUIS MANUEL HERNANDEZ JIMENEZ

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
   ```
   git clone https://github.com/luig2-prog/pension-manager-user
   cd pension-manager-user
   ```

2. Levanta todos los servicios con Docker Compose:
   ```
   docker-compose up -d
   ```

3. Una vez que los contenedores estén en ejecución, accede a:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Documentación API: http://localhost:8000/docs
   - DynamoDB local: http://localhost:8001

4. Detener todos los servicios con:

   ```
   docker-compose down
   ```

