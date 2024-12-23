To implement this solution in your environment, [import](https://github.com/new/import) the [repository](https://github.com/javiercarreraruiz/codepipeline-ecs-deploy-blog) and clone your imported repository to your local device:


****Create a Connection to GitHub****: Since the pipelines rely on your GitHub repository as the source, you'll need to set up an AWS CodeConnections connection to GitHub.

1. - ****Steps to Create the Connection****:
    - - ****Navigate to AWS CodeConnections****:
        - - Go to the AWS Management Console and open the [AWS](https://console.aws.amazon.com/codesuite/settings/connections) CodeConnections page.
        - ****Create a New Connection****:
        - - Click on ****Create connection****.
            - Select ****GitHub**** as the provider type.
        - ****Authorize AWS to Access GitHub****:
        - - Follow the prompts to authenticate with your GitHub account.
            - You'll be asked to grant AWS permissions to access your repositories. Ensure you authorize the correct repositories or organizations.
        - ****Retrieve the Connection ARN****:
        - - Once the connection is established, note the ****Connection ARN****. You'll need this value for the `GitHubConnectionArn` parameter in the CloudFormation template.

****Note 1:**** The connection allows AWS services like CodePipeline to securely interact with your GitHub repository. It enables automated triggering of pipelines based on code changes and fetches the latest code during the build process.

****Note 2****: AWS CodeConnections is the [new](https://aws.amazon.com/about-aws/whats-new/2024/03/aws-codeconnections-formerly-codestar-connections/) name of AWS CodeStar Connections.

****Prepare the ECS Container image****: Run the following commands to upload the first version of the container image.

```bash
aws ecr get-login-password --region <REGION_ID> | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.<REGION_ID>.amazonaws.com
aws ecr create-repository --repository-name demo-ecs-service-image
docker build -t <ACCOUNT_ID>.dkr.ecr.<REGION_ID>.amazonaws.com/demo-ecs-service-image .
docker push <ACCOUNT_ID>.dkr.ecr.<REGION_ID>.amazonaws.com/demo-ecs-service-image
```

****Note:**** The image's architecture should be x86.

****Deploy the Stack****: Use AWS CloudFormation to deploy the stack. You can do this via the AWS Management Console, AWS CLI, or AWS SDKs. Using AWS CLI:

```bash
aws cloudformation deploy \
  --template-file cloudformation-template.yml \
  --stack-name your-stack-name \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    GitHubConnectionArn=your-connection-arn \
    GitHubOwner=your-github-username \
    GitHubRepoName=your-repo-name \
    GitHubBranch=main \
    ECRRepositoryName=demo-ecs-service-image \
    ClusterName=demo-ecs-cluster \
    ServiceName=demo-ecs-service \
    TaskDefinitionFamily=demo-ecs-service-task-definition \
    VpcId=your-vpc-id \
    SubnetIds=your-subnet-ids-separated-by-commas
```

****Note:**** The deployment can take around 5 minutes.