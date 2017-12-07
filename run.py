
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

# get information of player
@respond_to('info')
def info(message):
    #print(message.body)
    user = sent_user(message)
    i = g.city_info(user[u'name'])
    player = i['player']
    city = i['city']
    links = i['links']
    print("===info===")
    print(player)
    print(type(player))
    m = str(player.name) + ' is ' + str(player.role) + ".\n"
    m += "- in " + str(city['name']) + " (with " + str(city['infections']) + " infections).\n"
    m += "- can move to \n"
    for linked_city in links:
        m += "-* " + str(linked_city['name']) + "(" + str(linked_city['pos']) + ")\n"
    message.reply(m)

@respond_to(r'^drive\s+\S.*')
def drive(message):
    text = message.body['text']
    command, word = text.split(None, 1)
    message.reply('param=' + word + " t=" + temp)


if __name__ == "__main__":
    g = Pandemic(3)
    g.setup()
    main()

