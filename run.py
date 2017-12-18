
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

def info_string(info):
    player = info['player']
    city = info['city']
    links = info['links']
    m = str(player.name) + ' is ' + str(player.role) + ".\n"
    m += str(player.action) + ' action played.\n'
    m += "- in " + str(city['name']) + " (with " + str(city['infections']) + " infections).\n"
    m += "- have cards below\n"
    for card in player.cards:
        m += "- [ " + str(card['name'])
        if 'pos' in card:
            m += " (" + str(card['pos']) + ")"
        m += " ]\n"
    m += "- can move to \n"
    for linked_city in links:
        m += "- [ " + str(linked_city['name']) + " (" + str(linked_city['pos']) + ") ]\n"
    return m


# get information of player
@respond_to('info')
def info(message):
    #print(message.body)
    user = sent_user(message)
    i = g.city_info(user[u'name'])
    message.reply(info_string(i))

def parse(message):
    user = message.channel._client.users[message.body['user']]
    text = message.body['text']
    command, word = text.split(None, 1)
    return {"user": user[u'name'], "command": command, "param": int(word)}


@respond_to(r'^drive\s+\S.*')
def drive(message):
    command = parse(message)
    r = g.drive(command['user'], command['param'])
    if r is None:
        message.reply('move to ' + command['param'] + " is failed.\n")
    else:
        i = g.city_info(command['user'])
        message.reply("drive successed.\n" + info_string(i))

@respond_to(r'^direct\s+\S.*')
def direct(message):
    command = parse(message)
    r = g.direct(command['user'], command['param'])
    if r is None:
        message.reply('direct move to ' + command['param'] + " is failed.\n")
    else:
        i = g.city_info(command['user'])
        message.reply("direct successed.\n" + info_string(i))


if __name__ == "__main__":
    g = Pandemic(3)
    g.setup()
    main()

