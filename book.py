import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import os
import natsort
import shutil

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}


def get_chapter_list(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.encoding = "gbk"
    soup = BeautifulSoup(response.text, "html.parser")
    chapter_list = []
    for chapter in soup.find("ul", id="section-list").find_all("li"):
        href = chapter.find("a")["href"]
        chapter_list.append(href)
    return chapter_list


def get_chapter_content(url):
    response = requests.get(url)
    response.encoding = "gbk"
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("h1", class_="title").text.strip()
    content = soup.find("div", id="content").text.strip()
    return title, content


def write_to_txt(title, content, index):
    os.makedirs("books", exist_ok=True)
    with open(os.path.join("books", str(index) + ".txt"), "w", encoding="utf-8") as f:
        f.write(title + "\n")
        f.write(content + "\n")


def get_chapter(url, index):
    title, content = get_chapter_content(url)
    if title and content:
        write_to_txt(title, content, index)
        print(f'保存成功 {title}')
    else:
        print(f'保存失败 {url}')


def merge_txt_files(filename):
    filelist = os.listdir('books')
    newFileList = natsort.natsorted(filelist)
    with open(filename + '.txt', 'w', encoding="utf-8") as outfile:
        for file_name in newFileList:
            with open(os.path.join('books', file_name), 'r', encoding="utf-8") as infile:
                outfile.write(infile.read())
    print('下载完成')
    shutil.rmtree('books')


def main(url, filename):
    chapter_list = get_chapter_list(url)
    with ThreadPoolExecutor(max_workers=20) as executor:
        for index, chapter_url in enumerate(chapter_list):
            executor.submit(get_chapter, url + chapter_url, index)
    merge_txt_files(filename)


if __name__ == "__main__":
    # 示例：https://www.52wx.com/141_141801/
    url = input("请输入小说地址:")
    filename = input("请输入小说名:")
    main(url, filename)
