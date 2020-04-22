![anti_covid19bot LOGO](https://habrastorage.org/webt/po/n0/j4/pon0j4qdgvvmhjx_dcd4bp5olt4.png)

*My personal chat bot with COVID-19 statistics feature*  
*Can be found at [@anticovid19statbot](https://telegram.me/anticovid19statbot)*

----------

## Requirements:

+ Python 3.7+
+ MongoDB 4.0+

### Libraries:

+ [requests](https://github.com/psf/requests)
+ [pytelegrambotapi](https://github.com/eternnoir/pyTelegramBotAPI)
+ [pymongo](https://github.com/mongodb/mongo-python-driver)
+ [dependency_injector](https://github.com/ets-labs/python-dependency-injector)
+ [geocoder](https://github.com/DenisCarriere/geocoder)
+ [jinja2](https://jinja.palletsprojects.com/en/2.11.x/)
+ [ciso8601](https://github.com/closeio/ciso8601)
+ [cachetools](https://github.com/tkem/cachetools)
+ [pandas](https://pandas.pydata.org)
+ [flask](https://flask.palletsprojects.com/en/1.1.x/)


## How to run

- install [Docker Desktop](https://www.docker.com/products/docker-desktop)
- install [MongoDb](https://www.mongodb.com/download-center/community)
- install [Pycharm](https://www.jetbrains.com/pycharm/download/#section=mac)
- `git clone https://github.com/Oskar987/anti_covid19bot.git`
- `cd anti_covid19bot`
- run [Pycharm](https://www.jetbrains.com/pycharm/download/#section=mac)
- edit environment variables
- change telegram api connection from webhook to long polling

```Python WEBHOOK
# set web hook
server = Flask(__name__)


@server.route('/' + token, methods=['POST'])
def get_messages():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return '!', 200


@server.route('/')
def web_hook():
    bot.remove_webhook()
    bot.set_webhook(url=os.getenv('HEROKU_URL') + token)
    return '!', 200


# application entry point
if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8443)))
```

```Python LONG POLLING
# application entry point
if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
```
- `run project in Pycharm`



Note that anti_covid19bot will run in development mode. Do not try to use this in production.



## Available functions:
+ /start - start communicating with bot
+ /help - get help information
+ /country - get covid-19 statistics by country which you enter the next step
+ /contacts - get contacts information
+ /statistics - get statistics of the bot usage
