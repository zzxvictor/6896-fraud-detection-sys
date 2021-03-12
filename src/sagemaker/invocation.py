import boto3
import json
import numpy as np
from sagemaker.local import LocalSession, LocalSagemakerRuntimeClient

# grab environment variables
# ENDPOINT_NAME = 'sagemaker-scikit-learn-2021-03-11-14-52-23-028'
# runtime = boto3.client('runtime.sagemaker')


if __name__ == '__main__':
    data = {'test': np.random.randn(1, 10).tolist(),
            'train': np.random.randn(200, 10).tolist()}

    response = LocalSagemakerRuntimeClient().invoke_endpoint(EndpointName="local",
                                                             ContentType='application/json',
                                                             Body=json.dumps(data))
    result = response['Body'].data.decode('utf-8')
    print(result)
