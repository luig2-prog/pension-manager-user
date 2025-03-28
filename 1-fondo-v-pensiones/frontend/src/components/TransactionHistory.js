import React from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow,
  Chip
} from '@mui/material';
import { useAppContext } from '../contexts/AppContext';

const TransactionHistory = () => {
  const { transactions, formatCurrency } = useAppContext();

  const getTransactionTypeColor = (type) => {
    return type === 'SUBSCRIPTION' ? 'primary' : 'error';
  };

  const getTransactionTypeLabel = (type) => {
    return type === 'SUBSCRIPTION' ? 'Vinculación' : 'Cancelación';
  };

  if (transactions.length === 0) {
    return (
      <Box sx={{ mt: 4, mb: 3 }}>
        <Typography variant="h5" gutterBottom>
          Historial de Transacciones
        </Typography>
        <Paper sx={{ p: 2 }}>
          <Typography variant="body1" color="text.secondary" align="center">
            No hay transacciones para mostrar
          </Typography>
        </Paper>
      </Box>
    );
  }

  return (
    <Box sx={{ mt: 4, mb: 3 }}>
      <Typography variant="h5" gutterBottom sx={{ mb: 2 }}>
        Historial de Transacciones
      </Typography>
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }}>
          <TableHead>
            <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
              <TableCell>Fecha</TableCell>
              <TableCell>Fondo</TableCell>
              <TableCell>Tipo</TableCell>
              <TableCell align="right">Monto</TableCell>
              <TableCell>ID Transacción</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {transactions.map((transaction) => (
              <TableRow key={transaction.id}>
                <TableCell>
                  {new Date(transaction.timestamp).toLocaleString()}
                </TableCell>
                <TableCell>{transaction.fund_name}</TableCell>
                <TableCell>
                  <Chip 
                    label={getTransactionTypeLabel(transaction.type)} 
                    color={getTransactionTypeColor(transaction.type)}
                    size="small"
                  />
                </TableCell>
                <TableCell align="right">
                  {formatCurrency(transaction.amount)}
                </TableCell>
                <TableCell>
                  <Typography variant="body2" sx={{ fontSize: '0.8rem', color: 'text.secondary' }}>
                    {transaction.id}
                  </Typography>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default TransactionHistory; 