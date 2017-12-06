| ![Brian Dolhansky](https://static1.squarespace.com/static/51d342a0e4b0290bcc56387d/t/5a25a353e2c48393e585aae9/1512416083021/me.jpg)  |  ![Cristian Canton Ferrer](https://i.imgur.com/XR1kGQw.jpg)
|:-:|:-:|
| [Brian Dolhansky](http://briandolhansky.com) | [Cristian Canton Ferrer](https://cristiancanton.github.io/)

# Introduction

We introduce a novel approach to in-painting where the identity of the object to remove or change is preserved and accounted for at inference time: Exemplar GANs (ExGANs). ExGANs are a type of conditional GAN that utilize exemplar information to produce high-quality, personalized in-painting results. We propose using exemplar information in the form of a reference image of the region to in-paint, or a perceptual code describing that object. Unlike previous conditional GAN formulations, this extra information can be inserted at multiple points within the adversarial network, thus increasing its descriptive power. We show that ExGANs can produce photo-realistic personalized in-painting results that are both perceptually and semantically plausible by applying them to the task of closed-to-open eye in-painting in natural pictures. A new benchmark dataset is also introduced for the task of eye in-painting for future comparisons.

# Celeb-ID Benchmark Dataset

In this repository, we provide a benchmark eye-inpainting dataset called Celeb-ID.
