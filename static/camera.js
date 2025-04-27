// Código para activar la cámara y tomar una foto
function startCamera() {
    const video = document.createElement('video');
    video.style.width = "100%";
    video.style.maxHeight = "300px";
    document.getElementById('messages').prepend(video);

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
            video.play();

            const captureButton = document.createElement('button');
            captureButton.textContent = '📸 Tomar foto';
            captureButton.style.margin = '10px';
            document.getElementById('messages').prepend(captureButton);

            captureButton.addEventListener('click', () => {
                const canvas = document.createElement('canvas');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                canvas.getContext('2d').drawImage(video, 0, 0);

                canvas.toBlob(blob => {
                    const file = new File([blob], "captura.png", { type: 'image/png' });
                    const formData = new FormData();
                    formData.append('file', file);

                    fetch('/upload', {
                        method: 'POST',
                        body: formData
                    }).then(res => {
                        if (res.ok) {
                            console.log('Foto enviada');
                        }
                    });
                }, 'image/png');

                // Detener cámara después de capturar
                stream.getTracks().forEach(track => track.stop());
                video.remove();
                captureButton.remove
