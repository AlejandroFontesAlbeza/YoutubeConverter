// Añadir una nueva fila para URL
function agregarFila() {
    const container = document.getElementById('urls-container');
    const newRow = document.createElement('div');
    newRow.classList.add('url-row');
    newRow.innerHTML = `
        <input type="text" class="url-input" placeholder="Pega el enlace aquí">
        <button onclick="eliminarFila(this)">Eliminar</button>
    `;
    container.appendChild(newRow);
}

// Eliminar la fila correspondiente
function eliminarFila(button) {
    const row = button.parentElement; // La fila que contiene el botón
    row.remove(); // Eliminar la fila
}

async function convertir() {
    const urlInputs = document.querySelectorAll('.url-input');
    const urls = [];

    // Recopilar todas las URLs de los campos de entrada
    urlInputs.forEach(input => {
        const url = input.value.trim();
        if (url) urls.push(url);
    });

    if (urls.length === 0) {
        alert('Por favor, ingresa al menos un enlace.');
        return;
    }

    const messagesDiv = document.getElementById('messages');
    messagesDiv.innerHTML = ''; // Limpiar mensajes anteriores

    const response = await fetch('/convert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ urls }) // Enviar las URLs como array
    });

    if (response.ok) {
        const results = await response.json();
        
        results.forEach((result, index) => {
            const link = document.createElement('a');
            link.href = result.file;
            link.download = `audio_${index + 1}.mp3`;  // Nombrar los archivos secuencialmente
            link.textContent = `Descargar MP3 ${index + 1}`;
            messagesDiv.appendChild(link);
            messagesDiv.appendChild(document.createElement('br'));
        });
    } else {
        const error = await response.json();
        messagesDiv.innerHTML += `<p>Error en la conversión: ${error.error}</p>`;
    }
}
