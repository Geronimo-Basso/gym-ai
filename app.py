from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        exercise = request.form['exercise']
        video = request.files['video']

        # Here you would process the video and perform AI analysis
        # For now, we'll just return a dummy result
        analysis_result = f"Analysis for {exercise}: Great form! Your depth is excellent, but try to keep your back a bit straighter at the bottom of the movement."

        return render_template('index.html', analysis_result=analysis_result)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
