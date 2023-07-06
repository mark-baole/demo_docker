# Demo_docker

A small repo to show how to dockerize your ML model.

---
## How to use the repo

- Create processed data from raw data:

```bash
python src/data/make_dataset.py -i data/raw/iris.csv -o data/processed/iris_processed.csv
```

- Create feature engineered data from processed data:

```bash
python src/features/build_features.py -i data/processed/iris_processed.csv -o data/processed/iris_features.csv
```

- Train the model:

```bash
python src/models/train_model.py -i data/processed/iris_features.csv -o models/iris_model.pkl
```

- Run inference app:

```bash
bash run_app.sh
```

---
## Using docker (locally)

- Build the image:

```bash
docker build -t demo_image:v1.0.0 .
```

- Run the container:

```bash
docker run --name demo_container -it -d -p 8080:8080 demo_image:v1.0.0
```

- (Optional) Push the image to docker hub:

```bash
export DOCKER_ID="your_docker_id"
docker tag demo_image:v1.0.0 $DOCKER_ID/demo_image:v1.0.0
docker push $DOCKER_ID/demo_image:v1.0.0
```

---
## Using docker (on cloud)

- Set up your docker_id
```bash
export DOCKER_ID="your_docker_id"
```

- Pull the image from docker hub:

```bash
docker pull $DOCKER_ID/demo_image:v1.0.0
```

- Run the container:

```bash
docker run --name demo_container -it -d -p 8080:8080 $DOCKER_ID/demo_image:v1.0.0
```

---
## Using AWS (App Runner or FarGate)

### Common steps for both App Runner and FarGate: Push the image to ECR

- Set up your AWS account id:

```bash
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
```

- Create an ECR repository:

```bash
aws ecr create-repository --repository-name demo-container-aws --region ap-southeast-1
```

- Tag the image:

```bash
docker tag demo_image:v1.0.0 $AWS_ACCOUNT_ID.dkr.ecr.ap-southeast-1.amazonaws.com/demo-container-aws:v1.0.0
```

- Login to ECR:

```bash
aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.ap-southeast-1.amazonaws.com
```

- Push the image to ECR:

```bash
docker push $AWS_ACCOUNT_ID.dkr.ecr.ap-southeast-1.amazonaws.com/demo-container-aws:v1.0.0
```

### App Runner

- Create an App Runner service:

    - Visit https://ap-southeast-1.console.aws.amazon.com/apprunner/home?region=ap-southeast-1#/welcome, click "Create App Runner service"
    - Select Container image URI, and enter the URI of the image you pushed to ECR (click Browse images, then select the image and tag)
    - In Deployment setting, choose Automatic
    - Create new service role (or select an existing one if you have one)
    - Click "Next"
    - Enter a service name, e.g. demo-app-runner-service
    - Click "Next"
    - Click "Create & deploy"
    - Wait for the service to be deployed. The app URL will be shown once the deployment is complete.
    **- Remember to delete the service after you are done.**

### FarGate


- Create an ECS cluster:

```bash
aws ecs create-cluster --cluster-name demo-ecs-cluster --region ap-southeast-1
```

- Create a task definition:

```bash
aws ecs register-task-definition --cli-input-json file://AWS_config/task_definition.json --region ap-southeast-1
```

- Create a service:

```bash
aws ecs create-service --cli-input-json file://AWS_config/service.json --region ap-southeast-1 --enable-execute-command 
```

(note: you can also create the service from the AWS console. In the service.json file, replace the value of "subnets" with the subnet IDs of your VPC, and replace the value of "securityGroups" with the security group ID of your VPC.)

- Get the public IP of the service:

```bash
export TASK_ID=$(aws ecs list-tasks --cluster demo-ecs-cluster --region ap-southeast-1 --query "taskArns[0]" --output text)
export ENI_ID=$(aws ecs describe-tasks --cluster demo-ecs-cluster --tasks $TASK_ID --output text --query 'tasks[0].attachments[0].details[?name==`networkInterfaceId`].value')
export ECS_PUBLIC_IP=$(aws ec2 describe-network-interfaces --network-interface-ids $ENI_ID --region ap-southeast-1 --query 'NetworkInterfaces[0].Association.PublicIp' --output text)
echo $ECS_PUBLIC_IP
```

- Access the app:

```bash
curl $ECS_PUBLIC_IP:8080
```

> **Debugging for FarGate**
> 
> Note: if you get an error, first check the log of the container to see if the container is running properly. If the container is running properly, check the security group of the VPC to see if port 8080 is open.
>
> - View the log of the container:
>
>```bash
>aws ecs describe-tasks --cluster demo-ecs-cluster --tasks $TASK_ID --region ap-southeast-1 --query "tasks[0].containers[0].logStreamName" --output text
>```
>
>- Exec into the container:
>
>```bash
>export TASK_ID=$(aws ecs list-tasks --cluster demo-ecs-cluster --region ap-southeast-1 --query "taskArns[0]" --output text)
>aws ecs execute-command --cluster demo-ecs-cluster --task $TASK_ID --container demo-container-aws --region ap-southeast-1 --command "/bin/bash" --interactive
>```

- Clean up:

```bash
export TASK_ID=$(aws ecs list-tasks --cluster demo-ecs-cluster --region ap-southeast-1 --query "taskArns[0]" --output text)
aws ecs update-service --cluster demo-ecs-cluster --service demo-service --desired-count 0 --region ap-southeast-1
aws ecs delete-service --cluster demo-ecs-cluster --service demo-service --region ap-southeast-1
aws ecs delete-cluster --cluster demo-ecs-cluster --region ap-southeast-1
aws ecr batch-delete-image --repository-name demo-container-aws --image-ids imageTag=v1.0.0 --region ap-southeast-1
aws ecr delete-repository --repository-name demo-container-aws --region ap-southeast-1
```
---

## CI/CD with AWS CodePipeline (in progress)

- Create a CodePipeline:
    - Visit https://ap-southeast-1.console.aws.amazon.com/codesuite/codepipeline/pipelines?region=ap-southeast-1
    - Click "Create pipeline"
    - In the "Pipeline settings" section, enter a pipeline name, e.g. demo-pipeline
    - In the "Service role" section, select "New service role" and enter a role name, e.g. demo-pipeline-role (or select an existing role if you have one)
    - Click "Next"
    - In the "Source" section, select "Amazon ECR" as the source provider, and select the ECR repository you created earlier
    - In the "Image tag" section, enter "latest"
    - Click "Next"
    - In the "Build" section, select "Skip build stage" (we will use ECS to build the image)
    - In the "Deploy" section, select "Amazon ECS (Blue/Green)" as the deploy provider
    - Select the ECS cluster you created earlier
    - Select the ECS service you created earlier
    - Click "Next"
    - Click "Create pipeline"
    - 
