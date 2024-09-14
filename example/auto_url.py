import sys
from pytube import YouTube
import instaloader
import re

def extract_video_details_youTube(url):
    yt = YouTube(url)
    title = yt.title

    # 기본 썸네일 URL과 고화질 썸네일 URL 생성
    thumbnail_url_default = f"https://i.ytimg.com/vi/{yt.video_id}/hqdefault.jpg"
    thumbnail_url_high_res = f"https://i.ytimg.com/vi/{yt.video_id}/maxresdefault.jpg"

    return title, thumbnail_url_default, thumbnail_url_high_res



if __name__ == "__main__":
    # 명령줄 인수로 URL 입력 받기
    if len(sys.argv) != 2:
        # print("사용법: python script_name.py <YouTube URL>")
        sys.exit(1)

    url = sys.argv[1]
    #여기서 url이 어떤 소셜 네트워크인지 판별 해야됨 
    #1. 유튜브
    #2. 인스타그램
    #3. 페이스북
    thumbnail_url_default = ""
    thumbnail_url_high_res = ""
    title = ""
    if "youtube.com" in url or "youtu.be" in url:
        yt = YouTube(url)
        title = yt.title

        title, thumbnail_url_default, thumbnail_url_high_res = extract_video_details_youTube(url)
        # 기본 썸네일 URL과 고화질 썸네일 URL 생성
        thumbnail_url_default = f"https://i.ytimg.com/vi/{yt.video_id}/hqdefault.jpg"
        thumbnail_url_high_res = f"https://i.ytimg.com/vi/{yt.video_id}/maxresdefault.jpg"
    elif "instagram.com" in url:
        # https://www.instagram.com/p/Cokgb1DBN6N/ -> 프로필 게시물 
        # https://www.instagram.com/reel/C8CbDc9yBdg/ -> 릴스 게시물
        if "reel" in url: # 릴스
            print("릴스 게시물 입니다")
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
        elif "p" in url: # 프로필 
            print("프로필 게시물 입니다.")
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

            # print(f"썸네일 이미지 URL: {thumbnail_url}")
            # print(f"제목(캡션): {caption}")
    else:
        print("지원되지 않는 URL입니다.")


  

    print(f"제목: {title}")
    print(f"기본 썸네일 URL: {thumbnail_url_default}")
    print(f"고화질 썸네일 URL: {thumbnail_url_high_res}")
