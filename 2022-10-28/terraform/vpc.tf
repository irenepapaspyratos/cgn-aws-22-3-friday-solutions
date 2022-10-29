resource "aws_vpc" "jobs-api-vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "Jobs API VPC"
  }
}

resource "aws_subnet" "public_subnet" {
  vpc_id     = aws_vpc.jobs-api-vpc.id
  cidr_block = "10.0.1.0/24"

  tags = {
    Name = "Public Subnet"
  }
}

resource "aws_subnet" "private_subnet" {
    vpc_id     = aws_vpc.jobs-api-vpc.id
    cidr_block = "10.0.2.0/24"

    tags = {
        Name = "Private Subnet"
    }
}


resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.jobs-api-vpc.id
}

resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.jobs-api-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    Name = "Public Route Table"
  }
}

resource "aws_route_table_association" "public_subnet_association" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_route_table.id
}

resource "aws_security_group" "ssh_http_security" {
  name        = "allow_http_ssh"
  description = "Allow HTTP and SSH"
  vpc_id      = aws_vpc.jobs-api-vpc.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

    ingress {
        description      = "TLS from VPC"
        from_port        = 443
        to_port          = 443
        protocol         = "tcp"
        cidr_blocks      = [aws_vpc.jobs-api-vpc.cidr_block]
    }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "allow_http_ssh"
  }
}