import { AppProvider } from './contexts/AppContext';
import { useAppContext } from './contexts/AppContext';
import { FundCard } from './components/FundCard';
import { UserFunds } from './components/UserFunds';
import { TransactionTable } from './components/TransactionTable';
import { Loading } from './components/Loading';
import { Notification } from './components/Notification';

const Dashboard = () => {
  const { availableFunds, userFunds, loading, error, formatCurrency } = useAppContext();

  if (error) {
    return (
      <div className="bg-red-50 border-l-4 border-red-400 p-4 my-4">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <p className="text-sm text-red-700">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {loading && <Loading />}
      <Notification />

      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Fondo de Pensiones</h1>
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-lg text-gray-600">Balance actual</p>
              <p className="text-3xl font-bold text-gray-900">{formatCurrency(userFunds.balance)}</p>
            </div>
            <div>
              <p className="text-lg text-gray-600">Fondos suscritos</p>
              <p className="text-3xl font-bold text-gray-900">{userFunds.subscribed_funds.length}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Mis Fondos</h2>
        <UserFunds />
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Fondos disponibles</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {availableFunds.map((fund) => (
            <FundCard
              key={fund.id}
              fund={fund}
              isSubscribed={userFunds.subscribed_funds.includes(fund.id)}
            />
          ))}
        </div>
      </div>

      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Historial de transacciones</h2>
        <TransactionTable />
      </div>
    </div>
  );
};

function App() {
  return (
    <AppProvider>
      <Dashboard />
    </AppProvider>
  );
}

export default App;
