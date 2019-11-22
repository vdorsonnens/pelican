cd samples
pelican ./content -s ./pelican.conf.py
pelican -l --port 8001 --bind 0.0.0.0
