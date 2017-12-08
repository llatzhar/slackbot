import random
import yaml
import copy
from game.player import Player

class Pandemic:
    def __init__(self, c):
        self.players = {}

    def load_map(self):
        f = open("game/map.yml", "r+")
        return yaml.load(f)

    def load_role(self):
        f = open("game/role.yml", "r+")
        return yaml.load(f)

    def load_special(self):
        f = open("game/special.yml", "r+")
        return yaml.load(f)

    def divide(self, deck, n):
        arrays = []
        for i in range(0, n):
            arrays.append([])
        #print("arrays=" + str(arrays))
        #print("deck len=" + str(len(deck)))
        c = 0
        while (c < len(deck)):
            print( c%n )
            arrays[c % n].append(deck[c])
            c += 1
        #print("arrays2=" + str(arrays))
        return arrays

    def dump_deck(self, deck):
        s = ""
        for card in deck:
            s += card['name']
            if 'infections' in card:
                s += " (" + str(card['infections']) + ")"
            s += "\n"
        return s

    def dump_players(self):
        s = ""
        for player_name in self.players:
            p = self.players[player_name]
            print(p)
            
            s += p.name
            for card in p.cards:
                s += " (" + card['name'] + ")"
            s += "\n"
        return s

    def pick_infection(self):
        return self.infection_cards.pop()

    def pick_player(self):
        return self.player_cards.pop()

    def put_cube(self, city, num):
        for c in self.cities:
            if c['pos'] == city['pos']:
                c['infections'] = num
                return

    def get_city(self, pos):
        for city in self.cities:
            if pos == city['pos']:
                return city
        return
            

    def setup(self):
        # master data
        self.map_master = self.load_map()
        self.roles = self.load_role()
        self.specials = self.load_special()
        # states
        self.player_cards = []
        self.infection_cards = []
        self.cities = []


        # buildup player card deck
        for city in self.map_master:
            c = copy.copy(city)
            c["card_type"] = "city"
            self.player_cards.append(c)
        for card in self.specials:
            c = copy.copy(card)
            card["card_type"] = "special"
            self.player_cards.append(c)
        random.shuffle(self.player_cards)
        divided = self.divide(self.player_cards, 4)        # todo 4 depends on difficulty
        self.player_cards = []
        for m in divided:
            print(m)
            m.append({'name': 'Epidemic', 'card_type': 'Epidemic'})
            random.shuffle(m)
            self.player_cards += m
        print(self.dump_deck(self.player_cards))

        # infection deck
        for city in self.map_master:
            c = copy.copy(city)
            self.infection_cards.append(c)
        random.shuffle(self.infection_cards)

        # buildup city states
        for city in self.map_master:
            c = copy.copy(city)
            c["infections"] = 0
            self.cities.append(c)

        print("======== before setup ======")
        print(self.dump_deck(self.cities))

        # setup initial infections on city states
        for _ in range(3):
            i = self.pick_infection()
            print("popped3:" + i['name'])
            self.put_cube(i, 3)
        for _ in range(3):
            i = self.pick_infection()
            print("popped2:" + i['name'])
            self.put_cube(i, 2)
        for _ in range(3):
            i = self.pick_infection()
            print("popped1:" + i['name'])
            self.put_cube(i, 1)

        print("======== after setup ======")
        print(self.dump_deck(self.cities))
        

    def entry(self, username):
        if username not in self.players:
            new_player = Player(username)
            new_player.set_role(self.role())
            for _ in range(2): # TODO 2 depends on player number. proceed epidemic?
                c = self.pick_player()
                new_player.add_picked(c)
            self.players[new_player.name] = new_player
        print("======== after entry ======")
        print(self.dump_players())
        return new_player

    def role(self):
        i = random.randint(0, 4)
        return self.roles[i]

    def drive(self, player_name, to_pos):
        player = self.players[player_name]
        current_city = self.get_city(player.pos)
        if to_pos not in current_city['links']:
            return
        else:
            player.pos = to_pos
            player.action += 1
        return player.pos
        

    def city_info(self, player_name):
        info = {}
        player = self.players[player_name]
        #print(player)
        #print(type(player))

        city = self.get_city(player.pos)
        #print(city)
        #print(type(city))
        links = []
        for pos in city['links']:
            c = self.get_city(pos)
            links.append(c)

        info['player'] = player
        info['city'] = city
        info['links'] = links

        return info
    
