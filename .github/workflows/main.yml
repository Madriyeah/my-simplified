name: Update M3U8 Link
on:
  schedule:
    - cron: '0 */3 * * *'  # Runs every 3 hours
  workflow_dispatch:      # Allows you to run it manually

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: pip install requests

      - name: Run update script
        run: python update.py

      - name: Commit and push changes
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "Auto-update token: $(date)"
          file_pattern: 'playlist.m3u8' # The file your script updates

