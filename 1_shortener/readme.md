# URL Shortener: "Shorten That Link!"

## Installation
A virtual environment can be setup based on the requirements file.
```
virtualenv venv --distribute
source venv/bin/activate
pip install -r requirements.txt
```

## Django Setup
For debugging, a simple sqlite database is used.
```
python manage.py syncdb
```

## Phishing Import
For performance, all data from phishtank.com is imported in a batch hourly
(the frequency with which their dump file is updated). On a production server,
this would be setup as a cronjob as such:
```
@hourly /full/path/manage.py runjobs hourly
```

However, for debugging, we can manually force the jobs to run:
```
python manage.py runjobs hourly
```

To speed up the debugging process, I included a file from phishtank.com in 
the repo. But the next time the command is run, it will pull it from the
server, which can take a while (it's around 50 MB).
