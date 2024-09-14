from pytube import YouTube

# YouTube 비디오 URL 제공
url = 'https://www.youtube.com/watch?v=CN5ODlH6ujc'

# YouTube 객체 생성
yt = YouTube(url)

# 제목과 썸네일 URL 추출
title = yt.title
thumbnail_url = yt.thumbnail_url

print(f"제목: {title}")
print(f"썸네일 URL: {thumbnail_url}")
