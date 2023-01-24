AWSTemplateFormatVersion: 2010-09-09
Description: Medium custom lambda stack
​
#Parameters:
#  CloudTrailName:
#    Type: String
#  BucketName:
#    Type: String
​
Resources:
  LambdaExecutionRole:
      Type: AWS::IAM::Role
      Properties:
        AssumeRolePolicyDocument:
          Version: '2012-10-17'
          Statement:
          - Effect: Allow
            Principal:
              Service:
              - lambda.amazonaws.com
            Action:
            - sts:AssumeRole
        Path: "/"
        Policies:
        - PolicyName: !Sub ExampleLambdaPolicy-${AWS::Region}
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
            - Effect: Allow
              Action:
              - logs:CreateLogGroup
              - logs:CreateLogStream
              - logs:PutLogEvents
              Resource: arn:aws:logs:*:*:*
            - Effect: Allow
              Action:
              - cloudformation:DescribeStacks
              - cloudformation:DescribeStackEvents
              - cloudformation:DescribeStackResource
              - cloudformation:DescribeStackResources
              - CloudTrail:*
              Resource: "*"
​
  CustomBackedLambda:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: CloudTrailLambda
      Runtime: python3.9
      Role: !GetAtt LambdaExecutionRole.Arn
      Handler: index.lambda_handler
      Timeout: 90
      Code:
        ZipFile: |
          import boto3
          import traceback
          import cfnresponse
          import logging
          logger = logging.getLogger()
          logger.setLevel(logging.INFO)
          def lambda_handler(event, context):
            print(event)
            if event['RequestType'] == 'Delete':
              try:
                responseData = {'Success': 'Deleted Resource'}
                cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, 'CloudTrailCustomConfigResource')
              except Exception as e:
                logger.error(e, exc_info=True)
                responseData = {}
                cfnresponse.send(event, context, cfnresponse.FAILED, responseData, 'CloudTrailCustomConfigResource')
            elif event.get('RequestType') == 'Create':
              try:
                  # Get variables from Custom Resource configuration
                  CloudTrailName = event["ResourceProperties"]["CloudTrailName"]
                  BucketName = event["ResourceProperties"]["BucketName"]
                  # Open CloudTrail client
                  cloudtrail = boto3.client('cloudtrail')
                  response = cloudtrail.put_event_selectors(
                    TrailName=CloudTrailName,
                    AdvancedEventSelectors=[
                      {
                        "Name": "Log PutObject events",
                        "FieldSelectors": [
                          { "Field": "eventCategory", "Equals": ["Data"] },
                          { "Field": "resources.type", "Equals": ["AWS::S3::Object"] },
                          { "Field": "eventName", "Equals": ["PutObject"] },
                          { "Field": "resources.ARN", "StartsWith": ["arn:aws:s3:::" + BucketName] }
                        ]
                      }
                    ])
                  responseData = {'Success': 'Added advanced event selector to trail'}
                  cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, 'CloudTrailCustomConfigResource')
              except Exception as e:
                logger.error(e, exc_info=True)
                responseData = {}
                cfnresponse.send(event, context, cfnresponse.FAILED, responseData, 'CloudTrailCustomConfigResource')
      Description: Cloud Trail Advanced Event Selector Lambda
​
 # InvokeCustomLambda:
  #  DependsOn: CustomBackedLambda
  #  Type: Custom::CloudTrailSelector
  #  Properties:
  #    ServiceToken: !GetAtt CustomBackedLambda.Arn
  #    CloudTrailName: !Ref CloudTrailName
  #    BucketName: !Ref BucketName