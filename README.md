# Instagram Reels Downloader

This project allows you to download Instagram Reels videos using links provided in a text file (`links.txt`). The downloaded videos are saved with their shortcode as the filename.

## Features

- Download multiple Instagram Reels videos.
- Rename downloaded videos to their shortcodes.
- Display progress with a progress bar.
- Print success messages for each downloaded video.

## Requirements

- Python 3.x
- `instaloader` library
- `tqdm` library

## Installation

1. Clone the repository or download the project files.

2. Install the required libraries:
    ```bash
    pip install instaloader tqdm
    ```

3. Create a `links.txt` file in the project directory and add the Instagram Reels links, one per line.

## Usage

1. Ensure your `links.txt` file is in the same directory as `main.py` and contains the Instagram Reels links you want to download.

2. Run the script:
    ```bash
    python main.py
    ```

3. The script will read the links from `links.txt`, download each video, and rename the files with their respective shortcodes. It will also display a progress bar and print success messages.

## Example

`links.txt`: -https://www.instagram.com/reel/C6TqZ9_qCM2/?igsh=eXVrczI3cGlmeGhy
              https://www.instagram.com/reel/C6TqZ9_qCM2/?igsh=eXVrczI3cGlmeGhy


Running the script:
```bash
python main.py
```

Output:
```
Founded 2 reels links in links.txt
Downloading Reels: 100%|████████████████████████████████████████| 2/2 [00:05<00:00,  2.50s/link]
Reel C6TqZ9_qCM2.mp4 successfully downloaded.
Reel C9t6Qk4t9X4.mp4 successfully downloaded.
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

