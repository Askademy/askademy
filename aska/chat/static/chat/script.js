const users = [
    { id: 1, name: "User 1", status: "online" },
    { id: 2, name: "User 2", status: "offline" },
    { id: 3, name: "User 3", status: "online" }
    // Add more users as needed
];

const userPanel = document.getElementById("userPanel");
const chatHeader = document.getElementById("chatHeader");
const chatMessages = document.getElementById("chatMessages");
const messageInput = document.getElementById("messageInput");
let selectedUser = null;

// Messages for each user
const userMessages = {};

users.forEach(user => {
    addUserToPanel(user);
    userMessages[user.id] = [];
});

function addUserToPanel(user) {
    const userElement = document.createElement("div");
    userElement.classList.add("user");

    // Ensure that the messages array is initialized
    if (!userMessages[user.id]) {
        userMessages[user.id] = [];
    }

    userElement.innerHTML = `
        <img src="https://via.placeholder.com/40" alt="${user.name}">
        <div class="user-info">
            <h4>${user.name}</h4>
            <p class="last-message">${getLastMessage(user)}</p>
        </div>
        <div class="status ${user.status === 'online' ? 'online' : 'offline'}"></div>
    `;
    userElement.addEventListener("click", () => {
        selectUser(user);
    });
    userPanel.appendChild(userElement);
}

function getLastMessage(user) {
    const messages = userMessages[user.id] || [];
    if (messages.length > 0) {
        const lastMessage = messages[messages.length - 1];
        return `${lastMessage.type === 'sent' ? 'You: ' : user.name + ': '}${lastMessage.content}`;
    } else {
        return "No messages yet";
    }
}

function selectUser(user) {
    if (selectedUser) {
        const selectedUserElement = document.querySelector(".user.selected");
        selectedUserElement.classList.remove("selected");
    }

    selectedUser = user;

    const users = document.querySelectorAll(".user");
    users.forEach(userElement => {
        if (userElement.textContent.includes(user.name)) {
            userElement.classList.add("selected");
        }
    });

    // Update the chat header with the selected user's name
    chatHeader.innerHTML = `<h2>${user.name}</h2>`;

    // Display messages for the selected user
    displayUserMessages(selectedUser);
}

function displayUserMessages(user) {
    chatMessages.innerHTML = ""; // Clear previous messages

    const messages = userMessages[user.id];
    messages.forEach(message => {
        displayMessage(message);
    });
}

function displayMessage(message) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", message.type);
    messageElement.innerHTML = `
        <div class="message-content">
            ${message.content}
        </div>
    `;
    chatMessages.appendChild(messageElement);

    // Update the last message in the user list when a new message is received or sent
    if (selectedUser && message.type === 'received' && selectedUser.id === message.senderId) {
        const selectedUserElement = document.querySelector(".user.selected");
        if (selectedUserElement) {
            const lastMessageElement = selectedUserElement.querySelector(".last-message");
            lastMessageElement.textContent = `${selectedUser.name}: ${message.content}`;
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
    const messageContent = messageInput.value;
    if (messageContent.trim() !== "" && selectedUser !== null) {
        const message = { type: "sent", content: messageContent };
        userMessages[selectedUser.id].push(message);
        displayMessage(message);
        messageInput.value = "";
    }
}


// Show placeholder message when no user is selected
function showPlaceholderMessage() {
    const funnyMessages = [
        "Looks like it's just you and me, imaginary friend! Time to spill the tea.",
        "Waiting for the chat fairy to sprinkle some magic words! 🧚✨",
        "The ghost of messages past is here, waiting for your company! 👻",
        "Let's break the silence with the sound of imaginary laughter! 😄",
        "This chat is as empty as my coffee cup. Refill, anyone? ☕",
        "Why did the message go to therapy? It had too many issues! 🛋️",
        "Did you hear about the chatroom that caught on fire? It was lit! 🔥",
        "Why don't scientists trust atoms? Because they make up everything, just like my chat history!",
        "Why did the cookie cry? Because its mother was a wafer too emotional. 🍪😢",
        // Add more funny messages as needed
    ];

    const randomMessage = funnyMessages[Math.floor(Math.random() * funnyMessages.length)];

    const messageContainer = document.createElement("div");
    messageContainer.classList.add("placeholder-message");
    messageContainer.innerHTML = `<p>${randomMessage}</p>`;

    chatMessages.innerHTML = ""; // Clear previous messages
    chatMessages.appendChild(messageContainer);

    // Make it stylish and interactive
    const messageElement = messageContainer.querySelector("p");
    messageElement.style.fontFamily = "cursive";
    messageElement.style.fontSize = "20px";
    messageElement.style.textAlign = "center";
    messageElement.style.color = "#4CAF50";
    messageElement.style.margin = "20px 0";
    messageElement.style.opacity = "0.9";

    setTimeout(() => {
        messageElement.style.transform = "rotate(360deg)";
        messageElement.style.transition = "transform 1s";
        setTimeout(() => {
            messageElement.style.transform = "rotate(0deg)";
        }, 1000);
    }, 500);

    // Add click event to make it interactive
    messageElement.addEventListener("click", () => {
        messageElement.style.fontSize = "25px";
        messageElement.style.color = "#FF9800";
        messageElement.style.transition = "font-size 0.5s, color 0.5s";
        setTimeout(() => {
            messageElement.style.fontSize = "20px";
            messageElement.style.color = "#4CAF50";
        }, 500);
    });
}

// Initial stylish and interactive placeholder message
showPlaceholderMessage();

