import React from 'react';
import { Container, CssBaseline, Box, Typography, Paper } from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { AppProvider } from './contexts/AppContext';
import Header from './components/Header';
import FundList from './components/FundList';
import UserFundList from './components/UserFundList';
import TransactionHistory from './components/TransactionHistory';
import Notification from './components/Notification';
import LoadingOverlay from './components/LoadingOverlay';

// Create theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppProvider>
        <Header />
        <Container maxWidth="lg" sx={{ py: 4 }}>
          <Box sx={{ mb: 4 }}>
            <Typography variant="h4" component="h1" gutterBottom>
              Plataforma de Gestión de Fondos
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              Administre sus fondos de inversión y pensión voluntaria de manera fácil y eficiente.
            </Typography>
          </Box>
          <FundList />
          <UserFundList />
          <TransactionHistory />
        </Container>
        <Notification />
        <LoadingOverlay />
      </AppProvider>
    </ThemeProvider>
  );
};

export default App; 