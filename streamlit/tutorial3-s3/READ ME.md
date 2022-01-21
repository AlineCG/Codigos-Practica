tutorial 1 https://www.youtube.com/watch?v=XGcoeEyt2UM
	minute 13:50 (create bucket)
  
Tutorial 2 https://www.youtube.com/watch?v=NHAuCWIHevk
       (connect bucket with ec2)
       
Tutorial 3 https://www.data-stats.com/how-to-read-s3-files-from-ec2-using-python/
	steps 5 y 6 to connect s3 with python 


<pre>      
Main idea: To Create a bucket in S3 and run our streamlit web app in EC2 
           that access to those S3 files.
	   
</pre>  

STEPS:


#### STEP 1: Tutorial 1 (CREATE S3 Bucket)

1) Go to AWS Console select S3 and create bucket.
 
2) Create name for the bucket that is unique in all internet then click create

3) Add any file (ex: footbal_data.csv)

#### STEP 2: Tutorial 2 (connecting S3 to EC2)

1) Go to IAM, create a new role for EC2, policy: S3FullAccess.
 
2) GO to instances, select the instance, actions, security, modify role for the one created before. 
 
3) Access to Instance Terminal (via SSH) and run aws s3 ls  \
 &emsp;&emsp;    (sudo apt install awscli if its not installed)
 
      
#### STEP 3: Tutorial 3 (streamlit app access to bucket data)
1)  pip3 install pandas \
    pip3 install s3fs \
    pip3 install boto3 
2) add this lines in python code:
 &emsp;&emsp; &emsp;&emsp; import pandas as pd \
 &emsp;&emsp; &emsp;&emsp; import boto3 \
 &emsp;&emsp; &emsp;&emsp; client = boto3.client('s3') \
 &emsp;&emsp; &emsp;&emsp; path='s3://Your_bucket_name/Your_file_name' \
 &emsp;&emsp; &emsp;&emsp; df=pd.read_csv(path) 
 
 3) python run example.py (Ex: streamlit run helloworlds3.py)


#### S3 COMMANDS: 
https://docs.aws.amazon.com/es_es/cli/latest/userguide/cli-services-s3-commands.html#using-s3-commands-listing-buckets \

- aws s3 ls
 - aws s3 ls s3://testbucket/ \
&emsp;&emsp;	shows with  PRE all folders in bucket 
 - aws s3 ls s3://testbucket/testfolder/	 
 - aws s3 cp testfile.txt s3://testbucket/testfolder/testfile.txt \
&emsp;&emsp; copy from virtual machine in ec2 to bucket in s3
 - aws s3 cp s3://testbucket-lanek-0/carpeta0/holi.txt holi2.txt \ 
 &emsp;&emsp; copy from bucket to virtual machine
 - aws s3 mb s3://newbucket  \
 &emsp;&emsp; create new bucket
 - aws s3 rb s3://newbucket \
  &emsp;&emsp; delete bucket or file

note: (for adding files to ec2 instance)\
pscp -i C:\path\my-key-pair.ppk C:\path\Sample_file.txt my-instance-user-name@my-instance-public-dns-name:/home/my-instance-user-name/Sample_file.txt 


