title: Face Detection with Viola Jones Method
datetime: 27 Nov 2019
summary: This article introduces viola-jones method.
-------

For a face recognition application, it will usually includes several steps, such as:

* Face Detection: Detect where the face is in a large image.
* Landmark Detection: Detect facial landmarks, such as eyes, mouth, etc.
* Face Recognition: Find the map between face image and its corresponding person id.
* Face Information Recognition: Extract/Predict information by the given image, such as age, gender, etc.

In this article, we only introduce an "old" face detection method: Viola-Jones method, which is the algorithm used by OpenCV for face detection, at least in 2.4. There are three key components for Viola-Jones method: Haar-like features, Adaboost and Cascade classifiers.

## Haar-like features

![5316411-b013ac3de86151b2.jpg](https://i.loli.net/2019/11/29/siBFVt4Zr9ENpmX.jpg)

As seen above, a rectangular haar-like feature can be defined as the difference of the sum of pixels of areas inside a rectangle, i.e. ```feature=sum(white)-sum(black)```. 