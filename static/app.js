const socket = io();

socket.on('receive_message', data => {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message';
    msgDiv.innerHTML = `<strong>${data.username}:</strong> ${data.message}`;
    document.getElementById('messages').appendChild(msgDiv);
});

function sendMessage() {
    const username = "{{ session['username'] }}";
    const message = document.getElementById('message').value;
    if (!message.trim()) return;
    socket.emit('send_message', { username, message });
    document.getElementById('message').value = '';
}

document.getElementById("message").addEventListener("keypress", function(e) {
    if (e.key === "Enter") sendMessage();
});
document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("emoji-btn").addEventListener("click", toggleEmoji);

document.getElementById('upload-btn').addEventListener('click', () => {
    document.getElementById('file-upload').click();
});

document.getElementById('file-upload').addEventListener('change', () => {
    const file = document.getElementById('file-upload').files[0];
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    }).then(res => {
        if (res.ok) {
            console.log('Archivo subido');
        }
    });
});
