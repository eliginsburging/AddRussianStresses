# AddRussianStresses
Simple PyQt5 interface for adding stresses to Russian text. Stresses are fetched via web scraping from где-ударение.рф. Designed specifically for use with my Reverso Context browser extension (see https://github.com/eliginsburging/ReversoAddon and https://www.youtube.com/watch?v=CUPK0YFfvss), but in principle it should work with any Russian text.

## How to Use this Application
1. Install requirements.txt in a virtual environment
2. Run addstresses.py in that virtual environment
3. Paste Russian text into the Qt window which appears
4. Press "Mark stresses" button
5. Wait for stresses to be fetched (may take a while -- scrapy is configured to be polite to avoid getting banned for too many requests in too short a time)
6. Code will generate "results.txt" file in the same directory with the stresses added.

Note that in the resultant text, all possible stress options will appear separated by double backslashes (i.e. "руки" will be replaced with "руки́\\ру́ки").
