import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def url_to_fname(url, out_dir):
    headshot = url.split('/')[-1]
    fname = os.path.join(out_dir, headshot)
    return fname

def download_image(url, out_dir):
    fname = url_to_fname(url, out_dir)

    if not os.path.exists(fname):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(fname, 'wb') as f:
                    f.write(response.content)
        except Exception as e:
            print(f"Error downloading {url}: {e}")

if __name__ == '__main__':
    url_file = './data/img_urls.txt'
    out_dir = './data/celeb_id_raw'
    max_workers = 100  # Adjust the number of workers based on your network and CPU capabilities

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    urls = []
    with open(url_file, 'r') as f:
        for line in f:
            url = line.strip()
            urls.append(url)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(download_image, url, out_dir): url for url in urls}
        for future in tqdm(as_completed(future_to_url), total=len(urls), desc="Downloading images"):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                print(f'{url} generated an exception: {exc}')