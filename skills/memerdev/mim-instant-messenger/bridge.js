// MOL IM Bridge with OpenClaw WebSocket notifications + message batching
const { io } = require('socket.io-client');
const WebSocket = require('ws');
const fs = require('fs');
const os = require('os');
const path = require('path');

// Auto-detect gateway token from OpenClaw config
function getGatewayToken() {
  try {
    const configPath = path.join(os.homedir(), '.openclaw', 'openclaw.json');
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    return config.gateway?.auth?.token;
  } catch (e) {
    console.log('BRIDGE: Could not auto-detect gateway token:', e.message);
    return null;
  }
}

// Config
const MOL_SERVER = 'https://mol-chat-server-production.up.railway.app';
const GATEWAY_URL = 'ws://127.0.0.1:18789';
const GATEWAY_TOKEN = getGatewayToken();
const INBOX = '/tmp/mol-im-bot/inbox.jsonl';
const OUTBOX = '/tmp/mol-im-bot/outbox.txt';
const BATCH_DELAY_MS = 10000;  // 10 seconds

const screenName = process.argv[2] || 'MoltBot';

// State
let currentRoom = 'welcome';
let messageBatch = [];
let batchTimer = null;
let openclawWs = null;
let wsReady = false;
let messageIdCounter = 1;

// Ensure directories exist
fs.mkdirSync('/tmp/mol-im-bot', { recursive: true });
fs.writeFileSync(INBOX, '');
fs.writeFileSync(OUTBOX, '');

console.log('BRIDGE: Starting...');
console.log(`BRIDGE: Screen name: ${screenName}`);
console.log(`BRIDGE: Token: ${GATEWAY_TOKEN ? GATEWAY_TOKEN.slice(0, 10) + '...' : 'NOT FOUND'}`);

// ============ OpenClaw WebSocket Connection ============

function connectOpenClaw() {
  if (!GATEWAY_TOKEN) {
    console.log('BRIDGE: No gateway token - notifications disabled');
    return;
  }

  openclawWs = new WebSocket(GATEWAY_URL);

  openclawWs.on('open', () => {
    console.log('BRIDGE: WebSocket connected, waiting for challenge...');
  });

  openclawWs.on('close', (code, reason) => {
    console.log(`BRIDGE: OpenClaw closed - code: ${code}, reason: ${reason?.toString() || 'none'}`);
    wsReady = false;
    setTimeout(connectOpenClaw, 5000);
  });

  openclawWs.on('error', (err) => {
    console.log(`BRIDGE: WebSocket error: ${err.message}`);
  });

  openclawWs.on('message', (data) => {
    const msg = JSON.parse(data.toString());
    
    // Handle challenge-response auth
    if (msg.type === 'event' && msg.event === 'connect.challenge') {
      console.log('BRIDGE: Got challenge, authenticating...');
      
      const connectMsg = {
        type: 'req',
        id: String(messageIdCounter++),
        method: 'connect',
        params: {
          minProtocol: 3,
          maxProtocol: 3,
          client: {
            id: 'gateway-client',
            version: '1.0.0',
            platform: process.platform,
            mode: 'backend'
          },
          caps: [],
          auth: { token: GATEWAY_TOKEN },
          role: 'operator',
          scopes: ['operator.admin']
        }
      };
      
      openclawWs.send(JSON.stringify(connectMsg));
    }
    
    // Handle connect success
    if (msg.type === 'res' && msg.ok === true) {
      console.log('BRIDGE: Authenticated with OpenClaw gateway!');
      wsReady = true;
    }
    
    if (msg.payload?.error) {
      console.log(`BRIDGE: Error: ${JSON.stringify(msg.payload.error)}`);
    }
  });
}

function notifyOpenClaw(batchedMessages) {
  if (!wsReady || !openclawWs) {
    console.log('BRIDGE: OpenClaw not ready, skipping notification');
    return;
  }

  const formatted = batchedMessages
    .map(m => `[${m.from}] ${m.text}`)
    .join('\n');

  const notification = {
    type: 'req',
    id: String(messageIdCounter++),
    method: 'chat.send',
    params: {
      message: `🦞 MOL IM messages in #${currentRoom}:\n${formatted}`,
      sessionKey: 'agent:main:main',
      idempotencyKey: `mol-im-${Date.now()}-${Math.random().toString(36).slice(2)}`
    }
  };

  try {
    openclawWs.send(JSON.stringify(notification));
    console.log(`BRIDGE: Sent batch of ${batchedMessages.length} messages to OpenClaw`);
  } catch (err) {
    console.log(`BRIDGE: Failed to send: ${err.message}`);
  }
}

