import React from 'react';
import { useAppContext } from '../contexts/AppContext';
import { Button } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import './FundsTable.css';

const FundsTable = () => {
    const { 
        availableFunds, 
        userFunds, 
        subscribeToFund, 
        formatCurrency, 
        loading 
    } = useAppContext();

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

    if (loading) return <div>Cargando fondos...</div>;

    return (
        <div className="funds-table-container">
            <h2>Fondos Disponibles</h2>
            <table className="funds-table">
                <thead>
                    <tr>
                        <th>Id</th>
                        <th>Nombre</th>
                        <th>Monto mínimo de vinculación</th>
                        <th>Categoría</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {availableFunds.map((fund) => (
                        <tr key={fund.id}>
                            <td>{fund.id}</td>
                            <td>{fund.nombre}</td>
                            <td>{formatCurrency(fund.monto_minimo)}</td>
                            <td>{fund.categoria}</td>
                            <td>
                                <Button
                                    variant="contained"
                                    color="primary"
                                    startIcon={<AddIcon />}
                                    onClick={() => handleSubscribe(fund.id)}
                                    disabled={
                                        loading || 
                                        isSubscribed(fund.id) || 
                                        !hasEnoughBalance(fund.monto_minimo)
                                    }
                                    size="small"
                                >
                                    {isSubscribed(fund.id) 
                                        ? 'Ya Vinculado' 
                                        : !hasEnoughBalance(fund.monto_minimo)
                                            ? 'Saldo Insuficiente'
                                            : 'Vincular'
                                    }
                                </Button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default FundsTable; 