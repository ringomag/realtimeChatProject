const chatLog = document.querySelector('#chat-log');
// chatLog.scrollTop = chatLog.scrollHeight;
const roomName = JSON.parse(document.getElementById('room-name').textContent);


const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const userId = data['user_id'];
    const msgSeen = data['message_seen'];
    console.log("ovo je data: ", data); //ovde se vidi izvuceni message.id
    const loggedInUserId = JSON.parse(document.getElementById('user_id').textContent)
    const messageElement = document.createElement('div')
 
    console.log("user id,", userId);
    console.log('loged in user id', loggedInUserId);
    messageElement.innerText = data.message
    messageElement.classList.add('infinite-item');

    if (userId === loggedInUserId){
        messageElement.classList.add('message', 'sender')
    } else {
        messageElement.classList.add('message', 'receiver')
    };
    
    if (messageElement.textContent){
        chatLog.appendChild(messageElement);
        // chatLog.scrollTop = chatLog.scrollHeight;
    }
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

var message_seen=false;
var seen = document.getElementById('mark-as-read');
seen.addEventListener('click', function(e){
    message_seen = true;
})

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    console.log("message seen", message_seen);
    chatSocket.send(JSON.stringify({
        'message': message,
        'message_seen':message_seen
    }));
    messageInputDom.value = '';
    
};

