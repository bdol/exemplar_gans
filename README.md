<div class="banner_img center">
<!--<div style="background-image:url('https://raw.githubusercontent.com/bdol/exemplar_gans/master/img/celeb_banner.png'); ?>);"></div>-->
<center>
 <img src="https://raw.githubusercontent.com/bdol/exemplar_gans/master/img/celeb_banner.png">
</center>
</div>

## Authors
<div style="text-align:center">
<div class="author">
    <a href="http://briandolhansky.com" target="_blank">
      <div class="authorphoto"><img src="https://static1.squarespace.com/static/51d342a0e4b0290bcc56387d/t/5a25a353e2c48393e585aae9/1512416083021/me.jpg"></div>
      <div>Brian Dolhansky</div>
    </a>
</div>
<div class="author">
    <a href="https://www.linkedin.com/in/cristiancanton" target="_blank">
      <div class="authorphoto"><img src="https://raw.githubusercontent.com/bdol/exemplar_gans/master/img/CristianCara315x315.jpg"></div>
      <div>Cristian Canton Ferrer</div>
    </a>
</div>
</div>


 <center><img src="https://raw.githubusercontent.com/bdol/exemplar_gans/master/img/facebook-logo.jpg"></center>

<center>
 <a href="https://arxiv.org/abs/1712.03999">
     <img src="https://raw.githubusercontent.com/bdol/exemplar_gans/master/img/paper_screenshot.png">
  </a>
</center>

<center>
  <a href="https://arxiv.org/abs/1712.03999">View full paper on arXiv</a>
</center>
 
<br><br>

## Introduction

We introduce a novel approach to in-painting where the identity of the object to remove or change is preserved and accounted for at inference time: Exemplar GANs (ExGANs). ExGANs are a type of conditional GAN that utilize exemplar information to produce high-quality, personalized in-painting results. We propose using exemplar information in the form of a reference image of the region to in-paint, or a perceptual code describing that object. Unlike previous conditional GAN formulations, this extra information can be inserted at multiple points within the adversarial network, thus increasing its descriptive power. We show that ExGANs can produce photo-realistic personalized in-painting results that are both perceptually and semantically plausible by applying them to the task of closed-to-open eye in-painting in natural pictures. A new benchmark dataset is also introduced for the task of eye in-painting for future comparisons.
<br><br>

## Architecture
![](img/arch.png)
<br><br>

## Results
### Different GAN in-painting strategies
A comparison between GAN in-painting strategies. The first column from the left is the original image, while the second column is the inpainting results from a [standard in-painting GAN](http://hi.cs.waseda.ac.jp/~iizuka/projects/completion/en/). The third and fourth columns show results from a reference-based and code-based ExGAN, respectively.
<br><br>
![](img/m_compare.png)
<br><br>

### Comparison
A comparison between the current [industrial state of the art solution for eye opening](https://www.google.com/search?q=photoshop+elements) and the results from an ExGAN. The first column is a reference image and the second column is the image to in-paint. The third column was generated with Photoshop Elements' eye-opening tool, and the last column shows the results of an ExGAN.
<br><br>
![](img/ours_v_patch_full.png)
<br><br>

## Celeb-ID Benchmark Dataset
![](img/celeb_id_2.jpg) ![](img/celeb_id_3.jpg) ![](img/celeb_id_4.jpg)

In this repository, we provide a benchmark eye-inpainting dataset called Celeb-ID. We do not provide the images, but we include scripts to download, align, and process the images, which results in a dataset of over 100,000 images of roughly 17,000 different celebrities. To create the dataset, clone this repository, then run:

```
python src/download_pics.py
python src/align.py 256
```

The aligned dataset will reside in `data/celeb_id_aligned`. The file `data/celeb_id_raw/data.json` is formatted as:

```
{
  "celeb_a":
    [
      {"eye_left": {...}, "box_left": {...}, 
       "eye_right": {...}, "box_right": {...}, 
       "opened": ..., 
       "closed": ..., 
       "filename": "celeb_a-1.jpg"},
      {"eye_left": {...}, "box_left": {...}, 
       "eye_right": {...}, "box_right": {...}, 
       "opened": ..., 
       "closed": ..., 
       "filename": "celeb_a-2.jpg"},
      ...
    ]
  "celeb_id_b":
    [
      ...
    ],
  ...
}

```

Each celebrity identity is a top-level key in the JSON file. The value for each celebrity is a list of images containing eye locations, boxes to remove from the image with a given height and width (where the box is centered on each eye location), detector values as to whether the eyes are open or closed, and a corresponding filename.<br>

Alternatively, you can download the data resulting from the execution of these two python scripts: [celeb_id_raw.zip](http://www.canton.cat/celeb_id_raw.zip) and [celeb_id_aligned.zip](http://www.canton.cat/celeb_id_aligned.zip). These two files are external and provided for long term archival purposes.
<br><br>

### Our benchmark results
We calculated ExGAN benchmark values on the entire Celeb-ID dataset by in-painting on a given image, and using the next image in the list as the reference (and by using the first image in the list as a reference when testing on the last image). We report average L1 loss over the entire image, as well as MS-SSIM, FID, and inception scores.

| Dataset | Model type | L1 | MS-SSIM | FID | Inception |
|:---:|:---:|:---:|:---:|:---:|:---:|
|Internal benchmark | [Non-exemplar GAN](http://hi.cs.waseda.ac.jp/~iizuka/projects/completion/) |0.018| 5.05E-2 | 11.27 | 3.96 |
|Internal benchmark | Reference-based ExGAN |0.014| 3.97E-2 | 7.67 | 3.82 |
|Internal benchmark | Code-based ExGAN |0.015| 4.15E-2 | 8.49 | 3.94 |
|Celeb ID | [Non-exemplar GAN](http://hi.cs.waseda.ac.jp/~iizuka/projects/completion/) | 7.36E-3 | 8.44E-3 | 15.30 | 3.72 |
|Celeb ID | Reference-based ExGAN | 7.15E-3 | 7.97E-3 | 15.66 | 3.56 |
|Celeb ID | Code-based ExGAN | 7.00E-3 | 7.80E-3 | 14.62 | 3.77 |

