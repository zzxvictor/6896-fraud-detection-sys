import sagemaker
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.local import LocalSession

import numpy as np
if __name__ == '__main__':
    sess = LocalSession()
    script_path = 'model_config.py'

    # run the Scikit-Learn script
    sklearn = SKLearn(
        entry_point=script_path,
        instance_type="local",
        framework_version='0.20.0',
        hyperparameters={'n_estimators': 10, 'contamination': 1/200},
        role="arn:aws:iam::070192854459:role/sagemaker_test_role",
        sagemaker_session=sess
        )

    sklearn.fit()
    predictor = sklearn.deploy(initial_instance_count=1, instance_type="local")