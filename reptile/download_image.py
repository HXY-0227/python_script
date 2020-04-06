import requests
import re

url = 'https://www.mzitu.com/'
header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Referer": "https://www.mzitu.com/"
}

response = requests.get(url, headers=header).text
image_infos = re.findall("data-original='(.*)' alt='(.*?)'", response)
for image_url, name in image_infos:
    print(image_url, name)
    image = requests.get(image_url, headers=header).content
    with open('image/' + name + '.jpg', 'wb') as file:
        file.write(image)