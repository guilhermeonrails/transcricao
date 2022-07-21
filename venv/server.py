from flask import Flask, render_template
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import PrettyPrintFormatter
from flask import request
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcrever/', methods=['POST', 'GET'])
def buscar_transcricao():
    if request.method == 'POST' or request.method == 'GET':
        data = []
        link_do_video = request.form['busca']
        id_do_video = encontrar_o_id_do_video(link_do_video)
        ts = YouTubeTranscriptApi.get_transcript(id_do_video, languages=['pt'])
        for i in ts:
            tempo = i['start'] / 100
            tempo_fixado = "{:.2f}".format(tempo)
            texto = str(tempo_fixado) + " "+ i['text'] 
            data.append(texto)
        formatter = PrettyPrintFormatter()
        data = formatter.format_transcript(data)
        return render_template('transcricao.html', data=data)
    else:
        return render_template('transcricao.html', data=data)

@app.route('/transcrever-sem-tempo/')
def buscar_transcricao_sem_tempo():
    data = []
    ts = YouTubeTranscriptApi.get_transcript('', languages=['pt'])
    for i in ts:
        data.append(i['text'])
    formatter = PrettyPrintFormatter()
    data = formatter.format_transcript(data)
    return render_template('transcricao.html', data=data)

def encontrar_o_id_do_video(busca):
    url_data = urlparse(busca)
    print(url_data)
    return url_data.query[2::]


if __name__ == '__main__':
    app.run(debug=True) 