resource "aws_instance" "instance_20221021" {
  ami                         = "ami-0d593311db5abb72b"
  instance_type               = "t3.micro"
  associate_public_ip_address = true
  subnet_id                   = aws_subnet.subnetPublic_20221021.id
  vpc_security_group_ids      = [aws_security_group.securityGroup_20221021.id]
  key_name                    = "vockey"
  user_data = file("userdata.sh")
  tags = {
    Name = "instance-20221021"
  }
}