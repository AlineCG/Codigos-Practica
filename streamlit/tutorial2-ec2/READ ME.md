Tutorial 2:
	https://towardsdatascience.com/how-to-deploy-a-streamlit-app-using-an-amazon-free-ec2-instance-416a41f69dc3
	
Tutorial 2.1: SSH Connetion for windows (use PuTTY) 
	https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html
  
Main idea: Create a EC2 server (virtual machine) to run streamlit web app. 

           We also use TMUX library for keeping the code running in the background.

STEPS:


1) TUTORIAL 1 (CREATE EC2 Instance)

 1.1) Go to AWS Console select EC2 and launch instance.
 1.2) Select AMI (ubuntu 18.04 (free tier)), next until security group.
 1.3) Add custom TCP with port range 8501, click review and launch
 1.4) Create a new key pair, add new name and download .pem file (KEEP IN SECURE LOCATION)
 1.5) Launch instance

2) Tutorial 2 (connecting with SSH to EC2)

 2.1) Download PuTTY
 2.2) Run PuTTYgen software, select RSA and then click load, choose the .pem file click OPEN and OK.
 2.3) click Save Private Key, yes, add new name and Save.
 Now We have the .ppk key
 
 2.4) Run PuTTY
 2.5) In Session category: 
      in HOST NAME box goes  my-instance-user-name@my-instance-public-dns-name. (default instance user name is ubuntu)
      in PORT box goes 22
      in connection type SSH
      more info:  https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connection-prereqs.html#connection-prereqs-get-info-about-instance
 2.6)In Connection/SSH/Auth category:
      browse for the .ppk key and open
 2.7) click open and we are connected to the EC2 instance (virtual machine)
 
 2.8) to send file from our computer to ec2 instance, in cmd run:
 	pscp -i C:\path\my-key-pair.ppk C:\path\Sample_file.txt my-instance-user-name@my-instance-public-dns-name:/home/my-instance-user-name/Sample_file.txt
      
      
      



  
  
