### Crawler
python3 main.py
args:
 - url(-u / --url): the url to crawl
 - headless (-h / --headless): if set to 1, the browser will not be shown
 - skip-map (-sm / --skip-map): if valid file path set, the crawler will skip the map and load the map from the file

Activate the virtual environment (ubuntu):
```
source venv/bin/activate
```
Install the requirements:
```
pip install -r requirements.txt
```

## How to use the crawler

```
python3 main.py --url=https://mdo.demogram.cz/
```
```
python3 main.py --url=https://mdo.demogram.cz/ --skip-map=map.csv
```
```
python3 main.py --url=https://mdo.demogram.cz/ --skip-map=map.csv --headless=1
```

## Loop for CMD
Create .bat file and insert this, then run it.

Loop is set to 5 repetitions.
```
@echo off
cd /d C:\Users\"Your file destination"
for /L %%i IN (1,1,5) do (
    python3 main.py --url=https://mdo.demogram.cz/ --skip-map=map.csv
)
```
In this section you must insert your Github project destination
```
cd /d C:\Users\"Your file destination"
```
