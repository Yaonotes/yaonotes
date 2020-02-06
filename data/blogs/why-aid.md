title: AID Story
datetime: 26 Dec 2019
summary: The reasons why I make AID, what it is and what it is going to be.
-------

There are many issues we've faced in our process of deploying computer vision models. In the past two years, we have encountered the problems such as:

* There are many different algorithms and open source code with different entries, test code and dataset. Reproducing their results is time-consuming, and sometimes impossible.
* When deploying our models to production, we need several days debugging with our program, environment, dependencies, etc. It cost us too much time than we expected. 
* We're working on an annotating platform, and the platform is supposed to give suggestions on dataset. However, the apis from Google, Amazon, Microsoft are different and require us learn from their docs.
* When we want to distribute our code to customers, but they do not like http calls to our server as they do not want to share the data with us.
* and more!

To tackle these problems, we proposed A.I.D, which helps us manage, share