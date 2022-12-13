# Project Bellflower : Step Function with Lambda, SNS, SQS, S3 orchestration with callback functionality

A State Machine demonstrating Lambda orchestration with a third party application using S3 and SQS - Lambda Callback functionality and notifying the users using SNS notification.

## Description

This is demonstration of a State Machine with Lambda, SNS, SQS and S3. The processing Lambda generates a payload and pushes to a SQS Trigger. An integration Lambda processes the Payload and send a file with task token to S3 outbound folder. An Business Application processes the information and sends a success trigger to the S3 inbound folder. The integration Lambda reads the success trigger and sends a success signal to the State Machine and resumes processing. Once processing completes, the State Machine sends a Success notification to SNS Topic. If the processing Lambda fails after 3 retries the State Machine fails and a Failure notification is sent to the SNS Topic..

![Project Tauris - Design Diagram]( https://subhamayblog.files.wordpress.com/2022/11/38_bellflower_1_1_architecture_diagram.png?w=1024")

## Getting Started

### Dependencies

* Create a Customer Managed KMS Key in the region where you want to create the stack..
* Modify the KMS Key Policy to let the IAM user encrypt / decrypt using any resource using the created KMS Key.

### Installing

* Clone the repository.
* Create a S3 bucket and make it public.
* Create the folders - bellflower/cft/nested-stacks, bellflower/cft/cross-stacks, bellflower/code, bellflower/state-machine
* Upload the following YAML templates to bellflower/cft/nested-stacks
    * iam-role-stack.yaml
    * lambda-function-stack.yaml
    * s3-stack.yaml
    * sns-stack.yaml
    * sqs-stack
* Upload the following YAML templates to bellflower/cft/cross-stacks
    * custom-resource-lambda-stack.yaml
* Upload the following YAML templates to tarius/cft/
    * bellflower-root-stack.yaml
* Zip and Upload the following Python files  to bellflower/cft/code
    * processing_lambda.py
    * integration_lambda.py
* Upload the ASL file state-machine.json to bellflower/state-machine
* Create the cross-stack using the template custom-resource-lambda-stack.yaml by using the S3 url and pass the appropriate parameters.
* Create the entire using by using the root stack template custom-resource-lambda-stack.yaml by providing the required parameters and the s3 cross stack name created in the previous step.

### Executing program

* Execute the state machine with default payload.
* Get the UUID of the execution from the log or from the S3 bucket outbound folder.
* Create a success.json file in the bucket s3://<s3 bucket uri>/inbound/<UUID>/
* Copying the success.json to S3 inbound folder
```
aws s3 cp success.json s3://<s3 bucket uri>/inbound/<UUID>/
```

## Help

Post message in my blog (https://subhamay.blog)


## Authors

Contributors names and contact info

Subhamay Bhattacharyya  - [subhamoyb@yahoo.com](https://subhamay.blog)

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under Subhamay Bhattacharyya. All Rights Reserved.

## Acknowledgments

Inspiration, code snippets, etc.
* [Stephane Maarek ](https://www.linkedin.com/in/stephanemaarek/)
* [Neal Davis](https://www.linkedin.com/in/nealkdavis/)
* [Adrian Cantrill](https://www.linkedin.com/in/adriancantrill/)
* [Durga Gadiraju Cantrill](https://www.https://www.linkedin.com/in/durga0gadiraju/)
