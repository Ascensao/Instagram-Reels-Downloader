import os
import instaloader
from tqdm import tqdm

def configure_instaloader():
    """Configure Instaloader settings."""
    IL = instaloader.Instaloader()
    IL.download_pictures = False
    IL.download_video_thumbnails = False
    IL.download_geotags = False
    IL.download_comments = False
    return IL

def read_links(filename):
    """Read reel links from a file."""
    with open(filename, 'r') as file:
        return file.read().splitlines()

def remove_non_mp4_files(directory):
    """Remove non-MP4 files from a directory."""
    for file in os.listdir(directory):
        if not file.endswith('.mp4'):
            os.remove(os.path.join(directory, file))

def download_reel(IL, link, download_dir):
    """Download a reel from a link and save it as an MP4 file."""
    shortcode = link.split("/")[-2]
    
    try:
        post = instaloader.Post.from_shortcode(IL.context, shortcode)
        IL.download_post(post, download_dir)

        for file in os.listdir(download_dir):
            if file.endswith(".mp4") and not file.startswith(shortcode):
                new_filename = os.path.join(download_dir, f"{shortcode}.mp4")
                
                if os.path.exists(new_filename):
                    new_filename = os.path.join(download_dir, f"{shortcode}_{os.path.getmtime(new_filename)}.mp4")
                
                os.rename(os.path.join(download_dir, file), new_filename)

        remove_non_mp4_files(download_dir)
        print(f"Reel {shortcode}.mp4 successfully downloaded.")
        return True

    except Exception as e:
        print(f"Failed to download {shortcode}: {e}")
        return False


def main():
    """Main function to download reels from links."""
    IL = configure_instaloader()
    links = read_links('links.txt')
    download_dir = "downloads"

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    print(f"Found {len(links)} reel links in links.txt")

    with tqdm(total=len(links), desc="Downloading Reels", unit="link") as progress_bar:
        for link in links:
            download_reel(IL, link, download_dir)
            progress_bar.update(1)

    # Delete all files in the directory except .mp4 files
    remove_non_mp4_files(download_dir)

    print("\nCongratulations, all links have been downloaded.")

if __name__ == "__main__":
    main()