function sendMessage() {
    let userInput = document.getElementById("user-input").value.trim();
    if (userInput === "") return;

    let chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;

    fetch("/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userInput })
    })
    .then(response => response.json())
    .then(data => {
        chatBox.innerHTML += `<p><strong>Bot:</strong> ${data.results.join("<br>")}</p>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    });

    document.getElementById("user-input").value = ""; // Clear input field
}
