let chatHistory = "";

// session id
let sessionId = localStorage.getItem("session_id");
if (!sessionId) {
    sessionId = crypto.randomUUID();
    localStorage.setItem("session_id", sessionId);
}


// DOM references (CRITICAL)
document.addEventListener("DOMContentLoaded", () => {
    const sendBtn = document.getElementById("send-btn");
    const input = document.getElementById("user-input");

    sendBtn.addEventListener("click", sendChat);

    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") sendChat();
    });
});

async function sendChat() {
    const input = document.getElementById("user-input");
    const chatWindow = document.getElementById("chat-window");

    if (!input || !chatWindow) {
        console.error("DOM elements not found");
        return;
    }

    const message = input.value.trim();
    if (!message) return;

    appendBubble(message, "scammer");
    input.value = "";

    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
            })
        });

        if (!res.ok) throw new Error("Backend error");

        const data = await res.json();
        appendBubble(data.reply, "sharma");

    } catch (err) {
        console.error(err);
        appendBubble(
            "Arrey beta… network problem lag raha hai. Can you repeat?",
            "sharma"
        );
    }
}

function appendBubble(text, sender) {
    const chatWindow = document.getElementById("chat-window");
    const bubble = document.createElement("div");
    bubble.className = `bubble ${sender}`;

    bubble.innerText = text;
    chatWindow.appendChild(bubble);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function generateReport() {
    const modal = document.getElementById("report-modal");
    const overlay = document.getElementById("overlay");
    const content = document.getElementById("report-content");

    modal.style.display = "block";
    overlay.style.display = "block";
    content.innerText = "Analyzing conversation and extracting scam details...";

    try {
        const res = await fetch("/api/report", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                session_id: sessionId   // 🔥 THIS FIXES IT
            })
        });

        const data = await res.json();
        content.innerHTML = data.report.replace(/\n/g, "<br>");

    } catch (err) {
        content.innerText = "Error generating report.";
        console.error(err);
    }
}