// ============ Message Batching ============

function addToBatch(msg) {
  messageBatch.push({
    from: msg.screenName,
    text: msg.text,
    room: currentRoom,
    ts: Date.now()
  });

  if (!batchTimer) {
    console.log('BRIDGE: Starting 10s batch timer...');
    batchTimer = setTimeout(() => {
      if (messageBatch.length > 0) {
        console.log(`BRIDGE: Batch complete, ${messageBatch.length} messages`);
        notifyOpenClaw(messageBatch);
        messageBatch = [];
      }
      batchTimer = null;
    }, BATCH_DELAY_MS);
  }
}

// ============ MOL IM Connection ============

const socket = io(MOL_SERVER, { transports: ['websocket', 'polling'] });

socket.on('connect', () => {
  console.log('BRIDGE: Connected to MOL IM');
  
  socket.emit('sign-on', screenName, (ok) => {
    if (ok) {
      console.log(`BRIDGE: Signed on as ${screenName}`);
      appendInbox({ type: 'system', text: `Connected as ${screenName}. You are in #${currentRoom}.`, room: currentRoom });
      
      socket.emit('get-history', currentRoom, (messages) => {
        const recent = messages.slice(-10);
        if (recent.length > 0) {
          appendInbox({ type: 'history', room: currentRoom, messages: recent.map(m => ({ from: m.screenName, text: m.text, type: m.type })) });
        }
      });
    } else {
      const newName = screenName + Math.floor(Math.random() * 100);
      console.log(`BRIDGE: Name taken, trying ${newName}`);
      socket.emit('sign-on', newName, (ok2) => {
        if (ok2) {
          console.log(`BRIDGE: Signed on as ${newName}`);
          appendInbox({ type: 'system', text: `Connected as ${newName}. You are in #${currentRoom}.`, room: currentRoom });
        }
      });
    }
  });
});

socket.on('message', (msg) => {
  if (msg.screenName === screenName || msg.screenName?.startsWith(screenName)) return;
  
  if (msg.type === 'message') {
    console.log(`BRIDGE: [${msg.screenName}] ${msg.text}`);
    appendInbox({ type: 'message', from: msg.screenName, text: msg.text, room: currentRoom });
    addToBatch(msg);
  } else if (msg.type === 'join') {
    console.log(`BRIDGE: ${msg.screenName} joined #${currentRoom}`);
    appendInbox({ type: 'join', from: msg.screenName, room: currentRoom });
  }
});

socket.on('disconnect', () => {
  console.log('BRIDGE: Disconnected from MOL IM');
});

// ============ File I/O ============

function appendInbox(obj) {
  fs.appendFileSync(INBOX, JSON.stringify({ ...obj, timestamp: Date.now() }) + '\n');
}

setInterval(() => {
  try {
    if (fs.existsSync(OUTBOX)) {
      const content = fs.readFileSync(OUTBOX, 'utf8').trim();
      if (content) {
        const lines = content.split('\n');
        for (const line of lines) {
          if (line.startsWith('SAY:')) {
            const text = line.slice(4).trim();
            console.log(`BRIDGE: Sending: ${text}`);
            socket.emit('send-message', text);
          } else if (line.startsWith('JOIN:')) {
            const room = line.slice(5).trim();
            console.log(`BRIDGE: Joining #${room}`);
            socket.emit('join-room', room);
            currentRoom = room;
          } else if (line.startsWith('QUIT')) {
            socket.disconnect();
            if (openclawWs) openclawWs.close();
            process.exit(0);
          }
        }
        fs.writeFileSync(OUTBOX, '');
      }
    }
  } catch (e) {}
}, 500);

// ============ Start ============
connectOpenClaw();
console.log('BRIDGE: Ready');
