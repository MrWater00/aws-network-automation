# AWS Network Automation 🌐

A complete AWS network infrastructure automation project built with **Terraform** and **Python boto3**. This project automates the creation and management of VPCs, subnets, security groups, and internet gateways — the exact setup used by real startups running on AWS.

> Built and tested locally using LocalStack — no AWS account or credit card required.

---

## 📋 Table of Contents
- [About the Project](#about-the-project)
- [Architecture](#architecture)
- [Tools and Technologies](#tools-and-technologies)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [What I Learned](#what-i-learned)

---

## About the Project

Cloud engineers are expected to automate infrastructure — not click buttons manually. This project demonstrates two industry-standard approaches to AWS network automation:

1. **Terraform** — defines infrastructure as code. One command creates an entire network.
2. **Python boto3** — automates, manages, and reports on AWS infrastructure programmatically.

Together they cover the full workflow a cloud/DevOps engineer uses at a real company.

---

## Architecture

The following network infrastructure is automated by this project:
VPC (10.0.0.0/16)
├── Public Subnet (10.0.1.0/24) — us-east-1a
│   └── Route Table → Internet Gateway → Internet
├── Private Subnet (10.0.2.0/24) — us-east-1b
│   └── No internet access (isolated and secure)
├── Security Group
│   ├── Inbound: Allow HTTP (port 80) from anywhere
│   ├── Inbound: Allow HTTPS (port 443) from anywhere
│   └── Outbound: Allow all traffic
└── Internet Gateway
└── Connects VPC to the public internet
---

## Tools and Technologies

| Tool | Purpose |
|------|---------|
| Terraform | Infrastructure as Code — defines and deploys AWS resources |
| Python 3 | Scripting and automation |
| boto3 | Official AWS SDK for Python — talks to AWS API |
| LocalStack | Runs a fake AWS environment locally — no cloud account needed |
| Docker | Required to run LocalStack |
| Git | Version control |

---

## Project Structure
aws-network-automation/
├── terraform/
│   └── main.tf           # Complete VPC infrastructure as code
├── python/
│   ├── vpc_manager.py    # Lists all VPCs, subnets, security groups
│   └── network_automation.py  # Fully automated network builder
└── .gitignore
---

## Getting Started

### Prerequisites
- Docker installed and running
- Terraform installed
- Python 3 installed
- LocalStack installed (`pipx install localstack`)

### 1. Start LocalStack
```bash
localstack start
```
Wait for `Ready.` — this starts your local AWS environment.

### 2. Clone this repo
```bash
git clone https://github.com/MrWater00/aws-network-automation.git
cd aws-network-automation
```

### 3. Set up Python environment
```bash
cd python
python3 -m venv venv
source venv/bin/activate
pip install boto3
```

---

## Usage

### Option 1 — Terraform (Infrastructure as Code)

```bash
cd terraform
terraform init      # Download AWS provider plugin
terraform plan      # Preview what will be created
terraform apply     # Create the infrastructure
```

After apply you will have a full VPC network running in LocalStack.

To destroy everything when done:
```bash
terraform destroy
```

### Option 2 — Python Automation Script

Run the full automated network builder:
```bash
cd python
source venv/bin/activate
python3 network_automation.py
```

This will:
- Create a VPC
- Create public and private subnets
- Create and attach an internet gateway
- Create a security group with HTTP/HTTPS rules
- Print a full network report at the end

Example output:
==================================================
Building Network: startup-network
[ 1/5 ] Creating VPC...
VPC created: vpc-f2745a259fa3f3f84
[ 2/5 ] Creating Public Subnet...
Public Subnet created: subnet-e42d3fef55681f910
[ 3/5 ] Creating Private Subnet...
Private Subnet created: subnet-3be0aafb4ba71f701
[ 4/5 ] Creating Internet Gateway...
Internet Gateway created and attached: igw-27cabdb4458196f73
[ 5/5 ] Creating Security Group...
Security Group created: sg-09ed7d95c4470062e
==================================================
NETWORK REPORT — 2026-05-27 00:33:46
Network Name   : startup-network
VPC ID         : vpc-f2745a259fa3f3f84
VPC CIDR       : 10.1.0.0/16
Public Subnet  : subnet-e42d3fef55681f910 (10.1.1.0/24)
Private Subnet : subnet-3be0aafb4ba71f701 (10.1.2.0/24)
Internet GW    : igw-27cabdb4458196f73
Security Group : sg-09ed7d95c4470062e
Status: NETWORK READY ✓
To list all existing infrastructure:
```bash
python3 vpc_manager.py
```

