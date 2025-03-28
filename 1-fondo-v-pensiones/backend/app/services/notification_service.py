import boto3
import os
import logging
from typing import Dict, Any, Tuple
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        # Configurar clientes de AWS
        self.ses_client = boto3.client('ses',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        self.sns_client = boto3.client('sns',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        self.source_email = os.getenv('AWS_SES_SOURCE_EMAIL')

    async def send_email(self, email: str, fund_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Envía un email usando AWS SES
        Returns: (success: bool, message: str)
        """
        try:
            subject = f"Notificación sobre el fondo {fund_data['nombre']}"
            body_html = f"""
                <html>
                <head></head>
                <body>
                    <h2>Información sobre su fondo</h2>
                    <p>Detalles del fondo:</p>
                    <ul>
                        <li>Nombre: {fund_data['nombre']}</li>
                        <li>Categoría: {fund_data['categoria']}</li>
                        <li>Monto mínimo: ${fund_data['monto_minimo']:,}</li>
                    </ul>
                    <p>Gracias por confiar en nosotros para administrar sus inversiones.</p>
                </body>
                </html>
            """
            body_text = f"""
                Información sobre su fondo
                
                Detalles del fondo:
                - Nombre: {fund_data['nombre']}
                - Categoría: {fund_data['categoria']}
                - Monto mínimo: ${fund_data['monto_minimo']:,}
                
                Gracias por confiar en nosotros para administrar sus inversiones.
            """

            response = self.ses_client.send_email(
                Source=self.source_email,
                Destination={
                    'ToAddresses': [email]
                },
                Message={
                    'Subject': {
                        'Data': subject
                    },
                    'Body': {
                        'Text': {
                            'Data': body_text
                        },
                        'Html': {
                            'Data': body_html
                        }
                    }
                }
            )
            logger.info(f"Email enviado exitosamente: {response['MessageId']}")
            return True, "Email enviado exitosamente"
        except ClientError as e:
            error_message = str(e)
            if "Email address is not verified" in error_message:
                logger.error(f"Error: Dirección de correo no verificada en AWS SES: {email}")
                return False, f"La dirección de correo {email} no está verificada en AWS SES. Por favor, verifica la dirección en la consola de AWS SES."
            logger.error(f"Error al enviar email: {error_message}")
            return False, f"Error al enviar el email: {error_message}"

    async def send_sms(self, phone: str, fund_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Envía un SMS usando AWS SNS
        Returns: (success: bool, message: str)
        """
        try:
            message = f"""
                Información del fondo {fund_data['nombre']}:
                Categoría: {fund_data['categoria']}
                Monto mínimo: ${fund_data['monto_minimo']:,}
                Gracias por confiar en nosotros.
            """

            response = self.sns_client.publish(
                PhoneNumber=phone,
                Message=message,
                MessageAttributes={
                    'AWS.SNS.SMS.SenderID': {
                        'DataType': 'String',
                        'StringValue': 'FONDOS'
                    },
                    'AWS.SNS.SMS.SMSType': {
                        'DataType': 'String',
                        'StringValue': 'Transactional'
                    }
                }
            )
            logger.info(f"SMS enviado exitosamente: {response['MessageId']}")
            return True, "SMS enviado exitosamente"
        except ClientError as e:
            error_message = str(e)
            logger.error(f"Error al enviar SMS: {error_message}")
            return False, f"Error al enviar el SMS: {error_message}"

notification_service = NotificationService() 