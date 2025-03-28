import boto3
import os
from typing import Dict, Any

# Configure AWS clients
sns = boto3.client(
    'sns',
    region_name=os.environ.get('AWS_REGION', 'us-east-1'),
    endpoint_url=os.environ.get('SNS_ENDPOINT', None)
)

ses = boto3.client(
    'ses',
    region_name=os.environ.get('AWS_REGION', 'us-east-1'),
    endpoint_url=os.environ.get('SES_ENDPOINT', None)
)

class NotificationModel:
    @staticmethod
    async def send_notification(
        recipient: str, 
        message: str, 
        subject: str, 
        notification_type: str = "email"
    ) -> Dict[str, Any]:
        """Send a notification via email or SMS"""
        try:
            if notification_type.lower() == "email":
                return await NotificationModel.send_email(recipient, message, subject)
            elif notification_type.lower() == "sms":
                return await NotificationModel.send_sms(recipient, message)
            else:
                return {"success": False, "message": "Invalid notification type"}
        except Exception as e:
            print(f"Error sending notification: {str(e)}")
            return {"success": False, "message": str(e)}
    
    @staticmethod
    async def send_email(recipient: str, message: str, subject: str) -> Dict[str, Any]:
        """Send an email notification"""
        try:
            response = ses.send_email(
                Source=os.environ.get('EMAIL_SENDER', 'noreply@example.com'),
                Destination={
                    'ToAddresses': [recipient]
                },
                Message={
                    'Subject': {'Data': subject},
                    'Body': {
                        'Text': {'Data': message},
                        'Html': {'Data': f"<html><body><p>{message}</p></body></html>"}
                    }
                }
            )
            return {
                "success": True, 
                "message": "Email sent successfully", 
                "message_id": response.get('MessageId')
            }
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return {"success": False, "message": str(e)}
    
    @staticmethod
    async def send_sms(phone_number: str, message: str) -> Dict[str, Any]:
        """Send an SMS notification"""
        try:
            response = sns.publish(
                PhoneNumber=phone_number,
                Message=message,
                MessageAttributes={
                    'AWS.SNS.SMS.SenderID': {
                        'DataType': 'String',
                        'StringValue': 'FONDOSAPP'
                    },
                    'AWS.SNS.SMS.SMSType': {
                        'DataType': 'String',
                        'StringValue': 'Transactional'
                    }
                }
            )
            return {
                "success": True, 
                "message": "SMS sent successfully", 
                "message_id": response.get('MessageId')
            }
        except Exception as e:
            print(f"Error sending SMS: {str(e)}")
            return {"success": False, "message": str(e)} 