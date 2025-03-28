import { useAppContext } from '../contexts/AppContext';

export const FundCard = ({ fund, isSubscribed }) => {
  const { subscribeToFund, unsubscribeFromFund, formatCurrency, loading, userFunds } = useAppContext();

  const handleSubscriptionToggle = async () => {
    try {
      if (isSubscribed) {
        await unsubscribeFromFund(fund.id);
      } else {
        await subscribeToFund(fund.id);
      }
    } catch (error) {
      console.error('Error al cambiar la suscripción:', error);
    }
  };

  const getCategoryBadgeColor = (category) => {
    switch (category) {
      case 'FPV':
        return 'bg-purple-100 text-purple-800';
      case 'FIC':
        return 'bg-orange-100 text-orange-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getRiskLevelBadgeColor = (riskLevel) => {
    switch (riskLevel.toLowerCase()) {
      case 'alto':
        return 'bg-red-100 text-red-800';
      case 'moderado':
        return 'bg-yellow-100 text-yellow-800';
      case 'bajo':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const canSubscribe = !isSubscribed && userFunds.balance >= fund.minimum_investment;

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-200">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-xl font-semibold text-gray-900">{fund.name}</h3>
          <p className="text-sm text-gray-500 mt-1">{fund.description}</p>
        </div>
        <div className="flex gap-2">
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getCategoryBadgeColor(fund.category)}`}>
            {fund.category}
          </span>
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskLevelBadgeColor(fund.risk_level)}`}>
            {fund.risk_level}
          </span>
        </div>
      </div>

      <div className="space-y-2">
        <div className="flex justify-between items-center">
          <span className="text-gray-600">Rendimiento anual:</span>
          <span className="font-medium text-green-600">+{fund.annual_return}%</span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-gray-600">Inversión mínima:</span>
          <span className="font-medium text-gray-900">{formatCurrency(fund.minimum_investment)}</span>
        </div>
        {!isSubscribed && (
          <div className="flex justify-between items-center">
            <span className="text-gray-600">Balance disponible:</span>
            <span className={`font-medium ${canSubscribe ? 'text-green-600' : 'text-red-600'}`}>
              {formatCurrency(userFunds.balance)}
            </span>
          </div>
        )}
      </div>

      <button
        onClick={handleSubscriptionToggle}
        disabled={loading || (!isSubscribed && !canSubscribe)}
        className={`mt-6 w-full py-2 px-4 rounded-md font-medium transition-colors duration-200 ${
          isSubscribed
            ? 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500'
            : canSubscribe
              ? 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500'
              : 'bg-gray-200 text-gray-500 cursor-not-allowed'
        } focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50`}
      >
        {loading ? (
          <div className="flex items-center justify-center">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
          </div>
        ) : isSubscribed ? (
          'Cancelar suscripción'
        ) : canSubscribe ? (
          'Suscribirse'
        ) : (
          'Saldo insuficiente'
        )}
      </button>
    </div>
  );
}; 