import feedparser
import bs4
import telepot
import shelve
import time
import urllib
import sys

rss = feedparser.parse("https://www.meneame.net/rss")
TOKEN = sys.argv[1]
bot = telepot.Bot(TOKEN)
data = shelve.open("meneamebot_data", writeback=True)
# bot.sendMessage("15866663", rss['updated'])

for entry in rss['entries'][0:24]:
    message = "[" + entry['title'] + "](" + entry['meneame_url'] + ")\n\n"
    message += "*Meneos*: [" + entry['meneame_votes'] + "](https://www.meneame.net/backend/menealo?id=" + entry['meneame_link_id'] + "&user=0)"
    message += ". *Negativos*: " + entry['meneame_negatives']
    message += ". *Clicks*: [" + entry['meneame_clicks'] + "](https://www.meneame.net/go?id=" + entry['meneame_link_id'] + ")"
    message += ". *Comentarios*: [" + entry['meneame_comments'] + "](" + entry['comments'] + ")\n"
    tags = []
    for tag in entry['tags']:
        tags.append("[" + tag['term'] + "](https://www.meneame.net/search?p=tags&q=" + urllib.parse.quote(tag['term']) + ")")
    message += "*Etiquetas*: " + ", ".join(tags) + "\n\n"
    summary_text = bs4.BeautifulSoup(entry['summary'], "lxml")
    message += summary_text.find_all('p')[0].text
    message += "\n_Actualizado: " + rss['updated'] + "_"
#    print(message)
    if entry['meneame_link_id'] not in data['sent_messages']:
        data['sent_messages'][entry['meneame_link_id']] = []
        for user in data['subscribed_users']:
            res = bot.sendMessage(user, message, parse_mode="markdown",
                                  disable_web_page_preview=True)
            msg_id = telepot.message_identifier(res)
            data['sent_messages'][entry['meneame_link_id']].append(msg_id)
    else:
        for msg in data['sent_messages'][entry['meneame_link_id']]:
            bot.editMessageText(msg, message, parse_mode="markdown",
                                disable_web_page_preview=True)
    time.sleep(1)
data.close()
