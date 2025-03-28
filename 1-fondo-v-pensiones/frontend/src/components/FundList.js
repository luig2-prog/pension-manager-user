import React from 'react';
import { 
  Box, 
  Typography, 
  Card, 
  CardContent, 
  Button, 
  Grid, 
  Chip,
  Divider
} from '@mui/material';
import { useAppContext } from '../contexts/AppContext';
import AddIcon from '@mui/icons-material/Add';

const FundList = () => {
  const { availableFunds, userFunds, subscribeToFund, formatCurrency, loading } = useAppContext();

  // Check if fund is already subscribed
  const isSubscribed = (fundId) => {
    return userFunds.subscribed_funds.some(fund => fund.id === fundId);
  };

  // Check if user has enough balance for the fund
  const hasEnoughBalance = (minAmount) => {
    return userFunds.balance >= minAmount;
  };

  const handleSubscribe = async (fundId) => {
    try {
      await subscribeToFund(fundId);
    } catch (error) {
      console.error('Failed to subscribe:', error);
    }
  };

  return (
    <Box sx={{ mt: 3, mb: 4 }}>
      <Typography variant="h5" gutterBottom sx={{ mb: 2 }}>
        Fondos Disponibles
      </Typography>
      <Grid container spacing={3}>
        {availableFunds.map((fund) => (
          <Grid item xs={12} sm={6} md={4} key={fund.id}>
            <Card 
              sx={{ 
                height: '100%', 
                display: 'flex', 
                flexDirection: 'column',
                borderLeft: fund.category === 'FPV' ? '4px solid #3f51b5' : '4px solid #f50057'
              }}
            >
              <CardContent sx={{ flexGrow: 1 }}>
                <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={1}>
                  <Typography variant="h6" component="div" gutterBottom>
                    {fund.name}
                  </Typography>
                  <Chip 
                    label={fund.category} 
                    color={fund.category === 'FPV' ? 'primary' : 'secondary'} 
                    size="small" 
                  />
                </Box>
                <Divider sx={{ mb: 2 }} />
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Monto mínimo: {formatCurrency(fund.min_amount)}
                </Typography>
                <Box sx={{ mt: 2 }}>
                  <Button
                    variant="contained"
                    color="primary"
                    startIcon={<AddIcon />}
                    onClick={() => handleSubscribe(fund.id)}
                    disabled={
                      loading || 
                      isSubscribed(fund.id) || 
                      !hasEnoughBalance(fund.min_amount)
                    }
                    fullWidth
                  >
                    {isSubscribed(fund.id) 
                      ? 'Ya Vinculado' 
                      : !hasEnoughBalance(fund.min_amount)
                        ? 'Saldo Insuficiente'
                        : 'Vincular'
                    }
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default FundList; 