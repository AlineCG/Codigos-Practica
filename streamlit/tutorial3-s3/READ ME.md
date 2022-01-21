tutorial 1 https://www.youtube.com/watch?v=XGcoeEyt2UM
	minuto 13:50 (crear bucket)
  
Tutorial 2 https://www.youtube.com/watch?v=NHAuCWIHevk
       (conectar bucket con ec2)
       
https://www.data-stats.com/how-to-read-s3-files-from-ec2-using-python/
	paso 5 y 6 para conectar s3 con python 


<pre>      
Main idea: To Create a bucket in S3 and run our streamlit web app in EC2 
           that access to those S3 files.
	   
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
 &emsp;&emsp;     browse for the .ppk key and open
 
7) click open and we are connected to the EC2 instance (virtual machine)
 
8) to send file from our computer to ec2 instance, in cmd run:\
 &emsp;	pscp -i C:\path\my-key-pair.ppk C:\path\Sample_file.txt my-instance-user-name@my-instance-public-dns-name:/home/my-instance-user-name/Sample_file.txt \
 &emsp; might need step 4     
      
#### STEP 3: Tutorial 1 (run streamlit in the background)
1) sudo apt-get update

2) pip install streamlit and run: streamlit helloworld.py

3) sudo apt-get install tmux

4) tmux new -s StreamSession

5) streamlit helloworld.py will be running in the StreamSession

6) ctrl+B then D (not simultaneously) now the session is detatched and we can disconnect without killing it.

#### TMUX COMMANDS 

*tmux new -s Session0* \
*tmx detach* \
*tmux list-sessions*   (para ver todas las sessiones) \
*tmux attach -t Session0* \
*tmux kill-session*    (para borrar todas las sesiones) 
      
#### STEP 4: (optional)  (connect AWS with computer)
1) install awscli for windows
2) run in cmd: aws configure \
    AWS Access Key ID [None]: write private key \
    AWS Secret Access Key [None]: write public key \
    Default region name [None]: us-east-2 \
    Default output format [None]: blank


