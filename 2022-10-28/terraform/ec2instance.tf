resource "aws_instance" "jobs_api_instance" {
  ami                         = "ami-08e2d37b6a0129927"
  instance_type               = "t3.micro"
  associate_public_ip_address = true
  subnet_id                   = aws_subnet.public_subnet.id
  vpc_security_group_ids      = [aws_security_group.ssh_http_security.id]
  key_name                    = "vockey"
  user_data = file("userdata.sh")
  
  tags = {
    Name = "Jobs API instance"
  }
}