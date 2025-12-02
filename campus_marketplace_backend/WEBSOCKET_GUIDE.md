# WebSocket Connection Guide

## Overview
This guide explains how to connect to the WebSocket endpoint for real-time messaging.

## Authentication
WebSocket connections require JWT authentication via query parameters.

## Connection URL Format
```
ws://localhost:8001/ws/chat/{conversation_id}/?token={jwt_access_token}
```

### Parameters:
- `conversation_id`: UUID of the conversation
- `token`: JWT access token (from login response)

## Frontend Example (JavaScript)

```javascript
// Get the access token from your auth context/storage
const accessToken = localStorage.getItem('access_token');
const conversationId = 'your-conversation-uuid';

// Create WebSocket connection
const ws = new WebSocket(
  `ws://localhost:8001/ws/chat/${conversationId}/?token=${accessToken}`
);

// Connection opened
ws.onopen = (event) => {
  console.log('WebSocket connected');
};

// Listen for messages
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received message:', data);
  // data contains: { message, sender_id, sender_username, created_at, id }
};

// Send a message
function sendMessage(messageText) {
  ws.send(JSON.stringify({
    message: messageText
  }));
}

// Handle errors
ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

// Connection closed
ws.onclose = (event) => {
  console.log('WebSocket disconnected');
};
```

## React Example with useEffect

```javascript
import { useEffect, useState, useRef } from 'react';

function ChatComponent({ conversationId, accessToken }) {
  const [messages, setMessages] = useState([]);
  const wsRef = useRef(null);

  useEffect(() => {
    // Create WebSocket connection
    const ws = new WebSocket(
      `ws://localhost:8001/ws/chat/${conversationId}/?token=${accessToken}`
    );

    ws.onopen = () => {
      console.log('Connected to chat');
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMessages(prev => [...prev, data]);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.onclose = () => {
      console.log('Disconnected from chat');
    };

    wsRef.current = ws;

    // Cleanup on unmount
    return () => {
      ws.close();
    };
  }, [conversationId, accessToken]);

  const sendMessage = (messageText) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        message: messageText
      }));
    }
  };

  return (
    // Your chat UI here
    <div>
      {messages.map((msg, idx) => (
        <div key={idx}>
          <strong>{msg.sender_username}:</strong> {msg.message}
        </div>
      ))}
    </div>
  );
}
```

## Message Format

### Sending Messages
```json
{
  "message": "Your message text here"
}
```

### Receiving Messages
```json
{
  "message": "The message text",
  "sender_id": "uuid-of-sender",
  "sender_username": "sender's username",
  "created_at": "2024-01-01T12:00:00Z",
  "id": "uuid-of-message"
}
```

## Troubleshooting

### Common Issues:

1. **Connection refused**: Make sure the backend server is running
2. **401 Unauthorized**: Check that your JWT token is valid and not expired
3. **403 Forbidden**: Verify you're a participant in the conversation
4. **CORS errors**: Ensure `localhost:3000` is in `CORS_ALLOWED_ORIGINS`

### Debugging:
- Check browser console for WebSocket errors
- Verify the token is being sent correctly in the URL
- Ensure the conversation_id exists and you're a participant
- Check backend logs for connection attempts

## Production Deployment

For production, change the WebSocket URL to use WSS (secure):
```javascript
const ws = new WebSocket(
  `wss://yourdomain.com/ws/chat/${conversationId}/?token=${accessToken}`
);
```
