import os
import instaloader
from instaloader.exceptions import BadCredentialsException, TwoFactorAuthRequiredException
from dotenv import load_dotenv
from tqdm import tqdm
import uuid
import time
import random

def configure_instaloader():
    """Configure Instaloader settings and log in to Instagram, handling 2FA if required."""
    # Load environment variables from .env file
    load_dotenv()

    IL = instaloader.Instaloader()

    # Configure Instaloader settings
    IL.download_pictures = False
    IL.download_video_thumbnails = False
    IL.download_geotags = False
    IL.download_comments = False

    USERNAME = os.getenv('INSTAGRAM_USER')
    PASSWORD = os.getenv('INSTAGRAM_PASS')

    if not USERNAME or not PASSWORD:
        print("Instagram credentials not found. Please check your .env file.")
        exit(1)

    session_file = f"{USERNAME}.session"

    try:
        if os.path.exists(session_file):
            # Load session from file
            IL.load_session_from_file(USERNAME, filename=session_file)
            print("Session loaded successfully.")
        else:
            # Perform login
            IL.login(USERNAME, PASSWORD)
            print("Successfully logged into Instagram.")
            # Save session to file
            IL.save_session_to_file(filename=session_file)
    except TwoFactorAuthRequiredException:
        print("Two-factor authentication required.")
        two_factor_code = input("Enter your 2FA code: ")
        try:
            IL.two_factor_login(two_factor_code)
            print("Successfully logged into Instagram with 2FA.")
            # Save session to file
            IL.save_session_to_file(filename=session_file)
        except Exception as e:
            print(f"Failed to login with 2FA: {e}")
            exit(1)
    except BadCredentialsException:
        print("Login failed. Please check your username and password.")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

    print("Proceeding to download reels...")
    return IL

def read_links(filename):
    """Read reel links from a file, ignoring blank lines and spaces."""
    with open(filename, 'r') as file:
        lines = file.read().splitlines()
        return [line.strip() for line in lines if line.strip()]

def remove_non_mp4_files(directory):
    """Remove non-MP4 files from a directory."""
    for file in os.listdir(directory):
        if not file.endswith('.mp4'):
            os.remove(os.path.join(directory, file))

def download_reel(IL, link, download_dir):
    """Download a reel from a link and save it as an MP4 file."""
    if not link.startswith('http'):
        print(f"Invalid link: {link}")
        return False

    try:
        shortcode = link.strip().split("/")[-2]
        post = instaloader.Post.from_shortcode(IL.context, shortcode)
        IL.download_post(post, download_dir)

        # Find the downloaded video file
        downloaded_files = [
            f for f in os.listdir(download_dir)
            if f.endswith('.mp4') and not f.startswith(shortcode)
        ]
        for file in downloaded_files:
            source_file = os.path.join(download_dir, file)
            # Ensure unique filename
            unique_filename = f"{shortcode}_{uuid.uuid4().hex}.mp4"
            new_filename = os.path.join(download_dir, unique_filename)
            os.rename(source_file, new_filename)

        remove_non_mp4_files(download_dir)
        print(f"Reel {shortcode}.mp4 downloaded successfully.")
        return True

    except Exception as e:
        print(f"Failed to download {link}: {e}")
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
            # Delay to avoid rate limiting
            time.sleep(random.uniform(2, 5))

    # Remove all files in the directory except .mp4 files
    remove_non_mp4_files(download_dir)

    print("\nCongratulations, all links have been processed.")

if __name__ == "__main__":
    main()