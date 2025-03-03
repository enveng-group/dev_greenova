# System Architecture

## Overview
Documentation on the System Architecture of a Django-based environmental obligations management system.

## Software Components

### Backend
- Django 5.1.6
- SQLite3 Database
- MatPlotlib for data visualization

### Frontend
- HTMX for dynamic interactions
- PicoCSS for styling
- Hyperscript for enhanced interactivity

## Data Flow
1. User Authentication
2. Obligations Processing
3. Reporting Pipeline

## Infrastructure Architecture

### Name
enssol-app-prod-001

#### Tags
- **Environment**: Production
- **Application**: EnssolApp
- **Project**: EnvObligations
- **Owner**: AGallo_Admin
- **CostCentre**: ENV-PROD-001
- **BackupPolicy**: Daily
- **SecurityGroup**: WebApplication
- **AutoShutdown**: No
- **Domain**: app.enssol.com.au

### Cloud Provider
- **Provider**: AWS (Amazon Web Services)
- **Region**: Sydney (ap-southeast-2)
- **Account Structure**: Production and Development accounts with AWS Organizations

### Compute Resources
- **EC2 Instance Type**: t2.nano (1 vCPU, 0.5 GB RAM)
- **CPU Credits**: Standard
- **AMI ID**: ami-0b87a8055f0211d32 (Ubuntu Pro 16.04 LTS)
- **Elastic IP**: 13.238.199.122

### Storage
- **Application Storage**: EBS standard volumes (8GB per instance)

### Database
- **Primary Database**: SQLite3 (hosted on EBS volume)
- **Backup Strategy**: Daily snapshots to GitHub

### Networking
- **VPC Configuration**:
  - VPC ID: vpc-038e672b8234f1858
  - CIDR: 10.0.0.0/16
  - Public Subnets: 10.0.1.0/24, 10.0.2.0/24
  - Private Subnets: 10.0.3.0/24, 10.0.4.0/24
- **Security Groups**:
  - Allow all traffic from the internet to the application

### DNS Configuration
- **Domain**: app.enssol.com.au
- **DNS Provider**: Route 53
- **Subdomains**:
  - app.enssol.com.au (Production)
  - staging.enssol.com.au (Staging)
  - dev.enssol.com.au (Development)

## Infrastructure as Code

### AWS CLI Commands
```bash
aws ec2 create-security-group --group-name "enssol-web-prod-sg" \
  --description "Enssol Web Application Security Group - Production Manages network access for Django environmental obligations system. Controls traffic to EC2 instances serving the app.enssol-env.com.au domain." \
  --vpc-id "vpc-038e672b8234f1858"

aws ec2 authorize-security-group-ingress --group-id "sg-preview-1" \
  --ip-permissions '{"IpProtocol":"-1","FromPort":-1,"ToPort":-1,"IpRanges":[{"CidrIp":"0.0.0.0/0","Description":"Allow all IP addresses to access the instance"}]}'

aws ec2 run-instances --image-id "ami-0b87a8055f0211d32" \
  --instance-type "t2.nano" \
  --instance-initiated-shutdown-behavior "stop" \
  --key-name "enssol-prod-ap-southeast-2-key" \
  --block-device-mappings '{"DeviceName":"/dev/sda1","Ebs":{"Encrypted":false,"DeleteOnTermination":true,"SnapshotId":"snap-06e32d71bf3127195","VolumeSize":8,"VolumeType":"standard"}}' \
  --network-interfaces '{"SubnetId":"subnet-01344c7dbe4c656f8","DeleteOnTermination":true,"Description":"Primary network interface for Enssol environmental obligations application - Production environment","AssociatePublicIpAddress":false,"DeviceIndex":0,"Groups":["sg-preview-1"]}' \
  --hibernation-options '{"Configured":false}' \
  --monitoring '{"Enabled":false}' \
  --credit-specification '{"CpuCredits":"standard"}' \
  --capacity-reservation-specification '{"CapacityReservationPreference":"none"}' \
  --network-performance-options '{"BandwidthWeighting":"default"}' \
  --tag-specifications '{"ResourceType":"instance","Tags":[{"Key":"Name","Value":"enssol-app-prod-001"},{"Key":"Environment","Value":"Production"},{"Key":"Application","Value":"EnssolApp"},{"Key":"Project","Value":"EnvObligations"},{"Key":"Owner","Value":"AGallo_Admin"},{"Key":"CostCentre","Value":"ENV-PROD-001"},{"Key":"BackupPolicy","Value":"Daily"},{"Key":"SecurityGroup","Value":"WebApplication"},{"Key":"AutoShutdown","Value":"No"},{"Key":"Domain","Value":"app.enssol.com.au"}]}' \
  --iam-instance-profile '{"Arn":"arn:aws:iam::381492266447:instance-profile/EC2"}' \
  --metadata-options '{"HttpEndpoint":"enabled","HttpTokens":"required","InstanceMetadataTags":"enabled"}' \
  --placement '{"Tenancy":"default"}' \
  --private-dns-name-options '{"HostnameType":"resource-name","EnableResourceNameDnsARecord":true,"EnableResourceNameDnsAAAARecord":false}' \
  --maintenance-options '{"AutoRecovery":"default"}' \
  --count "1"
```

## Deployment Environment

### Operating System
- **Distribution**: Ubuntu Pro 16.04 LTS
- **Kernel Requirements**: 4.4 or higher

## Security Architecture

### Authentication
- Django authentication system with MFA support
- AWS IAM for infrastructure access

### Authorization
- Role-based access control for application features
- Least privilege principle for AWS services

### Data Protection
- TLS 1.3 for all communications
- Data encryption at rest using AWS KMS
- Regular security patches and updates

### Security Concerns
- Consider restricting SSH access to specific IP ranges or using a bastion host
- SSH access is currently allowed from any IP (0.0.0.0/0) which presents a security risk

## Backup and Disaster Recovery

### Backup Strategy
- Daily database backups to S3
- Weekly full system backups
- 30-day retention period

### Disaster Recovery
- Documented disaster recovery procedures
- RTO (Recovery Time Objective): 4 hours
- RPO (Recovery Point Objective): 24 hours

## Scaling Strategy

### Vertical Scaling
- EC2 instance type upgrades as needed (current: t2.nano)
- Database resource allocation increases

### Horizontal Scaling
- Auto Scaling Groups for application tier
- Read replicas for database (future implementation)

## Network Paths and Data Flow

### External Request Flow
1. User Request → CloudFront → ALB → Nginx → Gunicorn → Django Application
2. API Request → ALB → Nginx → Gunicorn → Django REST Framework

### Internal Service Communication
1. Application → Database: Direct connection within VPC
2. Application → S3: Via VPC Endpoint
3. Application → External APIs: Via NAT Gateway

## Database Schema
[Include core database schema documentation]

## Future Enhancements
- Restrict SSH access to specific IP ranges for improved security
- Migration to container-based deployment with ECS/EKS
- Implementation of database read replicas for scaling
- Integration with AWS Organizations for multi-account management
