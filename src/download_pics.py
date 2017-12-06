import os
import urllib


def url_to_fname(url, out_dir):
    headshot = url.split('/')[-1]
    fname = os.path.join(out_dir, headshot)
    return fname


if __name__ == '__main__':
    url_file = './data/img_urls.txt'
    out_dir = './data/celeb_pics'

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    with open(url_file, 'r') as f:
        for line in f:
            url = line.strip()
            fname = url_to_fname(url, out_dir)

            if os.path.exists(fname):
                continue

            with open(fname, 'wb') as f:
                print('Downloading {}'.format(url))
                f.write(urllib.urlopen(url).read())
