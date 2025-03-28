import { useState } from 'react';
import { useAppContext } from '../contexts/AppContext';
import { NotificationService } from '../services/NotificationService';

export const UserFunds = () => {
  const { availableFunds, userFunds, unsubscribeFromFund, formatCurrency, loading } = useAppContext();
  const [selectedFund, setSelectedFund] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [notificationLoading, setNotificationLoading] = useState(false);
  const [notificationType, setNotificationType] = useState(null);
  const [contactInfo, setContactInfo] = useState('');
  const [validationError, setValidationError] = useState('');

  // Filter available funds to get only the subscribed ones
  const subscribedFunds = availableFunds.filter(fund => 
    userFunds.subscribed_funds.includes(fund.id)
  );

  if (!subscribedFunds.length) {
    return (
      <div className="bg-white rounded-lg shadow p-6 text-center">
        <p className="text-gray-500">No tienes fondos suscritos actualmente.</p>
      </div>
    );
  }

  const handleNotify = (fund) => {
    setSelectedFund(fund);
    setNotificationType(null);
    setContactInfo('');
    setValidationError('');
    setIsModalOpen(true);
  };

  const handleTypeSelect = (type) => {
    setNotificationType(type);
    setContactInfo('');
    setValidationError('');
  };

  const validateContactInfo = () => {
    if (!contactInfo.trim()) {
      setValidationError('Este campo es requerido');
      return false;
    }

    if (notificationType === 'email') {
      if (!NotificationService.validateEmail(contactInfo)) {
        setValidationError('Por favor ingrese un correo electrónico válido');
        return false;
      }
    } else if (notificationType === 'sms') {
      if (!NotificationService.validatePhone(contactInfo)) {
        setValidationError('Por favor ingrese un número de teléfono válido (+57 XXX XXX XXXX)');
        return false;
      }
    }

    setValidationError('');
    return true;
  };

  const handleSendNotification = async () => {
    if (!selectedFund || !notificationType) return;

    if (!validateContactInfo()) return;

    try {
      setNotificationLoading(true);
      const formattedContact = notificationType === 'sms' 
        ? NotificationService.formatPhone(contactInfo)
        : contactInfo.trim();

      await NotificationService.sendNotification(
        selectedFund.id,
        notificationType,
        formattedContact
      );

      alert(`Notificación enviada exitosamente a: ${formattedContact}`);
      setIsModalOpen(false);
    } catch (error) {
      alert(error.message);
    } finally {
      setNotificationLoading(false);
    }
  };

  return (
    <>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {subscribedFunds.map((fund) => (
          <div key={fund.id} className="bg-white rounded-lg shadow-md p-6">
            <div className="mb-4">
              <h3 className="text-xl font-semibold text-gray-900">{fund.name}</h3>
              <p className="text-sm text-gray-500 mt-1">{fund.description}</p>
            </div>

            <div className="space-y-2 mb-6">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Monto invertido:</span>
                <span className="font-medium text-gray-900">
                  {formatCurrency(fund.minimum_investment)}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Fecha de vinculación:</span>
                <span className="font-medium text-gray-900">
                  {new Date().toLocaleDateString('es-CO')}
                </span>
              </div>
            </div>

            <div className="flex gap-2">
              <button
                onClick={() => handleNotify(fund)}
                className="flex-1 bg-blue-100 text-blue-700 hover:bg-blue-200 py-2 px-4 rounded-md font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              >
                Notificar
              </button>
              <button
                onClick={() => unsubscribeFromFund(fund.id)}
                disabled={loading}
                className="flex-1 bg-red-600 text-white hover:bg-red-700 py-2 px-4 rounded-md font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  </div>
                ) : (
                  'Cancelar'
                )}
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Modal de Notificación */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Enviar notificación para {selectedFund?.name}
            </h3>

            {!notificationType ? (
              <>
                <p className="text-sm text-gray-500 mb-6">
                  Selecciona el método de notificación que prefieres:
                </p>
                <div className="space-y-3">
                  <button
                    onClick={() => handleTypeSelect('email')}
                    className="w-full bg-blue-600 text-white hover:bg-blue-700 py-2 px-4 rounded-md font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                  >
                    Correo electrónico
                  </button>
                  <button
                    onClick={() => handleTypeSelect('sms')}
                    className="w-full bg-green-600 text-white hover:bg-green-700 py-2 px-4 rounded-md font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
                  >
                    Mensaje de texto (SMS)
                  </button>
                </div>
              </>
            ) : (
              <>
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {notificationType === 'email' ? 'Correo electrónico' : 'Número de teléfono'}
                  </label>
                  <input
                    type={notificationType === 'email' ? 'email' : 'tel'}
                    value={contactInfo}
                    onChange={(e) => setContactInfo(e.target.value)}
                    placeholder={
                      notificationType === 'email'
                        ? 'ejemplo@correo.com'
                        : '+57 XXX XXX XXXX'
                    }
                    className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 ${
                      validationError
                        ? 'border-red-300 focus:ring-red-500'
                        : 'border-gray-300 focus:ring-blue-500'
                    }`}
                  />
                  {validationError && (
                    <p className="mt-1 text-sm text-red-600">{validationError}</p>
                  )}
                </div>
                <div className="space-y-3">
                  <button
                    onClick={handleSendNotification}
                    disabled={notificationLoading}
                    className="w-full bg-blue-600 text-white hover:bg-blue-700 py-2 px-4 rounded-md font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
                  >
                    {notificationLoading ? 'Enviando...' : 'Enviar notificación'}
                  </button>
                  <button
                    onClick={() => handleTypeSelect(null)}
                    disabled={notificationLoading}
                    className="w-full bg-gray-200 text-gray-800 hover:bg-gray-300 py-2 px-4 rounded-md font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                  >
                    Cambiar método
                  </button>
                </div>
              </>
            )}

            <button
              onClick={() => setIsModalOpen(false)}
              disabled={notificationLoading}
              className="w-full mt-3 bg-gray-200 text-gray-800 hover:bg-gray-300 py-2 px-4 rounded-md font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
            >
              Cancelar
            </button>
          </div>
        </div>
      )}
    </>
  );
}; 