# meneamebot
Telegram bot. Reads from "meneame" digg-like news aggregator's rss and forwards stories to bot subscribers

It was just a proof of concept of what can be done with telegram bots, and a way of learning about python. Any improvement, correction, linting is welcome.

To use it, you just need to add subscribers via python command (I'll may create a bot interface for that, too):
```
$ ./python
Python 3.5.2 (default, Jul  5 2016, 12:43:10) 
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import shelve
>>> data = shelve.open("meneamebot_data", writeback=True)
>>> data['subscribed_users'] = ['first-telegram-id', 'second-telegram-id', ...]
>>> data.close()
```
Also get a token from [botfather](https://telegram.me/bot/botfather), and use it as an argumen to the script.

Then you can run it periodically. I use a cron:
```
$ crontab -e
*/15 * * * * cd /home/meneamebot/bin/ && ./python meneamebot.py MY-BOT-TOKEN
```


