import React, { createContext, useContext, useState, useEffect } from 'react';
import { fundService, transactionService } from '../services/api';

// Create context
const AppContext = createContext();

// Custom hook to use the context
export const useAppContext = () => useContext(AppContext);

// Provider component
export const AppProvider = ({ children }) => {
  // State variables
  const [availableFunds, setAvailableFunds] = useState([]);
  const [userFunds, setUserFunds] = useState({ balance: 0, subscribed_funds: [] });
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [notification, setNotification] = useState({ show: false, message: '', type: 'success' });

  // Load initial data
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Fetch available funds
        const funds = await fundService.getAllFunds();
        setAvailableFunds(funds);
        
        // Fetch user funds and balance
        const userData = await fundService.getUserFunds();
        setUserFunds(userData);
        
        // Fetch transactions
        const transactionData = await transactionService.getTransactions();
        setTransactions(transactionData);
      } catch (err) {
        setError('Error cargando datos iniciales: ' + err.message);
        console.error('Error fetching initial data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchInitialData();
  }, []);

  // Subscribe to a fund
  const subscribeToFund = async (fundId) => {
    try {
      setLoading(true);
      const result = await fundService.subscribeToFund(fundId);
      
      // Refresh user funds and transactions
      const userData = await fundService.getUserFunds();
      setUserFunds(userData);
      
      const transactionData = await transactionService.getTransactions();
      setTransactions(transactionData);
      
      // Show success notification
      setNotification({
        show: true,
        message: result.message,
        type: 'success'
      });
      
      return result;
    } catch (err) {
      setNotification({
        show: true,
        message: err.message,
        type: 'error'
      });
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Unsubscribe from a fund
  const unsubscribeFromFund = async (fundId) => {
    try {
      setLoading(true);
      const result = await fundService.unsubscribeFromFund(fundId);
      
      // Refresh user funds and transactions
      const userData = await fundService.getUserFunds();
      setUserFunds(userData);
      
      const transactionData = await transactionService.getTransactions();
      setTransactions(transactionData);
      
      // Show success notification
      setNotification({
        show: true,
        message: result.message,
        type: 'success'
      });
      
      return result;
    } catch (err) {
      setNotification({
        show: true,
        message: err.message,
        type: 'error'
      });
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Clear notification
  const clearNotification = () => {
    setNotification({ show: false, message: '', type: 'success' });
  };

  // Format currency
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP',
      minimumFractionDigits: 0
    }).format(amount);
  };

  return (
    <AppContext.Provider
      value={{
        availableFunds,
        userFunds,
        transactions,
        loading,
        error,
        notification,
        subscribeToFund,
        unsubscribeFromFund,
        clearNotification,
        formatCurrency
      }}
    >
      {children}
    </AppContext.Provider>
  );
}; 