import sagemaker
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.local import LocalSession
import boto3

import numpy as np
if __name__ == '__main__':
    # need to change the profile name
    boto3_sess = boto3.Session(profile_name="eecs6895")
    sess = sagemaker.Session(boto_session=boto3_sess)
    # sess = LocalSession()
    script_path = 'model_config.py'

    # run the Scikit-Learn script
    # sklearn = SKLearn(
    #     entry_point=script_path,
    #     instance_type="local",
    #     framework_version='0.20.0',
    #     hyperparameters={'n_estimators': 10, 'contamination': 2/200},
    #     role="arn:aws:iam::070192854459:role/sagemaker_test_role",
    #     sagemaker_session=sess
    #     )
    # run the Scikit-Learn script in sageMaker
    sklearn = SKLearn(
        entry_point=script_path,
        instance_type="ml.m4.xlarge",
        framework_version='0.20.0',
        hyperparameters={'n_estimators': 10, 'contamination': 2/200},
        role="arn:aws:iam::614633518167:role/sagemaker_exec_role",
        sagemaker_session=sess
        )
    sklearn.fit()
    print("finished")
    endpoint = "6895-sagemaker-scikit-learn"
    predictor = sklearn.deploy(initial_instance_count=1,
                               instance_type="ml.m4.xlarge",
                                endpoint_name=endpoint)
