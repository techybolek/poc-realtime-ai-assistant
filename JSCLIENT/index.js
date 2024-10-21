import WebSocket from 'ws';

const ws = new WebSocket('ws://localhost:8765'); // Replace with your WebSocket server URL

ws.on('open', () => {
  console.log('Connected to WebSocket server');
});

ws.on('message', (data) => {
  console.log('Received message:', data.toString());
});

ws.on('error', (error) => {
  console.error('WebSocket error:', error);
});

ws.on('close', () => {
  console.log('Disconnected from WebSocket server');
});

