import axios from 'axios';

// Set base URL based on environment
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Fund services
export const fundService = {
  // Get all available funds
  getAllFunds: async () => {
    try {
      const response = await api.get('/api/funds/');
      return response.data;
    } catch (error) {
      console.error('Error fetching funds:', error);
      throw error;
    }
  },

  // Get user funds and balance
  getUserFunds: async () => {
    try {
      const response = await api.get('/api/funds/user');
      return response.data;
    } catch (error) {
      console.error('Error fetching user funds:', error);
      throw error;
    }
  },

  // Subscribe to a fund
  subscribeToFund: async (fundId) => {
    try {
      const response = await api.post('/api/funds/subscribe', { fund_id: fundId });
      return response.data;
    } catch (error) {
      console.error('Error subscribing to fund:', error);
      if (error.response) {
        throw new Error(error.response.data.detail || 'Error al subscribirse al fondo');
      }
      throw error;
    }
  },

  // Unsubscribe from a fund
  unsubscribeFromFund: async (fundId) => {
    try {
      const response = await api.post('/api/funds/unsubscribe', { fund_id: fundId });
      return response.data;
    } catch (error) {
      console.error('Error unsubscribing from fund:', error);
      if (error.response) {
        throw new Error(error.response.data.detail || 'Error al desvincular del fondo');
      }
      throw error;
    }
  }
};

// Transaction services
export const transactionService = {
  // Get all transactions
  getTransactions: async () => {
    try {
      const response = await api.get('/api/transactions/');
      return response.data;
    } catch (error) {
      console.error('Error fetching transactions:', error);
      throw error;
    }
  }
};

// Notification services
export const notificationService = {
  // Send a notification
  sendNotification: async (recipient, fundId, notificationType = 'email') => {
    try {
      const response = await api.post('/api/notifications/', {
        recipient,
        fund_id: fundId,
        notification_type: notificationType
      });
      return response.data;
    } catch (error) {
      console.error('Error sending notification:', error);
      if (error.response) {
        throw new Error(error.response.data.detail || 'Error al enviar la notificación');
      }
      throw error;
    }
  }
}; 