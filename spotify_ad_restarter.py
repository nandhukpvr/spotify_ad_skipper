import os
import time
import subprocess
import ctypes

def get_spotify_title():
    try:
        # Retrieve the MainWindowTitle for the Spotify process using PowerShell
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        output = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command", "(Get-Process Spotify -ErrorAction SilentlyContinue).MainWindowTitle"],
            startupinfo=startupinfo,
            text=True
        )
        titles = [line.strip() for line in output.split('\n') if line.strip()]
        if titles:
            return titles[0]
    except Exception:
        pass
    return None

def restart_and_play(previous_song_title=None):
    print("Restarting Spotify...")
    # Kill the Spotify process
    subprocess.call(["taskkill", "/F", "/IM", "Spotify.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.5)
    
    # Try different common installation paths for Spotify
    spotify_path = os.path.expandvars(r"%APPDATA%\Spotify\Spotify.exe")
    if not os.path.exists(spotify_path):
        spotify_path = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WindowsApps\Spotify.exe")
        
    if os.path.exists(spotify_path):
        subprocess.Popen([spotify_path])
    else:
        # Fallback if standard paths fail
        os.system("start spotify:")

    print("Waiting for Spotify to start up...")
    time.sleep(5) # Adjust this delay if your Spotify takes longer to load
    
    print("Resuming playback...")
    # Simulate a Media Play/Pause keystroke (Virtual-Key Code 0xB3)
    # This acts globally, similar to pressing the play/pause button on a keyboard
    VK_MEDIA_PLAY_PAUSE = 0xB3
    ctypes.windll.user32.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, 2, 0)
    
    # Wait a bit for the song to start playing
    time.sleep(3)
    
    # Check if the previously playing song is still playing
    current_title = get_spotify_title()
    if previous_song_title and current_title and current_title == previous_song_title:
        print(f"[{time.strftime('%H:%M:%S')}] Previous song detected after restart. Skipping...")
        VK_MEDIA_NEXT = 0xB0
        ctypes.windll.user32.keybd_event(VK_MEDIA_NEXT, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_MEDIA_NEXT, 0, 2, 0)
        time.sleep(1)  # Wait after skip to ensure it takes effect

def main():
    print("-" * 50)
    print("Spotify Ad Auto-Restarter is running!")
    print("Monitoring Spotify for ads... Press Ctrl+C to exit.")
    print("-" * 50)
    last_title = ""
    last_song_title = ""
    
    while True:
        title = get_spotify_title()
        
        if title:
            if title != last_title:
                if title:
                    print(f"[{time.strftime('%H:%M:%S')}] Currently Playing / Window Title: {title}")
                last_title = title
            
            title_lower = title.lower()
            
            # Normal songs ALWAYS use ' - ' (space-hyphen-space) to separate the artist and track name.
            # When paused, the window usually reverts to one of the default states.
            # Ads usually lack ' - ' and are not the default paused title.
            
            explicit_ads = ["advertisement", "ad", "werbung", "publicidad", "pub", "listen to music, ad-free."]
            is_explicit_ad = (title_lower in explicit_ads) or ("advertisement" in title_lower)
            is_implicit_ad = (" - " not in title) and (title_lower not in ["spotify", "spotify free", "spotify premium"])
            
            # Update last_song_title only if it's a song (not an ad)
            if not (is_explicit_ad or is_implicit_ad):
                last_song_title = title
            
            if is_explicit_ad or is_implicit_ad:
                # To prevent restarting during quick, normal song transitions where the title might temporarily lack a hyphen
                time.sleep(1.0) 
                current_title = get_spotify_title()
                
                # Double-check if the title is still an ad
                if current_title and current_title == title:
                    print(f"[{time.strftime('%H:%M:%S')}] Ad detected! (Title: {title}) Closing and restarting Spotify...")
                    restart_and_play(last_song_title)
                    last_title = ""
        
        time.sleep(1.5) # Poll less frequently to save CPU

if __name__ == "__main__":
    main()
