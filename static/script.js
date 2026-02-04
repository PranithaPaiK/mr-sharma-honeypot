async function sendMessage() {
    const input = document.getElementById("user-input");
    const text = input.value.trim();
    if (!text) return;

    document.getElementById("messages").innerHTML +=
        `<div class="msg scammer">${text}</div>`;

    input.value = "";

    const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            session_id: "session-1",
            text: text
        })
    });

    const data = await res.json();

    document.getElementById("messages").innerHTML +=
        `<div class="msg sharma">${data.reply}</div>`;
}