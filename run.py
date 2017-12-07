
from slackbot.bot import Bot
from slackbot.bot import respond_to

from game.pandemic import Pandemic

# ref https://github.com/lins05/slackbot/issues/43
def sent_user(message):
    return message.channel._client.users[message.body['user']]

def main():
    bot = Bot()
    bot.run()

@respond_to('json')
@respond_to('JSON')
def hello(message):
    message.reply('json :)')


@respond_to('entry')
def entry(message):
    user = sent_user(message)
    p = g.entry(user[u'name'])
    message.reply(user[u'name'] + ' are ' + str(p.role))

@respond_to('city')
def city(message):
    #print(message.body)
    user = sent_user(message)
    p = g.entry(user[u'name'])
    message.reply(user[u'name'] + ' are ' + str(p.role))

if __name__ == "__main__":
    g = Pandemic(3)
    g.setup()
    main()
