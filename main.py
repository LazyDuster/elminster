from requests import get
import youtube_dl

class ErrorLogging(object):
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        print(msg)

def download_video(search):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'opus',
        }],
        'outtmpl': 'output.%(ext)s',
        'verbose': True,
        'logger': ErrorLogging(),
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            get(search)
        except:
            video = ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]['webpage_url']
        else:
            video = ydl.extract_info(search, download=False)
        ydl.download([video])

def main():
    print("Behold! The great and powerful Elminster!")
    download_video("Developers") # I HAVE FOUR WORDS FOR YOU, I! LOVE! THIS! COMPANY!

if __name__ == "__main__":
    main()