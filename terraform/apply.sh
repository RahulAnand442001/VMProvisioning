#!/bin/bash

# init terraform module for provider
terraform init

# validate errors before deployment
terraform plan

# run terraform file
terraform apply -var-file=tfvars.json -auto-approve
