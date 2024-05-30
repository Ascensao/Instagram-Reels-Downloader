import os
import instaloader
from tqdm import tqdm

# Create an instance of Instaloader
IL = instaloader.Instaloader()

IL.download_pictures = False
IL.download_video_thumbnails = False
IL.download_geotags = False
IL.download_comments = False


# Read links from links.txt
with open('links.txt', 'r') as file:
    links = file.read().splitlines()


print(f"Founded {len(links)} reels links in links.txt")


def remove_non_mp4_files(directory):
    # List all files in the directory
    files = os.listdir(directory)

    for file in files:
        # If the file is not a .mp4, remove it
        if not file.endswith('.mp4'):
            os.remove(os.path.join(directory, file))


# Progress bar setup
progress_bar = tqdm(total=len(links), desc="Downloading Reels", unit="link")


# Process each link
for link in links:
    # Get the shortcode from the reel link
    shortcode = link.split("/")[-2]
    
    try:
        # Download the video
        post = instaloader.Post.from_shortcode(IL.context, shortcode)
        IL.download_post(post, "downloads")

        # Rename the video file
        for file in os.listdir("/downloads"):
            if file.endswith(".mp4") and not file.startswith(shortcode):
                os.rename(os.path.join("downloads", file), os.path.join("downloads", f"{shortcode}.mp4"))

        remove_non_mp4_files("downloads")
        print(f"Reel {shortcode}.mp4 successfully downloaded.")
    
    except Exception as e:
        print(f"Failed to download {shortcode}: {e}")
    
    # Update progress bar
    progress_bar.update(1)


progress_bar.close()
print("\n Congratulations, all links has been processed.")