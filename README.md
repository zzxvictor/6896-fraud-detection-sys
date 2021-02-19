# 6896-fraud-detection-sys
Fraud Detection System for EECS6895

# AWS CloudFormation
## Nested stack v.s Cross-stack referencing
![Nested Stack](images/nested_stack.png)

## References
https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/walkthrough-crossstackref.html

https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/outputs-section-structure.html

https://www.youtube.com/watch?v=eoiSBAtRxZg

https://stackoverflow.com/questions/56157423/cloudformation-cross-stack-vs-nested-stack#:~:text=2%20Answers&text=You%20should%20use%20cross%2Dstack,and%20updating%20the%20stacks%20independently.

## Resources
1. Host ML model on AWS Sagemaker: 
    * sample code: https://towardsdatascience.com/deploying-a-scikit-learn-model-on-aws-using-sklearn-estimators-local-jupyter-notebooks-and-the-d94396589498 
    * documentation: https://sagemaker.readthedocs.io/en/stable/frameworks/sklearn/using_sklearn.html#sagemaker-scikit-learn-model-server
    * Isolation forest: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html 
    * Local Outlier Factor: https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LocalOutlierFactor.html
2. Nested Cloudformation Stack And Parameter Sharing:
    * https://aws.amazon.com/premiumsupport/knowledge-center/cloudformation-nested-stacks-values/
3. Fraud Data Generation: 
    * https://blog.clover.com/how-to-detect-in-store-credit-card-fraud/
    * https://www.semanticscholar.org/paper/Data-mining-for-credit-card-fraud%3A-A-comparative-Bhattacharyya-Jha/9d26f0ba02ee5efe9b9c7bdcb5f528c8b8253cf7?p2df
    * https://www.identityguard.com/news/credit-card-fraud-detection
    * https://lbezone.ust.hk/pdfviewer/web/viewer.php?file=aHR0cHM6Ly9sYmV6b25lLnVzdC5oay9vYmovMS9vL2IxMDIzMjM4L2IxMDIzMjM4LnBkZg==#page=1
    * MUST READ: https://github.com/namebrandon/Sparkov/blob/master/README.md
   * https://arxiv.org/pdf/1709.08920.pdf
