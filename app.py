from flask import Flask, render_template, request
from aux.gemini_api_request import model_call

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    print('Hello 1')
    analysis_result = None
    if request.method == 'POST':
        print('Hello 2')
        exercise = request.form['exercise']
        prompt = f'The exercise the person is doing is {exercise}.'
        video = request.files['video']

        if video and exercise:
            print('Hello 3')
            print(video, exercise, prompt)
            model_response = model_call(video, prompt)
            analysis_result = model_response

    return render_template('index.html', analysis_result=analysis_result)


if __name__ == '__main__':
    app.run(debug=True)