import React from 'react';
import { AppBar, Toolbar, Typography, Box } from '@mui/material';
import { useAppContext } from '../contexts/AppContext';
import AccountBalanceWalletIcon from '@mui/icons-material/AccountBalanceWallet';

const Header = () => {
  const { userFunds, formatCurrency } = useAppContext();

  return (
    <AppBar position="static" color="primary">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Fondo Voluntario de Pensión
        </Typography>
        <Box display="flex" alignItems="center">
          <AccountBalanceWalletIcon sx={{ mr: 1 }} />
          <Typography variant="subtitle1">
            Balance: {formatCurrency(userFunds.balance)}
          </Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header; 