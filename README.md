# tiktok_ads_parser
As part of a freelance task, a program was written for parsing commercials in tiktok.
The program accepts links with commercials ( example: https://ads.tiktok.com/business/creativecenter/topads/7130213222917259265/pc/en?countryCode=US&period=7 ), and uploads videos from these pages.
The videos are saved under the path '../../Downloaded_videos/'.

P.S. Also, an asynchronous version is being developed, using arsenic

### :computer: Technologies:
- Undetected_chromedriver (This library was chosen because it automatically loads chromedriver, and the video on the site is loaded only when you physically open the page)
- requests;

---

### :hammer_and_wrench: Installation:
1. $ pip install -r requirements.txt
2. $ pyinstaller tiktok_parser.py (Optional)
