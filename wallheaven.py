import requests
from concurrent.futures import ThreadPoolExecutor
import os.path
from requests import ReadTimeout

global API_KEY
API_KEY = "《enter api_key》"

def init():

    global file_name
    file_name = input(">>>please enter a filename to save wallpapers（输入文件夹名以保存图片）:").strip()

    category_code = get_category_code()
    purity_code = get_purity_code()

    global data_url
    data_url = f"https://wallhaven.cc/api/v1/search?apikey={API_KEY}"+f"&purity={category_code}"+f"&purity={purity_code}"+f"&page=1"

def get_category_code():

    print("》》》chose category you like:\t《all》\t《anime》\t《general》\t《people》\t《ga》\t《gp》\n"
          "》》》输入想要下载的分类标签:\t《all》\t《anime》\t《general》\t《people》\t《ga》\t《gp》")
    category = input('》》》Enter Category: ').lower()
    print("\n")
    category_tags = {'all': '111', 'anime': '010', 'general': '100', 'people': '001', 'ga': '110', 'gp': '101'}
    category_code = category_tags[category]
    while category not in ('all', 'anime', 'general', 'people', 'ga', 'gp'):
        print("wrong category input!!!")
        category = input('》》》Enter Category: ').lower()
        print("\n")
    return category_code

def get_purity_code():
    print("》》》chose purity you like:\t 《sfw》\t《sketchy》\t《nsfw》\t《ws》\t《wn》\t《sn》\t《all》\n"
          "》》》输入纯享版块名:\t 《sfw》\t《sketchy》\t《nsfw》\t《ws》\t《wn》\t《sn》\t《all》")
    purity = input('》》》Enter Purity: ').lower()
    print("\n")
    while purity not in ('sfw', 'sketchy', 'nsfw', 'ws', 'sn', 'all'):
        print("wrong purity!!!")
        purity = input('》》》Enter Purity: ').lower()
        print("\n")
    purity_tags = {'sfw': '100', 'sketchy': '010', 'nsfw': '001', 'ws': '110', 'wn': '101', 'sn': '011', 'all': '111'}
    purity_code = purity_tags[purity]
    return purity_code

def get_one_pic(url):

    response = requests.get(url)

    if os.path.exists(f"./{file_name}/{url[-10:]}") == True:
        print(":::::" + url[-10:] + " has exists in " + f"./{file_name}/{url[-10:]}")

    else:
        try:
            if response.status_code == 200:
                content = response.content
                with open("./"+file_name+"/"+url[-10:], "wb") as f:
                    f.write(content)
                print("》》》downloading:正在下载:"+url[-10:])
            else:
                print('Get Picture Failed', response.status_code)
                return None
        except (ConnectionError, ReadTimeout):
            print('Crawling Failed', url)
            return None

def make_file(file_name):
    if not os.path.isdir('./' + file_name):
        os.mkdir(os.getcwd()+'\\\\'+file_name)

def get_page_number():
    start, end = map(int, input("》》》Please enter the page range you want download (like this:'1,1','1,2'.etc) :").split(","))
    return start, end+1

def main():
    init()
    make_file(file_name)
    star_page, end_page = get_page_number()
    for page in range(star_page, end_page):
        global data_url
        data_url = data_url[:-1]+f"{page}"
        print(data_url, "is crawling")
        data = (requests.get(data_url).json())["data"]
        # 线程池多线程提取
        with ThreadPoolExecutor(50) as t:
            for i in range(len(data)):
                path = data[i]["path"]
                t.submit(get_one_pic, url=path)

        print(f"》》》PAGE{page} IS OVER. 提取完成！！！")
    print("》》》All is done!!!")

if __name__=="__main__":
    main()