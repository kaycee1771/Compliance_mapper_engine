resource "aws_iam_role" "readonly" {
  name = "readonly-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
  permissions_boundary = "arn:aws:iam::123456789012:policy/ReadOnlyAccess"
}