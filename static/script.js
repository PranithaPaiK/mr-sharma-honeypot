function handleKey(e) {
    if (e.key === "Enter") sendMessage();
}

async function sendMessage() {
    const input = document.getElementById('user-input');
    const msgDiv = document.getElementById('messages');
    const alertBox = document.getElementById('extraction-alert');
    const text = input.value.trim();

    if (!text) return;

    // Show scammer message
    msgDiv.innerHTML += `<div class="msg scammer">${text}</div>`;
    input.value = '';
    msgDiv.scrollTop = msgDiv.scrollHeight;

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: usermessage })
        });

        const data = await response.json();

        let reply = data.reply;


        msgDiv.innerHTML += `<div class="msg sharma">${reply}</div>`;

        // 🚨 Show extracted info
        if (data.detected_info &&
            (data.detected_info.upi_ids.length > 0 ||
             data.detected_info.links.length > 0)) {

            alertBox.style.display = 'block';
            alertBox.innerText =
                "🚨 Detected: " +
                (data.detected_info.upi_ids[0] ||
                 data.detected_info.links[0]);

            setTimeout(() => {
                alertBox.style.display = 'none';
            }, 5000);
        }

    } catch (error) {
        console.error("Frontend error:", error);

        msgDiv.innerHTML +=
            `<div class="msg sharma">Arre beta… my internet is very slow. Please repeat slowly.</div>`;
    }

    msgDiv.scrollTop = msgDiv.scrollHeight;
}