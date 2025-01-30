# download Logos
import os
import requests
from PIL import Image

# API URL
API_URL = "http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard"

# Directory to save images
LOGO_DIR = "logos"
os.makedirs(LOGO_DIR, exist_ok=True)

def fetch_logos():
    """Fetch team logos from the ESPN API and download them."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        for event in data.get("events", []):
            competitors = event["competitions"][0]["competitors"]

            for team in competitors:
                abbreviation = team["team"].get("abbreviation", "unknown")
                logo_url = team["team"].get("logo")

                if abbreviation and logo_url:
                    download_logo(logo_url, abbreviation)

    except requests.RequestException as e:
        print(f"Error fetching API data: {e}")

def download_logo(url, abbreviation):
    """Download the logo and save it with a black background."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Save the original image temporarily
        temp_file = os.path.join(LOGO_DIR, f"{abbreviation}_temp.png")
        with open(temp_file, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        # Open image and add black background
        process_logo(temp_file, abbreviation)

        # Remove the temporary image
        os.remove(temp_file)

    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")

def process_logo(image_path, abbreviation):
    """Convert transparent areas to black and save the image."""
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGBA")  # Ensure image has an alpha channel
            background = Image.new("RGBA", img.size, (0, 0, 0, 255))  # Black background
            img = Image.alpha_composite(background, img)  # Merge image with background
            img = img.convert("RGB")  # Convert to RGB format

            final_path = os.path.join(LOGO_DIR, f"{abbreviation}.png")
            img.save(final_path, "PNG")

            print(f"Saved: {final_path}")

    except Exception as e:
        print(f"Error processing {image_path}: {e}")

if __name__ == "__main__":
    fetch_logos()
