import argparse
import os
import numpy as np
from sklearn.externals import joblib
from sklearn.ensemble import IsolationForest
import json


def model_fn(model_dir):
    clf = joblib.load(os.path.join(model_dir, "model.joblib"))
    return clf


def input_fn(request_body, request_content_type):
    if request_content_type == 'application/json':
        data = json.loads(request_body)
        test_data = np.array(data['test'])
        train_data = np.array(data['train'])
        return [train_data, test_data]
    else:
        pass


def predict_fn(input_data, model):
    full_data = np.concatenate(input_data, axis=0)
    label = model.fit_predict(full_data)
    print(label[0])

    return 1


def output_fn(prediction, content_type):
    return json.dumps({'result': 1})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Hyperparameters are described here. 
    parser.add_argument('--n_estimators', type=int, default=50)
    parser.add_argument('--contamination', type=float, default=(1 / 200))

    parser.add_argument('--model-dir', type=str, default=os.environ['SM_MODEL_DIR'])
    parser.add_argument('--train', type=str, default='')
    parser.add_argument('--output-data-dir', type=str, default='')

    args = parser.parse_args()

    # Now, create the model
    model = IsolationForest(n_estimators=args.n_estimators,
                            contamination=args.contamination)

    # Save the model to the output location in S3
    joblib.dump(model, os.path.join(args.model_dir, "model.joblib"))
