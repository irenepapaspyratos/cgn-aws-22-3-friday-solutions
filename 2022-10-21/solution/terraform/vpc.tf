resource "aws_vpc" "vpc_20221021" {
    cidr_block = "10.0.0.0/16"
    tags = {
        Name = "vpc-20221021"
    } 
}

resource "aws_subnet" "subnetPublic_20221021" {
    vpc_id     = aws_vpc.vpc_20221021.id
    cidr_block = "10.0.0.0/24"
    tags = {
        Name = "subnet-public-20221021-01"
    }
}

resource "aws_subnet" "subnetPrivate_20221021-01" {
    vpc_id     = aws_vpc.vpc_20221021.id
    cidr_block = "10.0.1.0/24"
    tags = {
        Name = "subnet-private-20221021-01"
    }
}

resource "aws_nat_gateway" "vpcPrivateNat" {
    connectivity_type = "private"
    subnet_id         = aws_subnet.subnetPrivate_20221021-01.id
    tags = {
        Name = "vpc-private-Nat"
    }
}

resource "aws_internet_gateway" "vpcWebGateway" {
    vpc_id = aws_vpc.vpc_20221021.id
    tags = {
        Name = "vpc-web-gateway"
    }
}

resource "aws_route_table" "publicRouteTable" {
    vpc_id = aws_vpc.vpc_20221021.id
    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.vpcWebGateway.id
    }
    tags = {
        Name = "public-route-table"
    }
}

resource "aws_route_table_association" "publicSubnetRouteTableAssociation" {
    subnet_id      = aws_subnet.subnetPublic_20221021.id
    route_table_id = aws_route_table.publicRouteTable.id
}

resource "aws_security_group" "securityGroup_20221021" {
    name        = "securityGroup-20221021"
    description = "SecurityGroupThursday allows tls usw."
    vpc_id      = aws_vpc.vpc_20221021.id

    ingress {
        description     = "SSH"
        from_port       = 22
        to_port         = 22
        protocol        = "tcp"
        cidr_blocks     = ["0.0.0.0/0"]
    }

    ingress {
        description      = "TLS from VPC"
        from_port        = 443
        to_port          = 443
        protocol         = "tcp"
        cidr_blocks      = [aws_vpc.vpc_20221021.cidr_block]
    }

    ingress {
        description      = "HTTP from VPC"
        from_port        = 80
        to_port          = 80
        protocol         = "tcp"
        cidr_blocks      = [aws_vpc.vpc_20221021.cidr_block]
    }

    egress {
        from_port        = 0
        to_port          = 0
        protocol         = "-1"
        cidr_blocks      = ["0.0.0.0/0"]
    }

    tags = {
        Name = "security-group-20221021"
    }
}