# AWS Network Automation

Infrastructure automation for AWS VPC networking using Terraform and Python (boto3). This project provisions a complete, production-style network environment — VPC, public and private subnets, security groups, internet gateway, and route tables — entirely through code.

Tested locally using [LocalStack](https://localstack.cloud), eliminating the need for a live AWS account during development.

---

## Overview

Manual cloud infrastructure setup doesn't scale. This project demonstrates how network engineers automate repeatable AWS environments using two industry-standard approaches:

- **Terraform** provisions the full network stack from a single configuration file
- **Python (boto3)** interacts with the AWS API to automate resource creation and generate infrastructure reports

The combination reflects the real workflow used by cloud and DevOps engineers at technology companies.

---

## Network Architecture

```
VPC — 10.0.0.0/16
│
├── Public Subnet — 10.0.1.0/24 (us-east-1a)
│   └── Route Table → Internet Gateway → Internet
│
├── Private Subnet — 10.0.2.0/24 (us-east-1b)
│   └── Isolated — no inbound or outbound internet access
│
├── Security Group
│   ├── Inbound  — TCP port 80  (HTTP)  from 0.0.0.0/0
│   ├── Inbound  — TCP port 443 (HTTPS) from 0.0.0.0/0
│   └── Outbound — All traffic allowed
│
└── Internet Gateway
    └── Attached to VPC, associated with public subnet route table
```

---

## Tech Stack

| Technology | Role |
|---|---|
| Terraform | Defines and provisions AWS infrastructure as code |
| Python 3 | Scripting and API-based automation |
| boto3 | AWS SDK for Python — interfaces with the AWS API |
| LocalStack | Emulates AWS services locally for development and testing |
| Docker | Required runtime for LocalStack |

---

## Repository Structure

```
aws-network-automation/
│
├── terraform/
│   └── main.tf                  # Full network infrastructure definition
│
├── python/
│   ├── vpc_manager.py           # Query and display existing VPCs, subnets, and security groups
│   └── network_automation.py   # End-to-end automated network provisioning script
│
└── .gitignore
```

---

## Prerequisites

Ensure the following are installed before getting started:

- [Docker](https://docs.docker.com/get-docker/)
- [Terraform](https://developer.hashicorp.com/terraform/install)
- [Python 3](https://www.python.org/downloads/)
- [LocalStack](https://docs.localstack.cloud/getting-started/installation/) — `pipx install localstack`

---

## Getting Started

### 1. Start LocalStack

```bash
localstack start
```

Wait until the terminal displays `Ready.` before proceeding.

### 2. Clone the Repository

```bash
git clone https://github.com/MrWater00/aws-network-automation.git
cd aws-network-automation
```

### 3. Set Up Python Environment

```bash
cd python
python3 -m venv venv
source venv/bin/activate
pip install boto3
```

---

## Usage

### Terraform — Infrastructure as Code

```bash
cd terraform

terraform init    # Install the AWS provider plugin
terraform plan    # Preview resources to be created
terraform apply   # Provision the network infrastructure
```

To tear down all provisioned resources:

```bash
terraform destroy
```

### Python — Automated Network Provisioning

```bash
cd python
source venv/bin/activate
python3 network_automation.py
```

The script provisions a complete network and prints a structured report on completion:

```
==================================================
  Building Network: startup-network
==================================================

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
==================================================
  Network Name   : startup-network
  VPC ID         : vpc-f2745a259fa3f3f84
  VPC CIDR       : 10.1.0.0/16
  Public Subnet  : subnet-e42d3fef55681f910 (10.1.1.0/24)
  Private Subnet : subnet-3be0aafb4ba71f701 (10.1.2.0/24)
  Internet GW    : igw-27cabdb4458196f73
  Security Group : sg-09ed7d95c4470062e
==================================================
  Status: NETWORK READY ✓
==================================================
```

To query all existing infrastructure:

```bash
python3 vpc_manager.py
```

---

## Key Concepts Covered

**VPC (Virtual Private Cloud)**
An isolated private network within AWS. All resources in this project are deployed inside a single VPC with a defined IP address range.

**Public vs Private Subnets**
The public subnet is routed through an internet gateway, making it accessible from the internet. The private subnet has no such route, making it suitable for databases and internal services.

**Security Groups**
Stateful firewall rules attached to resources. This project configures inbound rules for HTTP and HTTPS traffic and allows all outbound communication.

**Internet Gateway and Route Tables**
The internet gateway connects the VPC to the public internet. A route table directs outbound traffic from the public subnet through the gateway.

**Infrastructure as Code**
Terraform allows infrastructure to be defined, versioned, and deployed repeatedly from a single configuration file — eliminating manual setup and human error.

**API-driven Automation**
boto3 interacts directly with the AWS API, enabling dynamic resource creation, tagging, and reporting through Python scripts.

---

## Local Development with LocalStack

All resources in this project are provisioned against [LocalStack](https://localstack.cloud), a fully functional local AWS emulator. This allows complete development and testing without connecting to AWS, incurring costs, or managing credentials.

The Terraform provider and boto3 client are both configured to point to `http://localhost:4566` — LocalStack's default endpoint.
