import cv2
import numpy as np


def filename_to_group(f):
    group = '-'.join('.'.join(f.split('.')[:-1]).split('-')[:-1])
    i = int('.'.join(f.split('.')[:-1]).split('-')[-1])
    return group, i


def transform(p, M, cx, cy, scale):
    pp = [0, 0]
    pp[0] = int(scale * (p[0] * M[0, 0] + p[1] * M[0, 1] + M[0, 2] - cx))
    pp[1] = int(scale * (p[0] * M[1, 0] + p[1] * M[1, 1] + M[1, 2] - cy))
    return pp


def get_transformed_eye_points(d, M, cx, cy, scale):
    eye_left, eye_right = None, None
    if 'eye_left' in d:
        el = (d['eye_left']['x'], d['eye_left']['y'])
        eye_left = transform(el, M, cx, cy, scale)
    if 'eye_right' in d:
        er = (d['eye_right']['x'], d['eye_right']['y'])
        eye_right = transform(er, M, cx, cy, scale)

    return eye_left, eye_right


def get_face_center(d):
    if 'eye_right' not in d or 'eye_left' not in d or 'mouth_center' not in d:
        cx, cy = int(d['face_x']), int(d['face_y'])
    else:
        cx = int((d['eye_right']['x'] + d['eye_left']['x'] +
                  d['mouth_center']['x']) / 3)
        cy = int((d['eye_right']['y'] + d['eye_left']['y'] +
                  d['mouth_center']['y']) / 3)

    return cx, cy


def crop(im, d):
    x, y = get_face_center(d)
    im_h, im_w, _ = im.shape
    h, w = min(d['face_h'] * 1.2, im_h), min(d['face_w'] * 1.2, im_w)

    if x - w/2 < 0:
        x0 = 0
        x1 = w
    elif x + w/2 >= im_w:
        x0 = im_w - w
        x1 = im_w
    else:
        x0 = x - w / 2
        x1 = x + w / 2

    if y - h/2 < 0:
        y0 = 0
        y1 = h
    elif y + h/2 >= im_h:
        y0 = im_h - h
        y1 = im_h
    else:
        y0 = y - h / 2
        y1 = y + h / 2

    x0, x1, y0, y1 = int(x0), int(x1), int(y0), int(y1)

    return im[y0:y1, x0:x1, ...], x0, y0


def rotate(im, d, out_size):
    im_h, im_w, _ = im.shape
    cx, cy = get_face_center(d)

    M = cv2.getRotationMatrix2D((cx, cy), d['roll'], 1)

    im = cv2.warpAffine(im, M, (im_w, im_h), flags=cv2.INTER_CUBIC)
    return im, M


def clipped_normal(sz):
    return int(np.clip(
        np.abs(np.random.normal(sz // 2, sz // 4)), sz // 2, sz))
