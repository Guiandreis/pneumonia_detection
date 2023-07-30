import preprocess_and_predict_local
from flask import Flask, request, send_file, render_template
import json
import aws_predict

app = Flask(__name__, template_folder='static')

@app.route('/')
def index():
    print('index')
    return send_file('static\image.html')

@app.route('/image', methods=['POST'])
def receive_image():
    file_storage = request.files.get('image')
    name = file_storage.filename

    file_storage_aws = file_storage.read()

    if '.' in name[-4:]:
        new_name = name.split('.')[:-1]
        json_name = ''.join(new_name)

    process = 'AWS' # local
    
    if process == 'local':
        pred_probs = preprocess_and_predict_local.process_exam(file_storage)
        output = {
                'Pneumonia detector chances in (%)' : '',
                'Normal Chance': float(pred_probs[0][0])*100, 
                'Pneumonia Chance' : float(pred_probs[0][1])*100 
                }

        json_object = json.dumps(output)

        with open('outputs/' +json_name + ".json", "w") as outfile:
            outfile.write(json_object)
    
    else:
        output = aws_predict.aws_call_predictions(file_storage_aws, name)
        output = json.loads(output)


    return render_template(
        'predictions.html', data = output)

if __name__ == '__main__':
    app.run(debug = True)