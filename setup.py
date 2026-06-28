import pathlib
import requests

def download_db():
    url = "https://storage.googleapis.com/benchmarks-artifacts/chinook/Chinook.db"
    local_path = pathlib.Path("Chinook.db")
    if local_path.exists():
        print("Chinook.db already exists, skipping download.")
        return
    print("Downloading Chinook.db...")
    response = requests.get(url, timeout=60)
    if response.status_code == 200:
        local_path.write_bytes(response.content)
        print("Downloaded Chinook.db successfully.")
    else:
        raise RuntimeError(f"Failed to download DB. Status: {response.status_code}")

if __name__ == "__main__":
    download_db()