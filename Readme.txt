
Yaroslavl 30 days weather telegramm bot
---------------------------------------
username - @Jaroslavl_weather_bot
name - @Yaroslavl_30_days_weather_bot


Description
-----------
username - @Jaroslavl_weather_bot
name - @Yaroslavl_30_days_weather_bot

This bot represents weather parameters for Yaoslavl sity in range 30 days ahead.
Parameters:
	- min temerature in celsius, 
	- max temperature in celsius,
	- general description (sunny, rain, snow etc.),
	- wind speed in meters per second (for firs 10 days),
	- atmosphere pressure in gectopascals (for firs 10 days).

Bot use the information from https://pogoda33.ru site.
Bot language is russian.


Installation
------------

App require Python 3 interpreter

1) Install dependensis according to requirments.txt.
	>> pip install -r requirements.txt
2) Start the bot
	>> python 3 main.py


Usage
-----

Bot have two modes:
	1) if you send numbers from 1 to 30 you will get weather forecast
		for this day according to calendar.
	2) if you send anything else you will get menu:
		- today
		- tomorrow
		- next weekend
		- in two weeks
		- in month
		and you will get the weather forecast for the chosen option.