from pytube import YouTube

url = 'https://www.youtube.com/watch?v=CN5ODlH6ujc'
yt = YouTube(url)

title = yt.title

thumbnail_url_default = f"https://i.ytimg.com/vi/{yt.video_id}/hqdefault.jpg"
thumbnail_url_high_res = f"https://i.ytimg.com/vi/{yt.video_id}/maxresdefault.jpg"

print(f"제목: {title}")
print(f"기본 썸네일 URL: {thumbnail_url_default}")
print(f"고화질 썸네일 URL: {thumbnail_url_high_res}")
