def download_video(youtube_link):
    import subprocess
    output_path = "output.mp4"
    subprocess.run([
        "yt-dlp",
        "--cookies", "/home/ubuntu/youtube_cookies.txt", 
        youtube_link,
        "-o", output_path
    ], check=True)
    return output_path
