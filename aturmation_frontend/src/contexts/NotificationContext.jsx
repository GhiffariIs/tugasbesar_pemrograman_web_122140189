import { createContext, useContext, useState, useEffect } from 'react';
import { useAuth } from './AuthContext';

const NotificationContext = createContext();

export const useNotifications = () => useContext(NotificationContext);

export const NotificationProvider = ({ children }) => {
  const [notifications, setNotifications] = useState([]);
  const [lowStockItems, setLowStockItems] = useState([]);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (isAuthenticated) {
      // This would be replaced with an actual API call in production
      // fetchLowStockItems();
      
      // For demo purposes, we'll simulate some low stock items
      const demoLowStockItems = [
        { id: 1, name: 'Laptop Asus', currentStock: 2, minStock: 5 },
        { id: 2, name: 'Mouse Wireless', currentStock: 3, minStock: 10 }
      ];
      
      setLowStockItems(demoLowStockItems);
      
      // Generate notifications for low stock items
      const newNotifications = demoLowStockItems.map(item => ({
        id: `low-stock-${item.id}`,
        title: 'Stok Rendah',
        message: `${item.name} memiliki stok rendah (${item.currentStock}/${item.minStock})`,
        type: 'warning',
        read: false,
        timestamp: new Date().toISOString()
      }));
      
      setNotifications(newNotifications);
    }
  }, [isAuthenticated]);

  const addNotification = (notification) => {
    setNotifications(prev => [
      {
        id: Date.now(),
        timestamp: new Date().toISOString(),
        read: false,
        ...notification
      },
      ...prev
    ]);
  };

  const markAsRead = (notificationId) => {
    setNotifications(prev => 
      prev.map(notification => 
        notification.id === notificationId
          ? { ...notification, read: true }
          : notification
      )
    );
  };

  const markAllAsRead = () => {
    setNotifications(prev => 
      prev.map(notification => ({ ...notification, read: true }))
    );
  };

  const removeNotification = (notificationId) => {
    setNotifications(prev => 
      prev.filter(notification => notification.id !== notificationId)
    );
  };

  const unreadCount = notifications.filter(n => !n.read).length;

  return (
    <NotificationContext.Provider value={{
      notifications,
      lowStockItems,
      unreadCount,
      addNotification,
      markAsRead,
      markAllAsRead,
      removeNotification
    }}>
      {children}
    </NotificationContext.Provider>
  );
};

export default NotificationContext;
