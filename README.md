## Welcome to Guilherme Rettore Andreis Porfolio

# Project 1: Chest x-Ray Pneumonia Classifier

Created a deep learning neural network (DLNN) that classifies Chest X-Rays images within normal an pneumonia categories to help medical diagnosis in time and assertieness.
Developed a FLASK API to serve as interface with users.
![flask api](/images_read_me/flask_api2.PNG) ![results_api](/images_read_me/results_api2.PNG)


In order to reach the best result the DLNN used a ResNet18 backbone and was trained using the [kaggle Chest X-Ray pneumonia dataset](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia). The figures below show the results of the confusion matrix and a batch of the test dataset used to train the network.

![confusion matrix ](/images_read_me/confusion_matrix3.png)
![batch_result](/images_read_me/batch_result_final.png)

In order to make the DLNN more explainable to physicians the Gradcam was developed to try to demonstrate what parts of the images the DLNN is "looking" and atribuiting greater weights in the classification results, the input image and the highlighted points by the model with Gradcam is shown bellow.
![Original image](/images_read_me/cheast_image1.png)
![Gradcam over image](/images_read_me/gradcam_heatmap1.png)



