import requests
from bs4 import BeautifulSoup
from youtube_search import YoutubeSearch
import youtube_dl

print('Enter the Spotify link')
link = input()

if link.startswith('https://open.spotify.com'):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('meta', {'property': 'og:title'}).get('content')
    artist = soup.find('meta', {'name': 'music:musician_description'}).get('content')
    #print(artist)
    songname = str(title + " " + artist)
    song = "+".join([title, artist])
   # print('SongFound '+ song)
    print('\033[91m' + 'SongFound ' + song + '\033[0m')
    temp=YoutubeSearch(str(songname), max_results=1).to_dict()
    result = YoutubeSearch(str(songname), max_results=1).to_dict()[0]['url_suffix']
    
    
    video_url = str("https://www.youtube.com/" + result)
options = {
    'format': 'bestaudio/best',  # Choose the best audio quality available
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',  # Convert to MP3 format
        'preferredquality': '320',  # Specify the audio quality
    }],
    'outtmpl': f"{temp[0]['title']}.mp3",  
    #'verbose': True,  
    #'no_check_certificate': True,  
}
#print('VIDEO URL OF THE SONG:'+video_url)
try:
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_url])
        
except (youtube_dl.utils.PostProcessingError, youtube_dl.utils.DownloadError) as e:
    print(f"Error: {e}")
    print('\033[93m' + 'Song Downloaded! ' + '\033[0m')
    print("Please make sure ffmpeg is installed. You can install it from https://ffmpeg.org/download.html.")

