# demo_docker

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

## Using docker (AWS)

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
docker tag demo_image:v1.0.0 $AWS_ACCOUNT_ID.dkr.ecr.ap-southeast-1.amazonaws.com/demo-aws-repo:v1.0.0
```

- Login to ECR:

```bash
aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.ap-southeast-1.amazonaws.com
```

- Push the image to ECR:

```bash
docker push $AWS_ACCOUNT_ID.dkr.ecr.ap-southeast-1.amazonaws.com/demo-aws-repo:v1.0.0
```

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
aws ecs create-service --cli-input-json file://AWS_config/service.json --region ap-southeast-1
```

(note: you can also create the service from the AWS console. In the service.json file, replace the value of "subnets" with the subnet IDs of your VPC, and replace the value of "securityGroups" with the security group ID of your VPC.)

- Access the app:

```bash
curl http://[your_ecs_public_ip]:8080
```

(note: you can find the public IP of your ECS instance from the AWS console. For some reason, I have not been able to access the app from the public IP of the EC2 instance.)

- Clean up:

```bash
aws ecs update-service --cluster demo-ecs-cluster --service demo-service --desired-count 0 --region ap-southeast-1
aws ecs delete-service --cluster demo-ecs-cluster --service demo-service --region ap-southeast-1
aws ecs delete-cluster --cluster demo-ecs-cluster --region ap-southeast-1
aws ecr batch-delete-image --repository-name demo-container-aws --image-ids imageTag=v1.0.0 --region ap-southeast-1
aws ecr delete-repository --repository-name demo-container-aws --region ap-southeast-1
```