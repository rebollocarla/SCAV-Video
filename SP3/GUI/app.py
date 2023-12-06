from flask import Flask, render_template, request, send_file, redirect, url_for
from pytube import YouTube
import os
from video_converter import VideoConverter

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Verifica si la carpeta de carga existe, si no, la crea
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_choice', methods=['POST'])
def upload_choice():
    choice = request.form['choice']
    if choice == 'file':
        return render_template('upload_file.html')
    elif choice == 'link':
        return render_template('paste_link.html')

@app.route('/process_file', methods=['POST'])
def process_file():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            output_name = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            
            return redirect(url_for('convert_and_download', input_video=file_path))
    return 'Error al procesar el archivo'

@app.route('/process_link', methods=['POST'])
def process_link():
    url = request.form['url']
    
    # Obtiene el path completo de la carpeta de carga
    upload_folder_path = app.config['UPLOAD_FOLDER']

    # Verifica si la carpeta de carga existe, si no, la crea
    if not os.path.exists(upload_folder_path):
        os.makedirs(upload_folder_path)
    
    # Create a YouTube object
    yt = YouTube(url)

    # Get the highest resolution stream available
    video_stream = yt.streams.get_highest_resolution()

    if yt.length <= 180:
        try:
            # Download the video
            video_path = os.path.join(upload_folder_path, f"{yt.title}.mp4")
            video_stream.download(video_path)

            return redirect(url_for('convert_and_download', input_video=video_path))
        except:
            return "Link is not working"
    else:
        return "Video is too long"

@app.route('/convert_and_download', methods=['GET', 'POST'])
def convert_and_download():
    if request.method == 'POST':
        # Obtén los valores de los campos del formulario
        your_resolution = request.form['resolution']
        your_codec = request.form['codec']  # Descomenta esto si tienes más campos

        # Obtén la ruta del archivo de entrada
        input_video = request.args.get('input_video')

        # Rutas de salida dentro de la carpeta de carga
        output_resolution_video = os.path.join(app.config['UPLOAD_FOLDER'], 'output_resolution')
        input2 = request.args.get('output_resolution')
        final_output_video = os.path.join(app.config['UPLOAD_FOLDER'], 'output_video')

        print(f"DEBUG: input_video = {input_video}")
        print(f"DEBUG: output_resolution_video = {output_resolution_video}")
        print(f"DEBUG: input2 = {input2}")
        print(f"DEBUG: final_output_video = {final_output_video}")

        # Realiza la conversión
        converter = VideoConverter(input_video=input_video)
        final_converter = VideoConverter(input_video=input2)

        converter.convert_resolution(output_video=output_resolution_video,resolution=your_resolution)

        print("DEBUG: Resolution conversion completed")
        
        output_video = final_converter.convert_codec(output_video=final_output_video, video_codec=your_codec)

        print(f"DEBUG: Output video path = {output_video}")

        return redirect(url_for('final_screen', output_video=output_video))

    return render_template('second_screen.html')  # Puedes crear un nuevo template para la selección de resolución y codec

@app.route('/final_screen', methods=['GET'])
def final_screen():
    # Obtén la ruta del archivo de salida
    output_video = request.args.get('output_video')

    # You can perform any additional processing or logic here
    return render_template('final_screen.html', output_video=output_video)

@app.route('/download_result', methods=['GET'])
def download_result():
    # Obtén la ruta del archivo de salida
    output_video = request.args.get('output_video')

    try:
        return send_file(output_video, as_attachment=True, download_name='converted_video.mp4')
    except Exception as e:
        return f'Error during download: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)
