from flask import Flask, request, send_file, jsonify, send_from_directory
import yt_dlp
import os
import re

app = Flask(__name__, static_folder="../frontend", static_url_path="")

DOWNLOAD_FOLDER = "music_downloaded"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    urls = data.get("urls", [])
    if not urls:
        return jsonify({"error": "No URLs provided"}), 400

    results = []

    for url in urls:
        try:
            # Extraemos información del video antes de descargarlo
            ydl_opts = {
                'format': 'bestaudio/best',
                'noplaylist': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)  # No descargar, solo obtener info
                title = info_dict.get('title', 'audio')  # Usamos el título del video, si no lo encontramos, usamos 'audio'

                # Sanitizamos el título para evitar caracteres inválidos
                title = re.sub(r'[\\/*?:"<>|]', "", title)

                output_path = os.path.join(DOWNLOAD_FOLDER, f"{title}.mp3")

                if os.path.exists(output_path):
                    # Si el archivo ya existe, lo sobreescribimos
                    print(f"El archivo '{title}.mp3' ya existe y ha sido reemplazado.")

                # Ahora descargamos el archivo con el nombre único
                ydl_opts['outtmpl'] = output_path
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

        except Exception as e:
            results.append({
                'message': f"Error en la conversión de la URL: {url}",
                'error': str(e)
            })

    return jsonify(results)  # Retornamos los resultados de todas las conversiones

if __name__ == '__main__':
    app.run(debug=True)
