#!/bin/bash

set -e

# Configuration
AWS_REGION="us-east-1"
ECR_BACKEND_REPO="fondos-backend"
ECR_FRONTEND_REPO="fondos-frontend"
ENVIRONMENT="dev"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Print section header
print_section() {
  echo -e "\n${YELLOW}==== $1 ====${NC}\n"
}

# Check if AWS CLI is installed
print_section "Checking prerequisites"
if ! command -v aws &> /dev/null; then
  echo -e "${RED}AWS CLI is not installed. Please install it first.${NC}"
  exit 1
fi

# Get AWS account ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
if [ $? -ne 0 ]; then
  echo -e "${RED}Failed to get AWS account ID. Make sure you're logged in.${NC}"
  exit 1
fi

echo -e "${GREEN}Using AWS Account ID: ${AWS_ACCOUNT_ID}${NC}"

# Create ECR repositories if they don't exist
print_section "Setting up ECR repositories"

create_repo() {
  local repo_name=$1
  if aws ecr describe-repositories --repository-names ${repo_name} --region ${AWS_REGION} &> /dev/null; then
    echo -e "Repository ${GREEN}${repo_name}${NC} already exists"
  else
    echo -e "Creating repository ${GREEN}${repo_name}${NC}"
    aws ecr create-repository --repository-name ${repo_name} --region ${AWS_REGION}
  fi
}

create_repo ${ECR_BACKEND_REPO}
create_repo ${ECR_FRONTEND_REPO}

# Log in to ECR
print_section "Logging in to ECR"
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# Build and push backend image
print_section "Building and pushing backend image"
BACKEND_IMAGE_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_BACKEND_REPO}:latest"

echo "Building backend image..."
docker build -t ${BACKEND_IMAGE_URI} ./backend

echo "Pushing backend image to ${BACKEND_IMAGE_URI}..."
docker push ${BACKEND_IMAGE_URI}

# Build and push frontend image
print_section "Building and pushing frontend image"
FRONTEND_IMAGE_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_FRONTEND_REPO}:latest"

echo "Building frontend image..."
docker build -t ${FRONTEND_IMAGE_URI} ./frontend

echo "Pushing frontend image to ${FRONTEND_IMAGE_URI}..."
docker push ${FRONTEND_IMAGE_URI}

# Deploy backend using CloudFormation
print_section "Deploying backend with CloudFormation"
BACKEND_STACK_NAME="fondos-backend-${ENVIRONMENT}"

if aws cloudformation describe-stacks --stack-name ${BACKEND_STACK_NAME} --region ${AWS_REGION} &> /dev/null; then
  echo "Updating backend stack ${BACKEND_STACK_NAME}..."
  aws cloudformation update-stack \
    --stack-name ${BACKEND_STACK_NAME} \
    --template-body file://backend/cloudformation.yaml \
    --parameters \
      ParameterKey=EnvironmentName,ParameterValue=${ENVIRONMENT} \
      ParameterKey=ContainerImageUrl,ParameterValue=${BACKEND_IMAGE_URI} \
    --capabilities CAPABILITY_IAM \
    --region ${AWS_REGION}
else
  echo "Creating backend stack ${BACKEND_STACK_NAME}..."
  aws cloudformation create-stack \
    --stack-name ${BACKEND_STACK_NAME} \
    --template-body file://backend/cloudformation.yaml \
    --parameters \
      ParameterKey=EnvironmentName,ParameterValue=${ENVIRONMENT} \
      ParameterKey=ContainerImageUrl,ParameterValue=${BACKEND_IMAGE_URI} \
    --capabilities CAPABILITY_IAM \
    --region ${AWS_REGION}
fi

echo "Waiting for backend stack to complete..."
aws cloudformation wait stack-create-complete --stack-name ${BACKEND_STACK_NAME} --region ${AWS_REGION} || \
aws cloudformation wait stack-update-complete --stack-name ${BACKEND_STACK_NAME} --region ${AWS_REGION}

# Get backend API endpoint
BACKEND_API_ENDPOINT=$(aws cloudformation describe-stacks \
  --stack-name ${BACKEND_STACK_NAME} \
  --query "Stacks[0].Outputs[?OutputKey=='ApiEndpoint'].OutputValue" \
  --output text \
  --region ${AWS_REGION})

echo -e "Backend API endpoint: ${GREEN}${BACKEND_API_ENDPOINT}${NC}"

# Deploy frontend using CloudFormation
print_section "Deploying frontend with CloudFormation"
FRONTEND_STACK_NAME="fondos-frontend-${ENVIRONMENT}"

if aws cloudformation describe-stacks --stack-name ${FRONTEND_STACK_NAME} --region ${AWS_REGION} &> /dev/null; then
  echo "Updating frontend stack ${FRONTEND_STACK_NAME}..."
  aws cloudformation update-stack \
    --stack-name ${FRONTEND_STACK_NAME} \
    --template-body file://frontend/cloudformation.yaml \
    --parameters \
      ParameterKey=EnvironmentName,ParameterValue=${ENVIRONMENT} \
      ParameterKey=ContainerImageUrl,ParameterValue=${FRONTEND_IMAGE_URI} \
      ParameterKey=ApiEndpoint,ParameterValue=${BACKEND_API_ENDPOINT} \
    --capabilities CAPABILITY_IAM \
    --region ${AWS_REGION}
else
  echo "Creating frontend stack ${FRONTEND_STACK_NAME}..."
  aws cloudformation create-stack \
    --stack-name ${FRONTEND_STACK_NAME} \
    --template-body file://frontend/cloudformation.yaml \
    --parameters \
      ParameterKey=EnvironmentName,ParameterValue=${ENVIRONMENT} \
      ParameterKey=ContainerImageUrl,ParameterValue=${FRONTEND_IMAGE_URI} \
      ParameterKey=ApiEndpoint,ParameterValue=${BACKEND_API_ENDPOINT} \
    --capabilities CAPABILITY_IAM \
    --region ${AWS_REGION}
fi

echo "Waiting for frontend stack to complete..."
aws cloudformation wait stack-create-complete --stack-name ${FRONTEND_STACK_NAME} --region ${AWS_REGION} || \
aws cloudformation wait stack-update-complete --stack-name ${FRONTEND_STACK_NAME} --region ${AWS_REGION}

# Get frontend endpoint
FRONTEND_ENDPOINT=$(aws cloudformation describe-stacks \
  --stack-name ${FRONTEND_STACK_NAME} \
  --query "Stacks[0].Outputs[?OutputKey=='FrontendEndpoint'].OutputValue" \
  --output text \
  --region ${AWS_REGION})

print_section "Deployment Complete"
echo -e "Backend API: ${GREEN}${BACKEND_API_ENDPOINT}${NC}"
echo -e "Frontend: ${GREEN}${FRONTEND_ENDPOINT}${NC}"
echo -e "\n${GREEN}Application deployed successfully!${NC}" 