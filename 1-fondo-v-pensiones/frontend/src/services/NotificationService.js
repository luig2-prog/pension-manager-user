const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const NotificationService = {
  async sendNotification(fundId, type, contactInfo) {
    try {
      const response = await fetch(`${API_URL}/api/notifications/send`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          fund_id: fundId,
          notification_type: type,
          contact_info: contactInfo
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Error al enviar la notificación');
      }

      const result = await response.json();
      return result;
    } catch (error) {
      throw new Error(`Error al enviar la notificación: ${error.message}`);
    }
  },

  validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  },

  validatePhone(phone) {
    // Formato colombiano: +57 XXX XXX XXXX o XXX XXX XXXX
    const phoneRegex = /^(\+57\s?)?[0-9]{3}\s?[0-9]{3}\s?[0-9]{4}$/;
    return phoneRegex.test(phone);
  },

  formatPhone(phone) {
    // Elimina todos los espacios y el prefijo +57 si existe
    const cleaned = phone.replace(/\s+/g, '').replace(/^\+57/, '');
    // Asegura que el número tenga el prefijo +57
    return `+57${cleaned}`;
  }
}; 