import sys
from pytube import YouTube
import instaloader
import re
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 유튜브 url
def extract_video_details_youTube(url):
    yt = YouTube(url)
    title = yt.title

    # 기본 썸네일 URL과 고화질 썸네일 URL 생성
    thumbnail_url_default = f"https://i.ytimg.com/vi/{yt.video_id}/hqdefault.jpg"
    thumbnail_url_high_res = f"https://i.ytimg.com/vi/{yt.video_id}/maxresdefault.jpg"

    return title, thumbnail_url_default, thumbnail_url_high_res

#인스타그램 프로필 
def extract_details_from_instagram_profile(url):
    loader = instaloader.Instaloader()
    pattern = r'instagram\.com/p/([^/]+)/'
    match = re.search(pattern, url)
    # post_shortcode = 'Cokgb1DBN6N'  # URL에서 추출한 shortcode
    post_shortcode = ""
    if match:
        post_shortcode = match.group(1)
        print(f"게시물 ID: {post_shortcode}")
    else:
        print("URL에서 게시물 ID를 찾을 수 없습니다.")
    # 게시물 정보를 가져오기
    post = instaloader.Post.from_shortcode(loader.context, post_shortcode)
    thumbnail_url_default = post.url
    title = post.caption

    return title, thumbnail_url_default

#인스타그램 릴스
def extract_details_from_instagram_reels(url):
    loader = instaloader.Instaloader()

    pattern = r'instagram\.com/reel/([^/]+)/'
    match = re.search(pattern, url)

    # 릴스의 shortcode 추출
    # reel_shortcode = 'C8CbDc9yBdg'  # URL에서 추출한 shortcode
    reel_shortcode = ""
    if match:
        reel_shortcode = match.group(1)
        print(f"게시물 ID: {reel_shortcode}")
    else:
        print("URL에서 게시물 ID를 찾을 수 없습니다.")

    # 릴스 정보를 가져오기
    reel = instaloader.Post.from_shortcode(loader.context, reel_shortcode)
    thumbnail_url_default = reel.url
    title = reel.caption
    return title, thumbnail_url_default


# 일반 url
def extract_details_from_general_website(url):
    # 웹 페이지 HTML 가져오기
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 제목 추출
    title = soup.title.string if soup.title else "제목을 찾을 수 없음"

    # 메타 태그에서 썸네일 URL 추출
    thumbnail_url = ""
    og_image = soup.find("meta", property="og:image")
    if og_image and og_image.get("content"):
        thumbnail_url = og_image["content"]

    return title, thumbnail_url

def extract_favicon(url):
    try:
        # 웹사이트의 HTML 가져오기
        response = requests.get(url)
        response.raise_for_status()

        # BeautifulSoup을 사용하여 HTML 파싱
        soup = BeautifulSoup(response.content, 'html.parser')

        # 모든 파비콘 관련 링크 태그 찾기
        icons = soup.find_all('link', rel=lambda x: x and 'icon' in x.lower())

        # 고해상도 아이콘을 위한 변수 초기화
        high_res_favicon = None
        max_size = 0

        for icon in icons:
            href = icon.get('href', '')
            if not href:
                continue

            # 상대 경로 처리
            if not href.startswith('http'):
                href = urljoin(url, href)

            # 벡터 형식(SVG) 아이콘 우선 선택
            if icon.get('type') == 'image/svg+xml':
                return href

            # 해상도 크기 파악
            sizes = icon.get('sizes')
            if sizes:
                size_values = sizes.split('x')
                if len(size_values) == 2:
                    try:
                        width = int(size_values[0])
                        if width > max_size:
                            high_res_favicon = href
                            max_size = width
                    except ValueError:
                        continue
            else:
                # 'sizes' 속성이 없는 경우 기본적으로 아이콘을 선택
                if not high_res_favicon:
                    high_res_favicon = href

        return high_res_favicon

    except requests.RequestException as e:
        print(f"오류 발생: {e}")
        return None


if __name__ == "__main__":
    print("hee")
    # 명령줄 인수로 URL 입력 받기
    if len(sys.argv) != 2:
        # print("사용법: python script_name.py <YouTube URL>")
        sys.exit(1)

    url = sys.argv[1]
    # url = re.escape(raw_url)
    # print("url + ", url)

   
    #여기서 url이 어떤 소셜 네트워크인지 판별 해야됨 
    #1. 유튜브
    #2. 인스타그램
    #3. 페이스북
    thumbnail_url_default = ""
    thumbnail_url_high_res = ""
    title = ""
    favicon_url = ""
    if "youtube.com" in url or "youtu.be" in url: #유튜브
        yt = YouTube(url)
        title = yt.title

        title, thumbnail_url_default, thumbnail_url_high_res = extract_video_details_youTube(url)
        # 기본 썸네일 URL과 고화질 썸네일 URL 생성
        thumbnail_url_default = f"https://i.ytimg.com/vi/{yt.video_id}/hqdefault.jpg"
        thumbnail_url_high_res = f"https://i.ytimg.com/vi/{yt.video_id}/maxresdefault.jpg"
        favicon_url = extract_favicon(url)
    elif "instagram.com" in url: #인스타그램
        # https://www.instagram.com/p/Cokgb1DBN6N/ -> 프로필 게시물 
        # https://www.instagram.com/reel/C8CbDc9yBdg/ -> 릴스 게시물
        if "reel" in url: # 릴스
            title, thumbnail_url_default = extract_details_from_instagram_reels(url)
        elif "p" in url: # 프로필 
            title, thumbnail_url_default = extract_details_from_instagram_profile(url)
        favicon_url = extract_favicon(url)
    else: 
        # print("지원되지 않는 URL입니다.")
        title, thumbnail_url_default = extract_details_from_general_website(url)
        favicon_url = extract_favicon(url)

  

    print(f"제목: {title}")
    print(f"기본 썸네일 URL: {thumbnail_url_default}")
    print(f"고화질 썸네일 URL: {thumbnail_url_high_res}")
    print(f"파비콘 URL: {favicon_url}")
