import os
import pygame as pg
import math
main_dir = os.path.split(os.path.abspath(__file__))[0]

#####
from astar import *

from pygame.math import Vector2


class Player(pg.sprite.Sprite):

    def __init__(self, name, start, goal, waypoints, player_image, graph):
        super().__init__()
        self.name = name
        self.start = start
        self.goal = goal
        self.reached = False
        self.begin = False
        self.graph = graph
        self.image =load_image(player_image).convert_alpha()
        # self.image = pg.Surface((30, 50))
        # self.image.fill(pg.Color('dodgerblue1'))
        self.rect = self.image.get_rect(center=start)
        self.vel = Vector2(0, 0)
        self.max_speed = 3
        self.pos = Vector2(start)
        self.waypoints = waypoints
        self.waypoint_index = 0
        self.target = self.waypoints[self.waypoint_index]
        self.target_radius = 50

    def update(self):
        if self.begin:
            # A vector pointing from self to the target.
            heading = self.target - self.pos
            distance = heading.length()  # Distance to the target.
            if heading.length_squared() > 0:
                heading.normalize_ip()
                # dirvect.scale_to_length(self.speed) 

            if distance <= 2:  # We're closer than 2 pixels.
                # Increment the waypoint index to swtich the target.
                # The modulo sets the index back to 0 if it's equal to the length.
                # self.waypoint_index = (self.waypoint_index + 1) % len(self.waypoints)
                if self.waypoint_index < len(self.waypoints)-1:
                    self.waypoint_index = self.waypoint_index + 1
                elif self.waypoints[self.waypoint_index] == self.goal:
                    self.reached = True
                self.target = self.waypoints[self.waypoint_index]
            if distance <= self.target_radius:
                # If we're approaching the target, we slow down.
                self.vel = heading * (distance / self.target_radius * self.max_speed)
            else:  # Otherwise move with max_speed.
                self.vel = heading * self.max_speed
            

            self.pos += self.vel
            self.rect.center = self.pos
            # print(f'self.rect.center={self.rect.center}')

    def add_waypoint(self, new_point, graph=None):
        if graph == None:
            last_point = self.waypoints[-1]
            if new_point in self.graph.neighbors(last_point):
                self.waypoints.append(new_point)
        else:
            last_point = self.waypoints[-1]
            if new_point in graph.neighbors(last_point):
                self.waypoints.append(new_point)

    def play(self):
        self.begin = True
        print(f'{self.name} is plaing : {self.begin}')
        self.update()

# quick function to load an image
def load_image(name):
    path = os.path.join(main_dir, "data", name)
    return pg.image.load(path).convert()

Color_screen=(49,150,100)
Color_line=(172,172,172)
ai_way_color = (249,166,2)
human_way_color = (18,150,216)
line_width = 15

def draw_lines(screen,path_list, Color_line):
    for i in range(len(path_list)-1):
        pg.draw.line(screen, Color_line ,path_list[i],path_list[i+1], 1)
    # pg.draw.line(screen,Color_line,(60,80),(130,100))
    # pg.display.flip()

