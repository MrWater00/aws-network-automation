import boto3

ec2 = boto3.client(
    'ec2',
    region_name='us-east-1',
    aws_access_key_id='fake',
    aws_secret_access_key='fake',
    endpoint_url='http://localhost:4566'
)

def list_vpcs():
    response = ec2.describe_vpcs()
    vpcs = response['Vpcs']
    print(f"\n Total VPCs found: {len(vpcs)}\n")
    for vpc in vpcs:
        vpc_id = vpc['VpcId']
        cidr = vpc['CidrBlock']
        state = vpc['State']
        name = "No Name"
        for tag in vpc.get('Tags', []):
            if tag['Key'] == 'Name':
                name = tag['Value']
        print(f"  Name  : {name}")
        print(f"  ID    : {vpc_id}")
        print(f"  CIDR  : {cidr}")
        print(f"  State : {state}")
        print(f"  ------")

def list_subnets():
    response = ec2.describe_subnets()
    subnets = response['Subnets']
    print(f"\n Total Subnets found: {len(subnets)}\n")
    for subnet in subnets:
        subnet_id = subnet['SubnetId']
        cidr = subnet['CidrBlock']
        vpc_id = subnet['VpcId']
        az = subnet['AvailabilityZone']
        name = "No Name"
        for tag in subnet.get('Tags', []):
            if tag['Key'] == 'Name':
                name = tag['Value']
        print(f"  Name  : {name}")
        print(f"  ID    : {subnet_id}")
        print(f"  CIDR  : {cidr}")
        print(f"  VPC   : {vpc_id}")
        print(f"  Zone  : {az}")
        print(f"  ------")

def list_security_groups():
    response = ec2.describe_security_groups()
    groups = response['SecurityGroups']
    print(f"\n Total Security Groups found: {len(groups)}\n")
    for sg in groups:
        sg_id = sg['GroupId']
        name = sg['GroupName']
        vpc_id = sg['VpcId']
        print(f"  Name  : {name}")
        print(f"  ID    : {sg_id}")
        print(f"  VPC   : {vpc_id}")
        print(f"  ------")

list_vpcs()
list_subnets()
list_security_groups()
