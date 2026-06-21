# Last.fm Recommendation Engine

A music recommendation engine that uses the Last.fm API to suggest tracks based on a song you input. It compares tag-based characteristics using cosine similarity to find similar music.

## How It Works

1. You provide a track name and artist
2. The app fetches tag data for that track, similar tracks, and tracks from similar artists
3. It builds a tag-based profile for each track and uses cosine similarity to rank them
4. Recommendations are printed to the console and saved as a CSV file in `recommendations/`

## Prerequisites

- Python 3.13+
- A Last.fm API key and secret (get one at https://www.last.fm/api/account/create)

## Setup

1. Clone the repo and install dependencies:
   ```bash
   uv sync
   ```

2. Create a `.env` file in the project root:
   ```
   API_KEY=your_lastfm_api_key
   API_SECRET=your_lastfm_api_secret
   ```

## Usage

```bash
uv run main.py
```

You'll be prompted to enter a track name and artist name. Recommendations will be printed to the console and exported to a timestamped CSV in the `recommendations/` folder.
