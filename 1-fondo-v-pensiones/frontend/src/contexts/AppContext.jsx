import { createContext, useContext, useState, useEffect } from 'react';

const AppContext = createContext();

export const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};

export const AppProvider = ({ children }) => {
  const [availableFunds, setAvailableFunds] = useState([]);
  const [userFunds, setUserFunds] = useState({ balance: 500000, subscribed_funds: [] });
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [notification, setNotification] = useState({ show: false, message: '', type: 'success' });

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Fetch available funds
        const fundsResponse = await fetch(`${API_URL}/api/funds`);
        if (!fundsResponse.ok) throw new Error('Error al cargar los fondos');
        const funds = await fundsResponse.json();
        // Transform the data to match our expected format
        const transformedFunds = funds.map(fund => ({
          id: fund.id,
          name: fund.nombre,
          description: `Fondo de ${fund.categoria}`,
          minimum_investment: fund.monto_minimo,
          annual_return: Math.floor(Math.random() * 15) + 5, // Simulated return between 5-20%
          risk_level: fund.categoria === 'FIC' ? 'Alto' : 'Moderado',
          category: fund.categoria
        }));
        setAvailableFunds(transformedFunds);

        // Fetch user funds
        const userFundsResponse = await fetch(`${API_URL}/api/funds/user`);
        if (!userFundsResponse.ok) {
          // Si el endpoint no existe o falla, usamos datos simulados
          setUserFunds({
            balance: 500000,
            subscribed_funds: []
          });
        } else {
          const userData = await userFundsResponse.json();
          setUserFunds({
            balance: userData.balance || 500000,
            subscribed_funds: userData.subscribed_funds || []
          });
        }

        // Fetch transactions
        const transactionsResponse = await fetch(`${API_URL}/api/transactions`);
        if (!transactionsResponse.ok) {
          setTransactions([]);
        } else {
          const transactionData = await transactionsResponse.json();
          setTransactions(Array.isArray(transactionData) ? transactionData : []);
        }
      } catch (err) {
        setError('Error cargando datos iniciales: ' + err.message);
        console.error('Error fetching initial data:', err);
        setTransactions([]);
      } finally {
        setLoading(false);
      }
    };

    fetchInitialData();
  }, [API_URL]);

  const validateSubscription = (fundId) => {
    const fund = availableFunds.find(f => f.id === fundId);
    if (!fund) return { isValid: false, message: 'Fondo no encontrado' };

    if (userFunds.balance < fund.minimum_investment) {
      return {
        isValid: false,
        message: `No tiene saldo disponible para vincularse al fondo ${fund.name}. Saldo actual: ${formatCurrency(userFunds.balance)}, Monto mínimo: ${formatCurrency(fund.minimum_investment)}`
      };
    }

    return { isValid: true };
  };

  const subscribeToFund = async (fundId) => {
    try {
      const validation = validateSubscription(fundId);
      if (!validation.isValid) {
        setNotification({
          show: true,
          message: validation.message,
          type: 'error'
        });
        return;
      }

      setLoading(true);
      const fund = availableFunds.find(f => f.id === fundId);

      const response = await fetch(`${API_URL}/api/funds/subscribe`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ fund_id: fundId }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Error al suscribirse al fondo');
      }

      const result = await response.json();

      // Update local state
      setUserFunds(prev => ({
        balance: prev.balance - fund.minimum_investment,
        subscribed_funds: [...prev.subscribed_funds, fundId]
      }));

      // Add transaction to history
      const newTransaction = {
        id: `SUBSCRIPTION_${Date.now()}`,
        timestamp: new Date().toISOString(),
        type: 'SUBSCRIPTION',
        fund_id: fundId,
        amount: fund.minimum_investment
      };
      setTransactions(prev => [newTransaction, ...prev]);

      setNotification({
        show: true,
        message: result.message || 'Suscripción exitosa',
        type: 'success',
      });

      return result;
    } catch (err) {
      setNotification({
        show: true,
        message: err.message,
        type: 'error',
      });
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const unsubscribeFromFund = async (fundId) => {
    try {
      setLoading(true);
      const fund = availableFunds.find(f => f.id === fundId);

      const response = await fetch(`${API_URL}/api/funds/unsubscribe`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ fund_id: fundId }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Error al cancelar la suscripción');
      }

      const result = await response.json();

      // Update local state
      setUserFunds(prev => ({
        balance: prev.balance + fund.minimum_investment,
        subscribed_funds: prev.subscribed_funds.filter(id => id !== fundId)
      }));

      // Add transaction to history
      const newTransaction = {
        id: `CANCELLATION_${Date.now()}`,
        timestamp: new Date().toISOString(),
        type: 'CANCELLATION',
        fund_id: fundId,
        amount: fund.minimum_investment
      };
      setTransactions(prev => [newTransaction, ...prev]);

      setNotification({
        show: true,
        message: result.message || 'Cancelación exitosa',
        type: 'success',
      });

      return result;
    } catch (err) {
      setNotification({
        show: true,
        message: err.message,
        type: 'error',
      });
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const clearNotification = () => {
    setNotification({ show: false, message: '', type: 'success' });
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP',
      minimumFractionDigits: 0,
    }).format(amount);
  };

  const value = {
    availableFunds,
    userFunds,
    transactions,
    loading,
    error,
    notification,
    subscribeToFund,
    unsubscribeFromFund,
    clearNotification,
    formatCurrency,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}; 