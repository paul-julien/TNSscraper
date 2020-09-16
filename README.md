# TNSscraper
Dedicated web scraper for The News Stations' newsletter

Installation:

## Check if Python3 is installed:
```
python3 --version
```
If you see a python3 version, continue. Otherwise (Debian9):
```
sudo apt update
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev curl libbz2-dev
curl -O https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tar.xz
tar -xf Python-3.7.3.tar.xz
cd Python-3.7.3
./configure --enable-optimizations
make -j 8
sudo make altinstall
```
Verify that the installation was a success with:
```
python3.7 --version
```

## Run TNSScraper
Setup using
```
python3 ./setup.py install
```
Run with
```
python3 news_station_scraper/scraper.py
```

## Cron job example (for daily activation at 08:00)
```
crontab -e
0 8 * * * /usr/bin/python3 <yourpath>/news_station_scraper/scraper.py.py
```
