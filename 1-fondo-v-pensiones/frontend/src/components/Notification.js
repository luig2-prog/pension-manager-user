import React from 'react';
import { Snackbar, Alert } from '@mui/material';
import { useAppContext } from '../contexts/AppContext';

const Notification = () => {
  const { notification, clearNotification } = useAppContext();

  const handleClose = () => {
    clearNotification();
  };

  return (
    <Snackbar
      open={notification.show}
      autoHideDuration={6000}
      onClose={handleClose}
      anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
    >
      <Alert
        onClose={handleClose}
        severity={notification.type}
        sx={{ width: '100%' }}
      >
        {notification.message}
      </Alert>
    </Snackbar>
  );
};

export default Notification; 