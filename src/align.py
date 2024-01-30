import argparse
import cv2
import json
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from utils import crop, clipped_normal, filename_to_group, get_transformed_eye_points, rotate

log_interval = 1000

def process_image(k, v, image_dir, output_dir, output_size):
    im_f = os.path.join(image_dir, k)
    if not os.path.exists(im_f):
        print('Could not find {}'.format(im_f))
        return None

    im = cv2.imread(im_f)
    if im is None:
        print('Error reading {}'.format(im_f))
        return None

    im, M = rotate(im, v, output_size)
    im, cx, cy = crop(im, v)
    im_h, _, _ = im.shape
    scale = float(output_size) / float(im_h)
    im = cv2.resize(im, (output_size, output_size), interpolation=cv2.INTER_CUBIC)

    out_v = {'filename': k}
    eye_left, eye_right = get_transformed_eye_points(v, M, cx, cy, scale)
    if eye_left is not None:
        out_v['eye_left'] = {'x': eye_left[0], 'y': eye_left[1], 'box_left': {'w': clipped_normal(96), 'h': clipped_normal(96)}}
    else:
        out_v['eye_left'] = None

    if eye_right is not None:
        out_v['eye_right'] = {'x': eye_right[0], 'y': eye_right[1], 'box_right': {'w': clipped_normal(96), 'h': clipped_normal(96)}}
    else:
        out_v['eye_right'] = None

    out_v['opened'] = v.get('eyes_opened', None)
    out_v['closed'] = v.get('eyes_closed', None)

    cv2.imwrite(os.path.join(output_dir, k), im)
    return k, out_v

def main():
    parser = argparse.ArgumentParser(description='Batch 2d-align faces')
    parser.add_argument('output_size', type=int, default=256, help='Final image size')
    args = parser.parse_args()

    celeb_json = './data/celeb_params.json'
    image_dir = './data/celeb_id_raw'
    output_dir = './data/celeb_id_aligned'

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    with open(celeb_json, 'r') as f:
        data = json.load(f)

    out_data = {}
    lock = threading.Lock()

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_image, k, v, image_dir, output_dir, args.output_size) for k, v in data.items()]

        for c, future in enumerate(futures):
            if c % log_interval == 0:
                print('Processed {}/{}'.format(c, len(data)))
                with lock:
                    with open(os.path.join(output_dir, 'data.json'), 'w') as f:
                        json.dump(out_data, f)

            result = future.result()
            if result:
                k, out_v = result
                g, i = filename_to_group(k)
                with lock:
                    if g not in out_data:
                        out_data[g] = []
                    out_data[g].append(out_v)

    with open(os.path.join(output_dir, 'data.json'), 'w') as f:
        json.dump(out_data, f)

if __name__ == '__main__':
    main()