def draw_int_lines(screen,map, Color_line):
    loc = map['loc']
    rgk = map['vk']
    for k, v in loc.items():
        for end in v:
            cost = math.sqrt((k[0]-end[0])*(k[0]-end[0]) + (k[1]-end[1])*(k[1]-end[1]))
            pg.draw.line(screen,Color_line,k,end, line_width)

            font = pg.font.Font('freesansbold.ttf', 12)
            text = font.render(str(round(cost)), 1, (0, 0, 255), (255,255,255))
            textRect = text.get_rect()
            textRect.center = ((k[0]+end[0])//2, (k[1]+end[1])//2)
            screen.blit(text, textRect)
        # pg.draw.line(screen,Color_line,(60,80),(130,100))
        # pg.display.flip()
    b_list = []
    for k, v in loc.items():
        font = pg.font.Font('freesansbold.ttf', 12)
        text = font.render(rgk[k]+' '+str(k), 1, (255, 0, 0), (255,255,255))
        textRect = text.get_rect()
        textRect.center = (k[0], k[1])
        b_list.append(screen.blit(text, textRect))

    return b_list

def draw_house(screen, start, goal):
    house_ai =load_image("home-ai-80x80.png")
    house_ai_rect = house_ai.get_rect(center=start)
    house_human =load_image("home-human-80x80.png")
    house_human_rect = house_human.get_rect(center=goal)
    screen.blit(house_ai, house_ai_rect)
    screen.blit(house_human, house_human_rect)

# here's the full code
def main():
    pg.init()
    maps = Map(map_dict)
    # game_map = maps.get(name='travel')
    game_map = maps.get(name='default')
    print('game_map[kv]=',game_map['kv'])
    # start, goal = game_map['kv']['arad'], game_map['kv']['Bucharest']
    start, goal = game_map['kv']['a'], game_map['kv']['i']
    # start, goal = (100, 300), (800, 100)
    graph = Graph(game_map['loc'])
    print(f'graph: {graph}')
    # graph = Graph(loc)
    
    
    came_from, cost_so_far = a_star_search(graph, start, goal)

    print("""A path from "A" to "K":""")
    print('A-Star Path: ',construct_path(game_map['vk'], came_from.keys()))
    # print('came_from=',came_from.keys())
    print('cost_so_far=',cost_so_far)
    # path_list_ai =[k for k in came_from.keys()] 
    path_list_ai = graph.find_path(start, goal)
    # print('path_list_ai:',construct_path(rgk, path_list_ai))

    path_list_human = graph.find_path(goal,start)
    print('path_list_human:',construct_path(game_map['vk'], path_list_human))

    ###############################################
    screen = pg.display.set_mode((900, 650))
    pg.display.set_caption('House Attack (AI Based Game)')
    clock = pg.time.Clock()

    background = load_image("grass.jpg")
    background = pg.transform.scale2x(background)
    # background = load_image("sand-background.jpg")
    # background = pg.transform.scale2x(background)
    # background = pg.transform.scale2x(background)

    screen.blit(background, (0, 0))

    # waypoints = path_list_ai #
    waypoints = [k for k in came_from.keys()]
    # test_data = waypoints[::-1] # [(100, 300), (200, 100), (100, 600), (300, 200), (400, 100), (400, 400), (500, 200), (700, 200), (800, 100), (600, 500), (500, 300)][::-1] 
    b_list = draw_int_lines(screen, game_map, Color_line)
    draw_house(screen, start, goal)
    # draw_lines(screen, path_list_ai, ai_way_color)
    # draw_lines(screen, path_list_human, human_way_color)
    all_players = pg.sprite.Group()

    player_ai = Player(name="AI", start=start, goal=goal, waypoints=path_list_ai, player_image="little-bot-annimation.gif", graph=graph) # oldplayer.gif alien1.gif robot-80x80.jpg  robot-icon-50x50.png
    # player_human = Player(goal, path_list_human, player_image="human-50x50.png")
    player_human = Player(name="Player", start=goal, goal=start, waypoints=[goal], player_image="human-50x50.png", graph=graph)
    all_players.add(player_ai)
    all_players.add(player_human)
    print(f'path_list_human={path_list_human}')
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pos = pg.mouse.get_pos()
                for b in b_list:
                    if b.collidepoint(pos):
                        name = game_map['vk'][b.center]
                        print(f'Added Next Edge (waypoint) : {name}({b.center})')
                        new_point = b.center
                        all_players.sprites()[-1].add_waypoint(new_point)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    print("Game Starting :) ----------")
                    for player in all_players.sprites():
                        player.play()


        screen.blit(background, (0, 0))
        b_list = draw_int_lines(screen,game_map, Color_line)
        draw_house(screen, start, goal)
        p_ai = all_players.sprites()[0]
        p_human = all_players.sprites()[1]
        if p_ai.reached and p_human.reached:
            draw_lines(screen, p_ai.waypoints , ai_way_color)
            draw_lines(screen, p_human.waypoints, human_way_color)
        all_players.update()
        all_players.draw(screen)

        pg.display.flip()
        clock.tick(60)

    

if __name__ == "__main__":
    main()
