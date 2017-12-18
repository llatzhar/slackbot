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

    def dump_dict(self, deck):
        s = ""
        for key in deck:
            c = deck[key]
            s += c['name']
            if 'infections' in c:
                s += " (" + str(c['infections']) + ")"
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

    def pick_infection_deck(self):
        return self.infection_cards.pop()

    def pick_player_deck(self):
        return self.player_cards.pop()

    def put_cube(self, city, num):
        pos = city['pos']
        c = self.cities[pos]
        c['infections'] = num

    def pop_player_card(self, player, pos):
        for c in player.cards:
            if pos == c['pos']:
                player.cards.remove(c)
                return c
        return

    def get_city(self, pos):
        return self.cities[pos]

    def setup(self):
        # master data
        self.map_master = self.load_map()
        self.roles = self.load_role()
        self.specials = self.load_special()
        # states
        self.player_cards = []
        self.infection_cards = []
        self.cities = {}
        self.global_action = 0

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
            city_pos = c["pos"]
            self.cities[city_pos] = c

        print("======== before setup ======")
        print(self.dump_dict(self.cities))

        # setup initial infections on city states
        for _ in range(3):
            i = self.pick_infection_deck()
            print("popped3:" + i['name'])
            self.put_cube(i, 3)
        for _ in range(3):
            i = self.pick_infection_deck()
            print("popped2:" + i['name'])
            self.put_cube(i, 2)
        for _ in range(3):
            i = self.pick_infection_deck()
            print("popped1:" + i['name'])
            self.put_cube(i, 1)

        print("======== after setup ======")
        print(self.dump_dict(self.cities))
        

    def entry(self, username):
        if username not in self.players:
            new_player = Player(username)
            new_player.set_role(self.role())
            for _ in range(2): # TODO 2 depends on player number. proceed epidemic?
                c = self.pick_player_deck()
                new_player.add_picked(c)
            self.players[new_player.name] = new_player
        print("======== after entry ======")
        print(self.dump_players())
        return new_player

    def role(self):
        i = random.randint(0, 4)
        return self.roles[i]


    def check_draw(self, player):
        player.action += 1
        if player.action > 3:
            player.action = 0 
            for _ in range(2):
                c = self.pick_player_deck()
                player.add_picked(c)

        self.global_action += 1
        if self.global_action > 3:
            self.global_action = 0
            i = self.pick_infection_deck()
            print("infection:" + i['name'])
            self.put_cube(i, 1)

        print("======== after check_draw ======")
        print(self.dump_dict(self.cities))
        return


    def drive(self, player_name, to_pos):
        player = self.players[player_name]
        if player is None:
            return
        current_city = self.get_city(player.pos)
        if to_pos not in current_city['links']:
            return
        
        player.pos = to_pos
        self.check_draw(player)
        return player.pos


    def direct(self, player_name, to_card_pos):
        player = self.players[player_name]
        if player is None:
            return
        to_card = self.pop_player_card(player, to_card_pos)
        if to_card is None:
            return
        
        player.pos = to_card_pos
        self.check_draw(player)
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
    
