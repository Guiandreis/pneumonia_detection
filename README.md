
# Project 1: Chest X-ray Pneumonia Classifier

## Summary

**Developed a deep learning neural network (DLNN) that classifies Chest X-Rays images within normal and pneumonia categories to help medical diagnosis in time and assertiveness, using Flask for API connections, AWS EC2 for processing and AWS S3 for data storage.**

**Tools: Python, Flask, Pytorch, AWS EC2, AWS S3, Paramiko**

Developed a FLASK API to serve as the interface with users.
<p align="center">
  <img src="images_read_me/flask_api2.PNG" width="425" height="250">
  <img src="images_read_me/result_api2.PNG" width="425" height="250">
</p>
 
In order to reach the best result, the DLNN trained using the [kaggle Chest X-Ray pneumonia dataset](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia). The figures below show the results of the confusion matrix and a batch of the test dataset used to train the network.

<p align="center">
  <img src="images_read_me/confusion_matrix4.png" width="425" height="450">
  <img src="images_read_me/batch_result2.png" width="425" height="450">
</p>

# Table of contents
1.[How to Use](#How-to-Use)

2.[Data Exploratory Analisys](#Exploratory-Data-Analisys)

3.[Neural Network Development](#Neural-Network-Development)

4.[AWS Configuration](#AWS-Configuration)


5.[Future Implementation](#Future-Implementation)


## How to Use
Clone this git repo 

## Exploratory Data Analisys
This session describe the Exploratory Data Analisys performed

## Neural Network Development
This session describes the Neural Network Development

## AWS Configuration

  To configure the AWS settings enter the [aws_settings file](aws_files_config/aws_settings.py). To configure the EC2 instance, inside the *ec2_configuration_dict* function in the *dict_create_instance* pass the required information to create a new AWS instance, the required informatio is: Name of the instance, AMD ID, Instance type,  User Data, Key pair name and AWS Region which corresponds to the variables called name of the instance in the AWS, image of the the AWS instances, the type of the instance to be selected, the data that will be passed, the key pair to access this instance via SSH and the region to create the instance.
  
  To configure the EC2 bucket, inside the *s3_configuration_dict* pass the bucket_region and the NAME_S3_BUCKET which corresponds to the region to create the bucket and the name of the bucket. Please do not change any variable not citated in this configuration content. 
  
  
## Future Implementation
This session describes the future implementation for this project.



