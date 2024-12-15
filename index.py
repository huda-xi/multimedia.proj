import tkinter as tk
import yt_dlp as youtube_dl
import threading

# Variables for controlling the download
download_thread = None
is_paused = False
is_cancelled = False
pause_event = threading.Event()  # Event to pause download

def download_video(url, resolution=None, only_audio=False):
    global is_paused, is_cancelled, pause_event

    ydl_opts = {
        'format': 'bestaudio/best' if only_audio else 'best',
        'outtmpl': '%(title)s.%(ext)s',
    }

    if resolution:
        ydl_opts['format'] = f'bestvideo[height<={resolution}]+bestaudio/best'

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_text.insert(tk.END, "Starting download...\n")

            def progress_hook(d):
                if d['status'] == 'downloading':
                    percent = d.get('progress', 0)
                    info_text.delete(1.0, tk.END)  # Clear previous messages
                    info_text.insert(tk.END, f"Downloading: {percent}%\n")
                elif d['status'] == 'finished':
                    info_text.insert(tk.END, f"Download finished: {d['filename']}\n")

            ydl_opts['progress_hooks'] = [progress_hook]

            # Start downloading the video
            ydl.download([url])

            if is_cancelled:
                info_text.insert(tk.END, "\nDownload cancelled!\n", "error")
            else:
                info_text.insert(tk.END, "\nDownload completed successfully!\n", "success")

    except Exception as e:
        if str(e) != "Download cancelled":
            info_text.insert(tk.END, f"\nError: {e}\n", "error")

def start_download(url, resolution=None, only_audio=False):
    global download_thread, is_paused, is_cancelled, pause_event
    is_paused = False
    is_cancelled = False
    pause_event.set()  # Ensure download is not paused when it starts
    download_thread = threading.Thread(target=download_video, args=(url, resolution, only_audio))
    download_thread.start()

def download_high_quality():
    url = entry.get()
    start_download(url, resolution='1080p')

def download_low_quality():
    url = entry.get()
    start_download(url, resolution='360p')

def download_audio():
    url = entry.get()
    start_download(url, only_audio=True)

# Create the GUI
root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("600x400")
root.configure(bg="#000000")

# URL input field
entry_label = tk.Label(root, text="Enter YouTube Video URL To Download:", bg="#2b2b2b", fg="white", font=("Arial", 13))
entry_label.pack(pady=10)
entry = tk.Entry(root, width=50, font=("Arial", 12))
entry.pack(pady=10)

# Buttons for video quality and audio only
high_quality_button = tk.Button(root, text="High Quality", bg="#4caf50", fg="white", font=("Arial", 12), command=download_high_quality)
high_quality_button.pack(pady=5)

low_quality_button = tk.Button(root, text="Low Quality", bg="#6A0D17", fg="white", font=("Arial", 12), command=download_low_quality)
low_quality_button.pack(pady=5)

audio_button = tk.Button(root, text="Audio Only", bg="#2b2b2b", fg="white", font=("Arial", 12), command=download_audio)
audio_button.pack(pady=5)

# Text box to display information
info_text = tk.Text(root, height=10, width=50, bg="#1e1e1e", fg="white", font=("Consolas", 10), wrap="word")
info_text.tag_configure("success", foreground="lightgreen")
info_text.tag_configure("error", foreground="red")
info_text.pack(pady=10)

# Run the application
root.mainloop()