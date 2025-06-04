from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

rooms = {}
online_users = {}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message')
    key = data.get('key')
    username = data.get('username')
    system = data.get('system', False)
    if not message or not key or not username:
        return jsonify({'error': 'Missing message, key or username'}), 400
    if key not in rooms:
        rooms[key] = []
    if key not in online_users:
        online_users[key] = set()
    if system and 'vào phòng' in message:
        online_users[key].add(username)
    elif system and 'rời phòng' in message:
        online_users[key].discard(username)
    elif not system:
        online_users[key].add(username)
    if system:
        rooms[key].append({'user': 'Hệ thống', 'message': message})
    else:
        rooms[key].append({'user': username, 'message': message})
    return jsonify({'message': message})

@app.route('/messages', methods=['POST'])
def get_messages():
    data = request.get_json()
    key = data.get('key')
    if not key:
        return jsonify([])
    return jsonify(rooms.get(key, []))

@app.route('/online', methods=['POST'])
def get_online():
    data = request.get_json()
    key = data.get('key')
    if not key:
        return jsonify([])
    return jsonify(sorted(list(online_users.get(key, set()))))

HTML = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cypher Chat Room</title>
    <style>
        body {
            min-height: 100vh;
            margin: 0;
            padding: 0;
            font-family: 'San Francisco', 'Segoe UI', 'Roboto', Arial, sans-serif;
            color: #234;
            background: linear-gradient(120deg, #e0eafc, #cfdef3, #b5d0ee, #e0eafc, #f7fbff, #e0eafc);
            background-size: 200% 200%;
            animation: gradientBG 18s ease-in-out infinite;
            position: relative;
            overflow-x: hidden;
        }
        @keyframes gradientBG {
            0% {background-position:0% 50%}
            25% {background-position:50% 100%}
            50% {background-position:100% 50%}
            75% {background-position:50% 0%}
            100% {background-position:0% 50%}
        }
        /* Pattern overlay */
        body::before {
            content: "";
            position: fixed;
            inset: 0;
            z-index: 0;
            pointer-events: none;
            opacity: 0.13;
            background: url('https://www.transparenttextures.com/patterns/cubes.png');
            mix-blend-mode: lighten;
        }
        .chat-bg-side {
            position: fixed;
            top: 0; bottom: 0;
            width: 22vw;
            z-index: 1;
            pointer-events: none;
            background: linear-gradient(90deg, #e0eafc 60%, transparent 100%);
            filter: blur(8px) brightness(0.97);
            opacity: 0.7;
        }
        .chat-bg-side.right {
            right: 0;
            background: linear-gradient(270deg, #e0eafc 60%, transparent 100%);
        }
        .chat-bg-side.left {
            left: 0;
        }
        .side-icon {
            position: fixed;
            bottom: 32px;
            left: 32px;
            z-index: 2;
            opacity: 0.10;
            font-size: 110px;
            pointer-events: none;
            user-select: none;
            filter: blur(0.5px);
            text-shadow: 0 4px 24px #b5d0ee;
        }
        .side-icon.right {
            left: unset;
            right: 32px;
            transform: scaleX(-1);
        }
        .container {
            max-width: 540px;
            margin: 56px auto 0 auto;
            background: rgba(255,255,255,0.96);
            border-radius: 32px;
            box-shadow: 0 8px 48px 0 #b5d0ee60, 0 1.5px 0 #fff;
            padding: 0;
            border: 2.5px solid #b5d0ee;
            display: flex;
            flex-direction: column;
            min-height: 82vh;
            animation: fadeInUp 0.7s cubic-bezier(.23,1.01,.32,1) both;
            position: relative;
            z-index: 3;
            backdrop-filter: blur(2px);
        }
        h1 {
            text-align: center;
            color: #2e6da4;
            margin: 0;
            padding: 36px 0 20px 0;
            letter-spacing: 1px;
            font-size: 2.2rem;
            font-family: 'San Francisco', 'Segoe UI', 'Roboto', Arial, sans-serif;
            font-weight: 800;
            border-bottom: 1.5px solid #e0eafc;
            background: #f7fbffcc;
            border-radius: 32px 32px 0 0;
            box-shadow: 0 2px 12px #b5d0ee10;
            text-shadow: 0 2px 8px #b5d0ee30;
        }
        #room-form {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 36px 36px 0 36px;
            animation: fadeIn 1s;
            gap: 8px;
        }
        #room-form label {
            font-weight: 700;
            color: #2e6da4;
            margin-bottom: 8px;
            align-self: flex-start;
            font-size: 1.13rem;
            letter-spacing: 0.2px;
        }
        #room-form input[type="text"] {
            width: 100%;
            padding: 15px 18px;
            margin-bottom: 18px;
            border: 2px solid #b5d0ee;
            border-radius: 16px;
            font-size: 1.13rem;
            background: #f7fbff;
            color: #234;
            outline: none;
            box-shadow: 0 0 12px #b5d0ee20;
            transition: border 0.2s, box-shadow 0.2s;
            font-weight: 500;
        }
        #room-form input[type="text"]:focus {
            border: 2.5px solid #6cb2eb;
            box-shadow: 0 0 20px #b5d0ee60;
            background: #e0eafc;
        }
        #room-form button {
            background: linear-gradient(90deg, #6cb2eb 0%, #b5d0ee 100%);
            color: #234;
            border: none;
            padding: 15px 0;
            width: 100%;
            border-radius: 16px;
            font-size: 1.13rem;
            font-weight: 800;
            cursor: pointer;
            box-shadow: 0 2px 16px #b5d0ee30;
            letter-spacing: 0.7px;
            margin-top: 4px;
            transition: background 0.2s, color 0.2s, box-shadow 0.2s, transform 0.15s;
        }
        #room-form button:hover {
            background: linear-gradient(90deg, #b5d0ee 0%, #6cb2eb 100%);
            color: #2e6da4;
            box-shadow: 0 0 28px #b5d0ee60;
            transform: translateY(-2px) scale(1.04);
        }
        #chat-section {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            animation: fadeInUp 0.7s cubic-bezier(.23,1.01,.32,1) both;
        }
        #online-list {
            background: #f7fbffcc;
            border-radius: 0 0 0 0;
            border-bottom: 1.5px solid #e0eafc;
            padding: 12px 24px 12px 24px;
            font-size: 1.08rem;
            color: #2e6da4;
            min-height: 32px;
            animation: fadeIn 1.2s;
            font-weight: 600;
            letter-spacing: 0.2px;
        }
        #online-list span {
            display: inline-block;
            margin-right: 10px;
            margin-bottom: 2px;
            padding: 4px 14px 4px 12px;
            background: #d0e6fa;
            border-radius: 16px;
            font-weight: 600;
            color: #2e6da4;
            box-shadow: 0 1px 4px #b5d0ee20;
            transition: background 0.2s, color 0.2s;
        }
        #online-list span[style*="background:#6cb2eb"] {
            background: #6cb2eb !important;
            color: #fff !important;
        }
        #chat-box {
            position: relative;
            z-index: 3;
            flex: 1;
            min-height: 120px;
            max-height: 56vh;
            overflow-y: auto;
            background: #f7fbffcc;
            border-radius: 0 0 0 0;
            padding: 28px 16px 18px 16px;
            margin-bottom: 0;
            box-shadow: none;
            border: none;
            display: flex;
            flex-direction: column;
            gap: 12px;
            animation: fadeIn 1.2s;
        }
        .message, .my-message {
            display: flex;
            align-items: flex-end;
            gap: 10px;
            margin: 8px 0;
            border: none;
            background: none;
            box-shadow: none;
        }
        .bubble {
            padding: 13px 20px;
            font-size: 1.09rem;
            border-radius: 22px 22px 22px 8px;
            background: #f1f0f0;
            color: #234;
            max-width: 75%;
            word-break: break-word;
            box-shadow: 0 2px 8px #b5d0ee30;
            position: relative;
            transition: background 0.2s, color 0.2s, box-shadow 0.2s;
            font-weight: 500;
        }
        .my-message .bubble {
            background: linear-gradient(120deg, #6cb2eb 0%, #b5d0ee 100%);
            color: #fff;
            border-radius: 22px 22px 8px 22px;
            margin-left: auto;
            box-shadow: 0 2px 16px #b5d0ee40;
        }
        .avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: linear-gradient(135deg, #b5d0ee 60%, #6cb2eb 100%);
            color: #fff;
            font-weight: bold;
            font-size: 1.18rem;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 8px #b5d0ee30;
            user-select: none;
            border: 2px solid #fff;
            margin-bottom: 2px;
            transition: background 0.2s;
        }
        .my-message .avatar {
            order: 2;
            background: linear-gradient(135deg, #6cb2eb 60%, #b5d0ee 100%);
        }
        .message .avatar {
            order: 1;
        }
        .bubble .sender {
            font-weight: 700;
            color: #6cb2eb;
            margin-right: 8px;
        }
        .system {
            background: #f0f4f8cc;
            color: #6cb2eb;
            font-style: italic;
            border-left: 3px solid #6cb2eb;
            box-shadow: 0 1px 12px #b5d0ee30;
            border-radius: 14px;
            padding-left: 14px;
            max-width: 90%;
            align-self: center;
            margin: 10px auto;
            display: block;
            font-weight: 600;
        }
        .error {
            color: #ff1744;
            background: #ffeaea;
            border-radius: 10px;
            padding: 12px 16px;
            margin: 10px 0;
            font-size: 1.03rem;
            border-left: 3px solid #ff1744;
            box-shadow: 0 1px 12px #ff174440;
        }
        #message-form {
            display: flex;
            gap: 12px;
            padding: 20px 20px 28px 20px;
            background: #fff;
            border-radius: 0 0 32px 32px;
            border-top: 1.5px solid #e0eafc;
            animation: fadeInUp 0.7s;
        }
        #message-input {
            flex: 1;
            padding: 15px;
            border: 2px solid #b5d0ee;
            border-radius: 20px;
            font-size: 1.09rem;
            background: #f7fbff;
            color: #234;
            outline: none;
            box-shadow: 0 0 10px #b5d0ee20;
            transition: border 0.2s, box-shadow 0.2s;
            font-weight: 500;
        }
        #message-input:focus {
            border: 2.5px solid #6cb2eb;
            box-shadow: 0 0 18px #b5d0ee60;
            background: #e0eafc;
        }
        #message-form button {
            background: linear-gradient(90deg, #6cb2eb 0%, #b5d0ee 100%);
            color: #234;
            border: none;
            padding: 0 32px;
            border-radius: 20px;
            font-size: 1.09rem;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 2px 12px #b5d0ee30;
            letter-spacing: 0.6px;
            transition: background 0.2s, color 0.2s, box-shadow 0.2s, transform 0.15s;
        }
        #message-form button:hover {
            background: linear-gradient(90deg, #b5d0ee 0%, #6cb2eb 100%);
            color: #2e6da4;
            box-shadow: 0 0 20px #b5d0ee60;
            transform: translateY(-2px) scale(1.05);
        }
        #leave-btn {
            margin: 0 20px 20px 20px;
            background: linear-gradient(90deg, #ffb347 0%, #6cb2eb 100%);
            color: #234;
            font-weight: 800;
            box-shadow: 0 0 16px #ffb34740;
            border: none;
            border-radius: 20px;
            padding: 14px 0;
            font-size: 1.09rem;
            transition: background 0.2s, color 0.2s, box-shadow 0.2s, transform 0.15s;
        }
        #leave-btn:hover {
            background: linear-gradient(90deg, #6cb2eb 0%, #ffb347 100%);
            color: #2e6da4;
            box-shadow: 0 0 28px #ffb34760;
            transform: translateY(-2px) scale(1.05);
        }
        @media (max-width: 700px) {
            .container { max-width: 100vw; border-radius: 0; min-height: 100vh; }
            h1 { font-size: 1.2rem; border-radius: 0; }
            #chat-box { max-height: 55vh; padding: 10px 2px 10px 2px;}
            #message-input, #message-form button { font-size: 0.98rem; }
            #message-form { border-radius: 0 0 0 0; }
            #room-form { padding: 18px 8px 0 8px; }
            .avatar { width: 30px; height: 30px; font-size: 1rem;}
        }
        @keyframes fadeIn {
            from { opacity: 0;}
            to { opacity: 1;}
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(40px);}
            to { opacity: 1; transform: translateY(0);}
        }
        @keyframes slideInLeft {
            from { opacity: 0; transform: translateX(-40px);}
            to { opacity: 1; transform: translateX(0);}
        }
        @keyframes slideInRight {
            from { opacity: 0; transform: translateX(40px);}
            to { opacity: 1; transform: translateX(0);}
        }
        .side-icon {
            position: fixed;
            bottom: 32px;
            left: 32px;
            z-index: 2;
            opacity: 0.10;
            font-size: 110px;
            pointer-events: none;
            user-select: none;
            filter: blur(0.5px);
            text-shadow: 0 4px 24px #b5d0ee;
        }
        .side-icon.right {
            left: unset;
            right: 32px;
            transform: scaleX(-1);
        }
        body.dark-mode {
            background: linear-gradient(120deg, #23272f, #2a3140, #3a4256, #23272f, #23272f, #23272f);
            color: #f7fbff;
        }
        body.dark-mode .container {
            background: rgba(30,34,40,0.98);
            border-color: #3a4256;
            box-shadow: 0 8px 48px 0 #23272f80, 0 1.5px 0 #23272f;
        }
        body.dark-mode h1 {
            color: #b5d0ee;
            background: #23272fcc;
            border-bottom: 1.5px solid #3a4256;
            text-shadow: 0 2px 8px #23272f60;
        }
        body.dark-mode #room-form input[type="text"],
        body.dark-mode #message-input {
            background: #23272f;
            color: #f7fbff;
            border-color: #3a4256;
        }
        body.dark-mode #room-form input[type="text"]:focus,
        body.dark-mode #message-input:focus {
            border-color: #6cb2eb;
            background: #2a3140;
        }
        body.dark-mode #room-form button,
        body.dark-mode #message-form button,
        body.dark-mode #leave-btn {
            background: linear-gradient(90deg, #3a4256 0%, #6cb2eb 100%);
            color: #f7fbff;
        }
        body.dark-mode #room-form button:hover,
        body.dark-mode #message-form button:hover,
        body.dark-mode #leave-btn:hover {
            background: linear-gradient(90deg, #6cb2eb 0%, #3a4256 100%);
            color: #b5d0ee;
        }
        body.dark-mode #chat-box,
        body.dark-mode #online-list {
            background: #23272fcc;
            color: #b5d0ee;
        }
        body.dark-mode .bubble {
            background: #2a3140;
            color: #f7fbff;
        }
        body.dark-mode .my-message .bubble {
            background: linear-gradient(120deg, #3a4256 0%, #6cb2eb 100%);
            color: #fff;
        }
        body.dark-mode .avatar {
            background: linear-gradient(135deg, #3a4256 60%, #6cb2eb 100%);
            color: #fff;
            border-color: #23272f;
        }
        body.dark-mode .system {
            background: #2a3140cc;
            color: #6cb2eb;
            border-left: 3px solid #6cb2eb;
        }
        body.dark-mode .error {
            background: #3a4256;
            color: #ffb347;
            border-left: 3px solid #ffb347;
        }
    </style>
    <link href="https://fonts.googleapis.com/css?family=Roboto:400,700&display=swap" rel="stylesheet">
</head>
<body>
    <div class="chat-bg-side left"></div>
    <div class="chat-bg-side right"></div>
    <div class="side-icon">💬</div>
    <div class="side-icon right">💬</div>
    <div class="container">
        <h1>Cypher Chat Room</h1>
        <form id="room-form">
            <label for="username">Tên của bạn:</label>
            <input type="text" id="username" placeholder="Nhập tên..." required>
            <label for="room_key">Nhập mã Cypher/phòng:</label>
            <input type="text" id="room_key" placeholder="Nhập mã Cypher/phòng..." required>
            <button type="submit">Vào phòng</button>
        </form>
        <div id="chat-section" style="display:none;flex:1;flex-direction:column;">
            <div id="online-list"></div>
            <div id="chat-box"></div>
            <form id="message-form" autocomplete="off">
                <input type="text" id="message-input" placeholder="Nhập tin nhắn..." required autocomplete="off">
                <button type="submit">Gửi</button>
            </form>
            <button id="leave-btn">Rời phòng</button>
        </div>
    </div>
    <button id="toggle-theme" style="position:absolute;top:18px;right:24px;border-radius:16px;padding:8px 18px;font-weight:700;cursor:pointer;">🌙 Đổi giao diện</button>
    <script>
        let roomKey = '';
        let username = '';

        document.getElementById('room-form').addEventListener('submit', function(e) {
            e.preventDefault();
            roomKey = document.getElementById('room_key').value;
            username = document.getElementById('username').value;
            if (roomKey && username) {
                document.getElementById('chat-section').style.display = 'flex';
                document.getElementById('room-form').style.display = 'none';
                fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: username + ' đã vào phòng', key: roomKey, username: username, system: true })
                }).then(() => {
                    loadMessages();
                    loadOnline();
                    window.msgInterval = setInterval(() => {
                        loadMessages();
                        loadOnline();
                    }, 1500);
                });
            }
        });

        document.getElementById('leave-btn').addEventListener('click', function() {
            if (roomKey && username) {
                fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: username + ' đã rời phòng', key: roomKey, username: username, system: true })
                }).then(() => {
                    clearInterval(window.msgInterval);
                    document.getElementById('chat-section').style.display = 'none';
                    document.getElementById('room-form').style.display = 'flex';
                    document.getElementById('room_key').value = '';
                    document.getElementById('username').value = '';
                    document.getElementById('chat-box').innerHTML = '';
                    document.getElementById('online-list').innerHTML = '';
                    roomKey = '';
                    username = '';
                });
            }
        });

        document.getElementById('message-form').addEventListener('submit', function(e) {
            e.preventDefault();
            const messageInput = document.getElementById('message-input');
            const message = messageInput.value;
            fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message, key: roomKey, username: username })
            })
            .then(response => response.json())
            .then(data => {
                messageInput.value = '';
                loadMessages();
            });
        });

        window.addEventListener('beforeunload', function() {
            if (roomKey && username) {
                navigator.sendBeacon('/chat', JSON.stringify({
                    message: username + ' đã rời phòng',
                    key: roomKey,
                    username: username,
                    system: true
                }));
            }
        });

        function getAvatar(name) {
            if (!name) return "👤";
            return `<span class="avatar">${name.trim().charAt(0).toUpperCase()}</span>`;
        }
        function loadMessages() {
            fetch('/messages', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ key: roomKey })
            })
            .then(response => response.json())
            .then(data => {
                const chatBox = document.getElementById('chat-box');
                chatBox.innerHTML = '';
                data.forEach(msg => {
                    if (msg.user === 'Hệ thống') {
                        const msgDiv = document.createElement('div');
                        msgDiv.className = 'system';
                        msgDiv.textContent = msg.message;
                        chatBox.appendChild(msgDiv);
                    } else if (msg.user === username) {
                        const msgDiv = document.createElement('div');
                        msgDiv.className = 'my-message';
                        msgDiv.innerHTML = `
                            <div class="bubble">${msg.message}</div>
                            ${getAvatar(msg.user)}
                        `;
                        chatBox.appendChild(msgDiv);
                    } else {
                        const msgDiv = document.createElement('div');
                        msgDiv.className = 'message';
                        msgDiv.innerHTML = `
                            ${getAvatar(msg.user)}
                            <div class="bubble"><span class="sender">${msg.user}</span> ${msg.message}</div>
                        `;
                        chatBox.appendChild(msgDiv);
                    }
                });
                chatBox.scrollTop = chatBox.scrollHeight;
            });
        }

        function loadOnline() {
            fetch('/online', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ key: roomKey })
            })
            .then(response => response.json())
            .then(data => {
                const onlineList = document.getElementById('online-list');
                if (data.length === 0) {
                    onlineList.innerHTML = '<i>Không ai online</i>';
                } else {
                    onlineList.innerHTML = '<b>Đang online:</b> ' + data.map(name => 
                        `<span${name === username ? ' style="background:#6cb2eb;color:#fff;"' : ''}>${name === username ? 'Bạn' : name}</span>`
                    ).join('');
                }
            });
        }

        document.getElementById('toggle-theme').addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            this.textContent = document.body.classList.contains('dark-mode') ? '☀️ Đổi giao diện' : '🌙 Đổi giao diện';
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)