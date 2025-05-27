import {
  Drawer,
  Box,
  Typography,
  List,
  ListItem,
  ListItemText,
  IconButton,
  Divider,
  Badge,
  Button,
  Tooltip
} from '@mui/material';
import { 
  Close as CloseIcon, 
  Delete as DeleteIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
  CheckCircleOutline as SuccessIcon
} from '@mui/icons-material';
import { useNotifications } from '../../contexts/NotificationContext';
import { formatDateTime } from '../../utils/formatters';

const NotificationPanel = ({ open, onClose }) => {
  const { 
    notifications, 
    markAsRead, 
    markAllAsRead, 
    removeNotification
  } = useNotifications();

  const getIconByType = (type) => {
    switch(type) {
      case 'warning': return <WarningIcon color="warning" />;
      case 'error': return <ErrorIcon color="error" />;
      case 'success': return <SuccessIcon color="success" />;
      default: return <InfoIcon color="primary" />;
    }
  };

  const handleNotificationClick = (notification) => {
    if (!notification.read) {
      markAsRead(notification.id);
    }
  };

  return (
    <Drawer
      anchor="right"
      open={open}
      onClose={onClose}
      PaperProps={{
        sx: { width: { xs: '100%', sm: 400 } }
      }}
    >
      <Box sx={{ p: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h6">Notifikasi</Typography>
        <Box>
          <Button
            size="small"
            onClick={markAllAsRead}
            sx={{ mr: 1 }}
          >
            Tandai semua dibaca
          </Button>
          <IconButton onClick={onClose} edge="end">
            <CloseIcon />
          </IconButton>
        </Box>
      </Box>
      <Divider />

      <List sx={{ p: 0, overflow: 'auto', maxHeight: 'calc(100vh - 120px)' }}>
        {notifications.length > 0 ? notifications.map((notification) => (
          <Box key={notification.id}>
            <ListItem
              alignItems="flex-start"
              onClick={() => handleNotificationClick(notification)}
              sx={{
                bgcolor: notification.read ? 'inherit' : 'action.hover',
                cursor: 'pointer',
                '&:hover': {
                  bgcolor: 'action.selected',
                },
              }}
              secondaryAction={
                <Tooltip title="Hapus notifikasi">
                  <IconButton 
                    edge="end" 
                    aria-label="delete"
                    onClick={(e) => {
                      e.stopPropagation();
                      removeNotification(notification.id);
                    }}
                  >
                    <DeleteIcon />
                  </IconButton>
                </Tooltip>
              }
            >
              <Badge
                color="primary"
                variant="dot"
                invisible={notification.read}
                sx={{ mr: 2, mt: 1 }}
              >
                {getIconByType(notification.type)}
              </Badge>
              <ListItemText
                primary={notification.title}
                secondary={
                  <>
                    <Typography
                      component="span"
                      variant="body2"
                      color="text.primary"
                      sx={{ display: 'block' }}
                    >
                      {notification.message}
                    </Typography>
                    <Typography
                      component="span"
                      variant="caption"
                      color="text.secondary"
                    >
                      {formatDateTime(notification.timestamp)}
                    </Typography>
                  </>
                }
              />
            </ListItem>
            <Divider component="li" />
          </Box>
        )) : (
          <Box p={3} textAlign="center">
            <Typography color="text.secondary">
              Tidak ada notifikasi
            </Typography>
          </Box>
        )}
      </List>
    </Drawer>
  );
};

export default NotificationPanel;
