import React from 'react';
import { Backdrop, CircularProgress } from '@mui/material';
import { useAppContext } from '../contexts/AppContext';

const LoadingOverlay = () => {
  const { loading } = useAppContext();

  return (
    <Backdrop
      sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
      open={loading}
    >
      <CircularProgress color="inherit" />
    </Backdrop>
  );
};

export default LoadingOverlay; 