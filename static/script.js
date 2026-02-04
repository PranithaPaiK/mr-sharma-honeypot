function handleKey(e) {
    if (e.key === "Enter") sendMessage();
}

function fallbackReply() {
    const replies = [
        "Hmm beta, please continue… I’m listening carefully.",
        "Yes beta, go on. Tell me more.",
        "I see… please explain clearly.",
        "Hmm… that sounds important. Continue beta.",
        "Alright beta, I am following you."
    ];
    return replies[Math.floor(Math.random() * replies.length)];
}

async function sendMessage() {
    const input = document.getElementById('user-input');
    const msgDiv = document.getElementById('messages');
    const alertBox = document.getElementById('extraction-alert');
    const text = input.value.trim();

    if (!text) return;

    msgDiv.innerHTML += `<div class="msg scammer">${text}</div>`;
    input.value = '';
    msgDiv.scrollTop = msgDiv.scrollHeight;

    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ message: text })
        });

        const data = await response.json();

        const reply = data.reply && data.reply.trim()
            ? data.reply
            : fallbackReply();

        msgDiv.innerHTML += `<div class="msg sharma">${reply}</div>`;

        if (data.detected_info &&
            (data.detected_info.upi_ids.length > 0 ||
             data.detected_info.links.length > 0)) {

            alertBox.style.display = 'block';
            alertBox.innerText =
                "🚨 Detected: " +
                (data.detected_info.upi_ids[0] ||
                 data.detected_info.links[0]);

            setTimeout(() => alertBox.style.display = 'none', 5000);
        }

    } catch (err) {
        msgDiv.innerHTML += `<div class="msg sharma">${fallbackReply()}</div>`;
    }

    msgDiv.scrollTop = msgDiv.scrollHeight;
}