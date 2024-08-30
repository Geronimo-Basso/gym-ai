import os
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from aux.gemini_api_request import model_call

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    analysis_result = None
    if request.method == 'POST':
        exercise = request.form['exercise']
        prompt = f'The exercise the person is doing is {exercise}.'
        video = request.files['video']

        if video and exercise and allowed_file(video.filename):
            filename = secure_filename(video.filename)
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            video.save(video_path)

            print(f'Video saved at: {video_path}')

            model_response = model_call(video_path, prompt)
            analysis_result = model_response

            print(f'Model response: {model_response}')

    return render_template('index.html', analysis_result=analysis_result)


if __name__ == '__main__':
    app.run(debug=True)