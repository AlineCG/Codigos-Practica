Tutorial 2:\
	https://towardsdatascience.com/how-to-deploy-a-streamlit-app-using-an-amazon-free-ec2-instance-416a41f69dc3
	
Tutorial 2.1: SSH Connetion for windows (use PuTTY) \
	https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html
<pre>      
Main idea: To Create a EC2 server (virtual machine) to run our streamlit web app. 
           We also use TMUX library for keeping the code running in the background.
	   
</pre>  

STEPS:


#### STEP 1: Tutorial 1 (CREATE EC2 Instance)

1) Go to AWS Console select EC2 and launch instance.
 
2) Select AMI (ubuntu 18.04 (free tier)), next until security group.
 
3) Add custom TCP with port range 8501, click review and launch
 
4) Create a new key pair, add new name and download .pem file (KEEP IN SECURE LOCATION)
 
5) Launch instance

#### STEP 2: Tutorial 2 (connecting with SSH to EC2)

1) Download PuTTY
 
2) Run PuTTYgen software, select RSA and then click load, choose the .pem file click OPEN and OK.
 
3) click Save Private Key, yes, add new name and Save.
 
&emsp; Now We have the .ppk key
 
4) Run PuTTY
 
5) In Session category: \
&emsp;&emsp;      in HOST NAME box goes  my-instance-user-name@my-instance-public-dns-name. (default instance user name is ubuntu)\
&emsp;&emsp;      in PORT box goes 22\
&emsp;&emsp;      in connection type SSH\
&emsp;&emsp;      more info:  https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connection-prereqs.html#connection-prereqs-get-info-about-instance 
 \     
6) In Connection/SSH/Auth category:\
 &emsp;&emsp;     browse for the .ppk key and open \
 
note: In Connection category: Seconds between keepalives field goes 180\ 
     also, save the session in Session category with a name
 
7) click open and we are connected to the EC2 instance (virtual machine)
 
8) to send file from our computer to ec2 instance, in cmd run:\
 &emsp;	pscp -i C:\path\my-key-pair.ppk C:\path\Sample_file.txt my-instance-user-name@my-instance-public-dns-name:/home/my-instance-user-name/Sample_file.txt \
 &emsp; might need step 4     
      
#### STEP 3: Tutorial 1 (run streamlit in the background)

1) sudo apt-get update 
2) wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
3) bash ~/miniconda.sh -b -p ~/miniconda
4) echo "PATH=$PATH:$HOME/miniconda/bin" >> ~/.bashrc
5) source ~/.bashrc

6) pip3 install streamlit and run: streamlit helloworld.py

7) sudo apt-get install tmux

8) tmux new -s StreamSession

9) streamlit helloworld.py will be running in the StreamSession

10) ctrl+B then D (not simultaneously) now the session is detatched and we can disconnect without killing it.

#### TMUX COMMANDS 

*tmux new -s Session0* \
*tmux detach* \
*tmux list-sessions*   (para ver todas las sessiones) \
*tmux attach -t Session0* \
*tmux kill-session*    (para borrar todas las sesiones) 
      
#### STEP 4: (optional)  (connect AWS with computer to send files)
1) install awscli for windows
2) run in cmd: aws configure \
    AWS Access Key ID [None]: write private key \
    AWS Secret Access Key [None]: write public key \
    Default region name [None]: us-east-2 \
    Default output format [None]: blank
    



  
  
