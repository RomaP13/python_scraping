import requests
import json
import csv
from bs4 import BeautifulSoup

# url = "https://bi.ua/ukr/kukly-i-pupsy/kukly/"
headers = {
    "Accept": "application/font-woff2;q=1.0,application/font-woff;q=0.9,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0"
}

# req = requests.get(url, headers=headers)
# src = req.text

# with open("index.html", "w") as file:
#     file.write(src)

with open("index.html") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")
urls = soup.find(class_="row catalog").find_all(class_="goodsItemLink")
names = soup.find(class_="row catalog").find_all(class_="itemDes")

urls_dict = {}

for url, name in zip(urls, names):
    item_url = "https://bi.ua" + url.get("href")
    item_name = name.text

    urls_dict[item_name] = item_url

count = 0
for name in names:
    url = urls_dict[name.text]

    req = requests.get(url, headers=headers)
    src = req.text

    soup = BeautifulSoup(src, "lxml")

    price = soup.find(class_="costIco").text

    old_price = soup.find(class_="old").text

    description = soup.find(class_="scroller").get_text()

    features = soup.find(class_="bordered").find_all("table")

    features_info = {}
    for item in features:
        features_tds = item.find_all("td")
        for i in range(0, len(features_tds), 2):
            features_info[features_tds[i].text] = features_tds[i + 1].text

    image_tags = soup.find_all('img', class_='pnav')

    image_urls, video_urls = [], []

    for img in image_tags:
        image_src = img["src"]
        if not image_src.startswith("https"):
            if 'size' in image_src:
                image_src = image_src.replace('/size_60', '')
            image_urls.append("https://bi.ua" + image_src)
        if "data-video-src" in img.attrs:
            video_urls.append(img["data-video-src"])

    features = ', '.join(str(item) for item in features_info)
    img_urls = ', '.join(str(item) for item in image_urls)
    vid_urls = ', '.join(str(item) for item in video_urls)

    with open("data.csv", "a", encoding="utf-8") as file:
        writer = csv.writer(file)
        if old_price:
            writer.writerow(
                    (
                        name.text,
                        price,
                        old_price,
                        description,
                        features,
                        img_urls,
                        vid_urls
                    )
            )
        else:
            writer.writerow(
                    (
                        name.text,
                        price,
                        description,
                        features,
                        img_urls,
                        vid_urls
                    )
            )
    


# with open("all_categories_dict.json", "w") as file:
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)


# # with open("all_categories_dict.json") as file:
# #     all_categories = json.load(file)

# with open("index2.html", "w") as file:
#     file.write(src)
