import sagemaker
from sagemaker.sklearn.estimator import SKLearn
import json


def handler(event, context):
    classifier_model = 'model_config.py'
    sklearn = SKLearn(
        entry_point=classifier_model,
        instance_type="ml.m5.large",
        framework_version='0.20.0',
        hyperparameters={'n_estimators': 10, 'contamination': 1 / 200},
        role="arn:aws:iam::070192854459:role/sagemaker_test_role",
    )
    return {
        'statusCode': 200,
        'body': json.dumps("Hello World from sagemaker !!!")
    }