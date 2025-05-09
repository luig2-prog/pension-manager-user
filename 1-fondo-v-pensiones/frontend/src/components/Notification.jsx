import { useEffect } from 'react';
import { useAppContext } from '../contexts/AppContext';

export const Notification = () => {
  const { notification, clearNotification } = useAppContext();

  useEffect(() => {
    if (notification.show) {
      const timer = setTimeout(() => {
        clearNotification();
      }, 5000);

      return () => clearTimeout(timer);
    }
  }, [notification.show, clearNotification]);

  if (!notification.show) return null;

  const baseClasses = "fixed top-4 right-4 p-4 rounded-lg shadow-lg max-w-sm z-50";
  const typeClasses = notification.type === 'error'
    ? "bg-red-100 border border-red-400 text-red-700"
    : "bg-green-100 border border-green-400 text-green-700";

  return (
    <div className={`${baseClasses} ${typeClasses}`}>
      <div className="flex items-center">
        <div className="flex-shrink-0">
          {notification.type === 'error' ? (
            <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          ) : (
            <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
          )}
        </div>
        <div className="ml-3">
          <p className="text-sm font-medium">{notification.message}</p>
        </div>
        <div className="ml-auto pl-3">
          <div className="-mx-1.5 -my-1.5">
            <button
              onClick={clearNotification}
              className={`inline-flex rounded-md p-1.5 focus:outline-none focus:ring-2 focus:ring-offset-2 ${
                notification.type === 'error'
                  ? "text-red-500 hover:bg-red-100 focus:ring-red-600"
                  : "text-green-500 hover:bg-green-100 focus:ring-green-600"
              }`}
            >
              <span className="sr-only">Cerrar</span>
              <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}; 