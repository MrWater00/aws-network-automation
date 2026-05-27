import boto3
import json
from datetime import datetime

# Connect to LocalStack
ec2 = boto3.client(
    'ec2',
    region_name='us-east-1',
    aws_access_key_id='fake',
    aws_secret_access_key='fake',
    endpoint_url='http://localhost:4566'
)

def create_network(vpc_name, vpc_cidr, public_cidr, private_cidr):
    print(f"\n{'='*50}")
    print(f"  Building Network: {vpc_name}")
    print(f"{'='*50}\n")

    # Step 1 - Create VPC
    print("[ 1/5 ] Creating VPC...")
    vpc = ec2.create_vpc(CidrBlock=vpc_cidr)
    vpc_id = vpc['Vpc']['VpcId']
    ec2.create_tags(Resources=[vpc_id], Tags=[{'Key': 'Name', 'Value': vpc_name}])
    print(f"        VPC created: {vpc_id}")

    # Step 2 - Create Public Subnet
    print("[ 2/5 ] Creating Public Subnet...")
    pub_subnet = ec2.create_subnet(
        VpcId=vpc_id,
        CidrBlock=public_cidr,
        AvailabilityZone='us-east-1a'
    )
    pub_subnet_id = pub_subnet['Subnet']['SubnetId']
    ec2.create_tags(Resources=[pub_subnet_id], Tags=[{'Key': 'Name', 'Value': f'{vpc_name}-public'}])
    print(f"        Public Subnet created: {pub_subnet_id}")

    # Step 3 - Create Private Subnet
    print("[ 3/5 ] Creating Private Subnet...")
    priv_subnet = ec2.create_subnet(
        VpcId=vpc_id,
        CidrBlock=private_cidr,
        AvailabilityZone='us-east-1b'
    )
    priv_subnet_id = priv_subnet['Subnet']['SubnetId']
    ec2.create_tags(Resources=[priv_subnet_id], Tags=[{'Key': 'Name', 'Value': f'{vpc_name}-private'}])
    print(f"        Private Subnet created: {priv_subnet_id}")

    # Step 4 - Create Internet Gateway and attach to VPC
    print("[ 4/5 ] Creating Internet Gateway...")
    igw = ec2.create_internet_gateway()
    igw_id = igw['InternetGateway']['InternetGatewayId']
    ec2.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
    ec2.create_tags(Resources=[igw_id], Tags=[{'Key': 'Name', 'Value': f'{vpc_name}-igw'}])
    print(f"        Internet Gateway created and attached: {igw_id}")

    # Step 5 - Create Security Group
    print("[ 5/5 ] Creating Security Group...")
    sg = ec2.create_security_group(
        GroupName=f'{vpc_name}-web-sg',
        Description='Allow HTTP and HTTPS',
        VpcId=vpc_id
    )
    sg_id = sg['GroupId']

    # Add inbound rules
    ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            },
            {
                'IpProtocol': 'tcp',
                'FromPort': 443,
                'ToPort': 443,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            }
        ]
    )
    print(f"        Security Group created: {sg_id}")

    # Final Report
    print(f"\n{'='*50}")
    print(f"  NETWORK REPORT — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")
    print(f"  Network Name   : {vpc_name}")
    print(f"  VPC ID         : {vpc_id}")
    print(f"  VPC CIDR       : {vpc_cidr}")
    print(f"  Public Subnet  : {pub_subnet_id} ({public_cidr})")
    print(f"  Private Subnet : {priv_subnet_id} ({private_cidr})")
    print(f"  Internet GW    : {igw_id}")
    print(f"  Security Group : {sg_id}")
    print(f"{'='*50}")
    print(f"  Status: NETWORK READY ✓")
    print(f"{'='*50}\n")

# Run it
create_network(
    vpc_name="startup-network",
    vpc_cidr="10.1.0.0/16",
    public_cidr="10.1.1.0/24",
    private_cidr="10.1.2.0/24"
)
