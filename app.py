from flask import Flask, request, jsonify
from fastai.basics import load_learner
from fastai.vision.core import load_image
from flask_cors import CORS,cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)

# load the learner
learn = load_learner(path='./models', file='5items_model.pkl')
classes = learn.dls.vocab


def predict_single(img_file):
    'function to take image and return prediction'
    prediction = learn.predict(load_image(img_file))
    probs_list = prediction[2].numpy()
    return {
        'category': classes[prediction[1].item()],
        'probs': {c: round(float(probs_list[i]), 5) for (i, c) in enumerate(classes)}
    }


# route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    return jsonify(predict_single(request.files['image']))

if __name__ == '__main__':
    app.run()