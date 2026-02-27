import yt_dlp
import os

def naar_seconden(tijd):
    """Zet mm:ss of hh:mm:ss formaat om naar seconden."""
    if ':' in tijd:
        delen = tijd.split(':')
        if len(delen) == 2:
            return int(delen[0]) * 60 + int(delen[1])
        elif len(delen) == 3:
            return int(delen[0]) * 3600 + int(delen[1]) * 60 + int(delen[2])
    return int(tijd)


def download_video(url, output_path="downloads", quality="best"):
    """Download een YouTube video."""
    
    os.makedirs(output_path, exist_ok=True)
    
    ydl_opts = {
        'format': quality,
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'noplaylist': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"\ndownloaden: {url}")
        info = ydl.extract_info(url, download=True)
        print(f"Klaar! Video opgeslagen als: {info['title']}")


def download_audio_only(url, output_path="downloads"):
    """Download alleen het audio (mp3)."""
    
    os.makedirs(output_path, exist_ok=True)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"\nAudio downloaden: {url}")
        info = ydl.extract_info(url, download=True)
        print(f"✓ Klaar! Audio opgeslagen als: {info['title']}.mp3")


def download_clip(url, start_tijd, duur, output_path="downloads"):
    """Download een clip vanaf een starttijd voor een bepaalde duur."""
    
    os.makedirs(output_path, exist_ok=True)
    
    eind_tijd = start_tijd + duur
    
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'{output_path}/%(title)s_clip.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegVideoRemuxer',
            'preferedformat': 'mp4',
        }],
        'download_ranges': lambda info, ydl: [{'start_time': start_tijd, 'end_time': eind_tijd}],
        'force_keyframes_at_cuts': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"\nClip downloaden van {start_tijd}s tot {eind_tijd}s ({duur} seconden)...")
        info = ydl.extract_info(url, download=True)
        print(f"Klaar! Clip van {duur} seconden opgeslagen.")


# --- Hoofdprogramma ---
if __name__ == "__main__":
    print("=" * 35)
    print("      YouTube Downloader")
    print("=" * 35)
    print("1. Video downloaden")
    print("2. Alleen audio (MP3)")
    print("3. Clip downloaden (tijdstempels)")
    print("=" * 35)

    keuze = input("\nKeuze (1, 2 of 3): ").strip()
    url = input("YouTube URL: ").strip()

    if keuze == "1":
        print("\nKwaliteit opties: best, 1080p, 720p, 480p, 360p")
        kwaliteit = input("Kwaliteit (standaard = best): ").strip() or "best"
        if kwaliteit != "best":
            kwaliteit = f"bestvideo[height<={kwaliteit[:-1]}]+bestaudio/best"
        download_video(url, quality=kwaliteit)

    elif keuze == "2":
        download_audio_only(url)

    elif keuze == "3":
        print("\nTijdstempel invoeren (formaat: 3:30 of 210 voor seconden)")
        start = input("Vanaf waar: ").strip()
        duur = int(input("Hoeveel seconden: ").strip())
        download_clip(url, naar_seconden(start), duur)

    else:
        print("Ongeldige keuze, start het programma opnieuw.")