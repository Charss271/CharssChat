function toggleEmoji() {
    const picker = document.getElementById("emoji-picker");
    picker.style.display = picker.style.display === "block" ? "none" : "block";
}

window.onload = () => {
    const picker = document.getElementById("emoji-picker");
    const emojis = ["😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😎", "😍", "😘", "😜", "😢", "😭", "😡", "👍", "👎", "👏", "🙏"];
    emojis.forEach(e => {
        const span = document.createElement("span");
        span.textContent = e;
        span.style.cursor = "pointer";
        span.style.fontSize = "20px";
        span.style.margin = "5px";
        span.onclick = () => {
            document.getElementById("message").value += e;
            toggleEmoji();  // Ocultar el selector al seleccionar un emoji
        }
        picker.appendChild(span);
    });
};
