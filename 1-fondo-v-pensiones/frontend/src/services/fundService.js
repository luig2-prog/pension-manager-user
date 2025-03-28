const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const getFunds = async () => {
    try {
        const response = await fetch(`${API_URL}/api/funds`);
        if (!response.ok) {
            throw new Error('Error al obtener los fondos');
        }
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
};

export const getFundById = async (id) => {
    try {
        const response = await fetch(`${API_URL}/api/funds/${id}`);
        if (!response.ok) {
            throw new Error('Error al obtener el fondo');
        }
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}; 