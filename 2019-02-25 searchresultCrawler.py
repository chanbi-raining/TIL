


import requests
from bs4 import BeautifulSoup
import re

url = 'https://search.naver.com/search.naver'


def parsePost(soup):
    post = soup.select('div.section.sp_post')
    posttext = []
    if post:
        titles = post[0].select('dl > dt')
        contents = post[0].select('dl > dd')
        for idx in range(len(titles)):
            temp = titles[idx].text + ' '
            temp += contents[4 * idx + 1].text
            posttext.append(temp)
    return posttext


def parseKinn(soup):
    kinn = soup.select('div._kinBase.section.kinn')
    kinntext = []
    if kinn:
        titles = kinn[0].select('dt.question')
        contents_q = kinn[0].select('dl > dd')
        contents_a = kinn[0].select('dd.answer')
        for idx in range(len(titles)):
            temp = titles[idx].text[4:] + ' '
            temp += contents_q[4 * idx + 1].text
            temp += contents_a[idx].text[3:]
            kinntext.append(temp)
    return kinntext


# parsing news
def parseNews(soup):
    news = soup.select('div._prs_nws_all.section.news')
    newstext = []
    if news:
        titles = news[0].select('dt > a')
        content = news[0].select('dd')
        c_idx = 0
        for idx in range(len(titles)):
            temp = titles[idx].text + ' '
            while c_idx < len(content):
                if content[c_idx].text[-5:] == '보내기  ':
                    c_idx += 1
                    continue
                if re.findall('관련뉴스 전체보기', content[c_idx].text):
                    c_idx += 1
                    continue
                temp += content[c_idx].text
                break
            newstext.append(temp)
            c_idx += 1
    return newstext


# parsing cafes
def parseCafe(soup):
    cafe = soup.select('div._prs_caf._cafeBase.section.cafe')
    cafetext = []
    if cafe:
        titles = cafe[0].select('dl > dt')
        contents = cafe[0].select('dd.sh_cafe_passage')
        for idx in range(len(titles)):
            temp = titles[idx].text + ' '
            temp += contents[idx].text
            cafetext.append(temp)
    return cafetext


# parsing blogs
def parseBlog(soup):
    blog = soup.select('div._prs_blg._blogBase.section.blog')
    blogtext = []
    if blog:
        titles = blog[0].select('dl > dt')
        contents = blog[0].select('dd.sh_blog_passage')
        for idx in range(len(titles)):
            temp = titles[idx].select('a')[0].text + ' '
            temp += contents[idx].text
            blogtext.append(temp)
    return blogtext


def parseFirstPage(keywords):
    alteredkey = keywords.replace(' ', '+')
    param = {'query': alteredkey}
    response = requests.get(url, params=param)
    soup = BeautifulSoup(response.text, 'lxml')

    result = parsePost(soup) + parseKinn(soup) + parseNews(soup)
    result += parseCafe(soup) + parseBlog(soup)

    with open(keywords + '_crawled.txt', 'w', encoding='UTF-8') as f:
        for item in result:
            f.write('%s\n' % item)

    print(keywords, "Done")


if __name__ == '__main__':
    with open('final.txt', 'r') as F:
        words = F.readlines()
    for key in words:
        parseFirstPage(key.strip())
