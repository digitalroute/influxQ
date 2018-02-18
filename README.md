# influxQ
influxQ is a tool to query influxDB written in python 3.



## Build and Install
Note: As the prerequisite, make sure you have python3 installed.

1. ```sudo pip3 install -r requirements.txt```
2. ```pyinstaller -c --onefile influxQ.py```
3. ```sudo cp dist/influxQ /usr/local/bin/influxQ```

### Disclaimer
I have created this tool to make my own life easier since I have a need to explore and query different influxDB instances.
It's not a professional tool as I'm not quite a developer.
Feel free to hack it the way you'd like (pull requests or fork)

##### The reasons for existence of such a tool
* InfluxDB has dropped the support for the web interface.
* chronograf is not enough for data exploration. (Does not support tables)
* Graphana is fine, but too much for me.

