const usersData = JSON.parse(document.getElementById("users-data").innerText);
const currentUser = JSON.parse(document.getElementById("current-user").innerText)

let selectedUser = null;

const chatHeader = document.getElementById("chatHeader");
const chatMessages = document.getElementById("chatMessages");
const messageInput = document.getElementById("messageInput");
messageInput.focus();

messageInput.onkeydown =function(e){
    if (e.key === "Enter"){
        sendMessage()
    }
}

function selectUser(user) {
    clearSelectedUser();
    selectedUser = user;

    const userElement = document.querySelector(`.user[data-id="${user.id}"]`);
    if (userElement) {
        userElement.classList.add("selected");
    }

    chatSocket = new WebSocket(
        "ws://" +
        window.location.host +
        "/ws/chat/private/" +
        `${user.id}/`
    )

    chatSocket.onopen = function(event){
        console.log("WebSocket connection established");
    };
    
    chatSocket.onmessage= function(event){
        const data = JSON.parse(event.data)
        if (data.initial != undefined) {
            displayUserMessages(data.messages)
        } else {
            const messageType = data.sender_id===currentUser.id ? "sent" : "received" 
            displayMessage({content: data.message, type: messageType, sender_id: data.sender_id})
        }
    };
    
    chatSocket.onerror = function(event){
        console.error("WebSocket error:", event);
    };
    
    chatSocket.onclose = function(event){
        console.log("WebSocket connection closed:");
    };
    
    updateChatHeader(user);
    messageInput.focus();
}

function clearSelectedUser() {
    if (selectedUser) {
        const selectedUserElement = document.querySelector(".user.selected");
        if (selectedUserElement) {
            selectedUserElement.classList.remove("selected");
        }
    }
}

function updateChatHeader(user) {
    chatHeader.innerHTML = `<h2>${user.username}</h2>`;
}

function displayUserMessages(messages) {
    chatMessages.innerHTML = "";
    messages.forEach(msg=>{
        const messageType = msg.sender_id==currentUser.id ? "sent" : "received"
        const message = {content: msg.content, type: messageType, sender_id: msg.sender_id}
        displayMessage(message)
    })
}

function displayMessage(message) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", message.type);
    messageElement.innerHTML = `<div class="message-content">${message.content}</div>`;
    chatMessages.appendChild(messageElement);

    updateLastMessageInUserList(message);
}

function updateLastMessageInUserList(message) {
    if (selectedUser && message.type === 'received' && selectedUser.id == message.sender_id) {
        const selectedUserElement = document.querySelector(".user.selected");
        if (selectedUserElement) {
            const lastMessageElement = selectedUserElement.querySelector(".last-message");
            lastMessageElement.textContent = `(${message.content})`;
        }
    }

    if (message.type === 'sent') {
        const selectedUserElement = document.querySelector(".user.selected");
        if (selectedUserElement) {
            const lastMessageElement = selectedUserElement.querySelector(".last-message");
            lastMessageElement.textContent = `You: ${message.content}`;
        }
    }
}

function sendMessage() {
    const messageContent = messageInput.value.trim();
    if (messageContent !== "" && selectedUser !== null) {
        const message = { type: "sent", content: messageContent };
        const userIndex = usersData.findIndex(user => user.id === selectedUser.id);

        if (userIndex !== -1) {
            usersData[userIndex].messages.push(message);
        }

        // send message to the web socket
        chatSocket.send(JSON.stringify({
            'message': messageContent,
            "sender_id": currentUser.id,

        }));
        messageInput.value = "";

    }else if(!selectedUser){
        alert("Select a user to send message")
    }
}

