import React, { useState } from 'react';
import { 
  Box, 
  Typography, 
  Card, 
  CardContent, 
  Button, 
  Grid, 
  Chip,
  Divider,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  FormControlLabel,
  RadioGroup,
  Radio
} from '@mui/material';
import { useAppContext } from '../contexts/AppContext';
import RemoveIcon from '@mui/icons-material/Remove';
import NotificationsIcon from '@mui/icons-material/Notifications';
import { notificationService } from '../services/api';

const UserFundList = () => {
  const { userFunds, unsubscribeFromFund, formatCurrency, loading } = useAppContext();
  const [notificationDialog, setNotificationDialog] = useState({ open: false, fundId: null });
  const [recipient, setRecipient] = useState('');
  const [notificationType, setNotificationType] = useState('email');
  const [notificationSent, setNotificationSent] = useState(false);
  const [notificationError, setNotificationError] = useState('');

  const handleUnsubscribe = async (fundId) => {
    try {
      await unsubscribeFromFund(fundId);
    } catch (error) {
      console.error('Failed to unsubscribe:', error);
    }
  };

  const handleOpenNotificationDialog = (fundId) => {
    setNotificationDialog({ open: true, fundId });
    setNotificationSent(false);
    setNotificationError('');
  };

  const handleCloseNotificationDialog = () => {
    setNotificationDialog({ open: false, fundId: null });
    setRecipient('');
    setNotificationType('email');
  };

  const handleSendNotification = async () => {
    try {
      if (!recipient) {
        setNotificationError('Por favor ingrese un correo o número de teléfono');
        return;
      }

      await notificationService.sendNotification(
        recipient,
        notificationDialog.fundId,
        notificationType
      );
      
      setNotificationSent(true);
      setNotificationError('');
    } catch (error) {
      setNotificationError(error.message || 'Error al enviar la notificación');
    }
  };

  if (userFunds.subscribed_funds.length === 0) {
    return (
      <Box sx={{ mt: 4, mb: 3 }}>
        <Typography variant="h5" gutterBottom>
          Mis Fondos
        </Typography>
        <Card>
          <CardContent>
            <Typography variant="body1" color="text.secondary" align="center">
              No tiene fondos vinculados actualmente
            </Typography>
          </CardContent>
        </Card>
      </Box>
    );
  }

  return (
    <Box sx={{ mt: 4, mb: 3 }}>
      <Typography variant="h5" gutterBottom sx={{ mb: 2 }}>
        Mis Fondos
      </Typography>
      <Grid container spacing={3}>
        {userFunds.subscribed_funds.map((fund) => (
          <Grid item xs={12} sm={6} md={4} key={fund.id}>
            <Card 
              sx={{ 
                height: '100%', 
                display: 'flex', 
                flexDirection: 'column',
                border: '1px solid #3f51b5'
              }}
            >
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography variant="h6" component="div" gutterBottom>
                  {fund.name}
                </Typography>
                <Divider sx={{ mb: 2 }} />
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Monto invertido: {formatCurrency(fund.amount)}
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Fecha de vinculación: {new Date(fund.subscription_date).toLocaleDateString()}
                </Typography>
                <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
                  <Button
                    variant="outlined"
                    color="primary"
                    startIcon={<NotificationsIcon />}
                    onClick={() => handleOpenNotificationDialog(fund.id)}
                    size="small"
                    sx={{ flexGrow: 1 }}
                  >
                    Notificar
                  </Button>
                  <Button
                    variant="contained"
                    color="error"
                    startIcon={<RemoveIcon />}
                    onClick={() => handleUnsubscribe(fund.id)}
                    disabled={loading}
                    size="small"
                    sx={{ flexGrow: 1 }}
                  >
                    Cancelar
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Notification Dialog */}
      <Dialog open={notificationDialog.open} onClose={handleCloseNotificationDialog}>
        <DialogTitle>Enviar Notificación</DialogTitle>
        <DialogContent>
          {notificationSent ? (
            <Typography color="success.main">
              ¡Notificación enviada exitosamente!
            </Typography>
          ) : (
            <>
              <FormControl component="fieldset" sx={{ mb: 2, mt: 1 }}>
                <Typography variant="subtitle2" gutterBottom>
                  Tipo de notificación
                </Typography>
                <RadioGroup
                  row
                  value={notificationType}
                  onChange={(e) => setNotificationType(e.target.value)}
                >
                  <FormControlLabel 
                    value="email" 
                    control={<Radio />} 
                    label="Email" 
                  />
                  <FormControlLabel 
                    value="sms" 
                    control={<Radio />} 
                    label="SMS" 
                  />
                </RadioGroup>
              </FormControl>
              <TextField
                autoFocus
                margin="dense"
                label={notificationType === 'email' ? "Correo Electrónico" : "Número de Teléfono"}
                type={notificationType === 'email' ? "email" : "tel"}
                fullWidth
                variant="outlined"
                value={recipient}
                onChange={(e) => setRecipient(e.target.value)}
                error={!!notificationError}
                helperText={notificationError}
              />
            </>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseNotificationDialog}>
            {notificationSent ? 'Cerrar' : 'Cancelar'}
          </Button>
          {!notificationSent && (
            <Button onClick={handleSendNotification} variant="contained" color="primary">
              Enviar
            </Button>
          )}
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default UserFundList; 