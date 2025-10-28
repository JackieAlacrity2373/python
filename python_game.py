import curses
import time
import random
import math

# --- CONFIGURATION ---
GX = 32  # grid width
GY = 12  # grid height
TICK_RATE = 0.08  # seconds between frames
Q_SPAWN_INTERVAL = 10  # player moves between spawns
Q_MOVE_INTERVAL = 2    # moves every 2 player moves
Q_RANGE = 2            # detection radius

# --- ENTITY SYSTEM ---
class Entity:
    def __init__(self, x, y, char, solid=False):
        self.x = x
        self.y = y
        self.char = char
        self.solid = solid

    def move(self, dx, dy, world):
        new_x = self.x + dx
        new_y = self.y + dy
        if not world.is_solid_at(new_x, new_y):
            self.x = new_x
            self.y = new_y


class Enemy(Entity):
    """Randomly moving basic enemy (E)"""
    def __init__(self, x, y):
        super().__init__(x, y, "E", solid=True)

    def take_turn(self, world):
        dx, dy = random.choice([(1,0), (-1,0), (0,1), (0,-1), (0,0)])
        new_x = self.x + dx
        new_y = self.y + dy
        if world.is_solid_at(new_x, new_y):
            return
        player = world.get_player()
        if player and player.x == new_x and player.y == new_y:
            world.game_over = True
            return
        self.x, self.y = new_x, new_y


class QEnemy(Entity):
    """Special Q enemy: spawns every 10 moves, moves every 2 moves, kills in radius."""
    def __init__(self, x, y):
        super().__init__(x, y, "Q", solid=True)
        self.move_cooldown = 0

    def take_turn(self, world, player_moves):
        # Move only every Q_MOVE_INTERVAL turns
        if player_moves % Q_MOVE_INTERVAL != 0:
            return

        dx, dy = random.choice([(1,0), (-1,0), (0,1), (0,-1), (0,0)])
        new_x = self.x + dx
        new_y = self.y + dy

        if not world.is_solid_at(new_x, new_y):
            self.x, self.y = new_x, new_y

        # Check if player is within range (Manhattan distance)
        player = world.get_player()
        if player:
            dist = abs(self.x - player.x) + abs(self.y - player.y)
            if dist <= Q_RANGE:
                world.game_over = True


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.entities = []
        self.game_over = False
        self.win = False

    def add_entity(self, entity):
        self.entities.append(entity)

    def get_entity_at(self, x, y):
        for e in self.entities:
            if e.x == x and e.y == y:
                return e
        return None

    def is_solid_at(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        for e in self.entities:
            if e.solid and e.x == x and e.y == y:
                return True
        return False

    def get_player(self):
        for e in self.entities:
            if e.char == "@":
                return e
        return None

    def get_enemies(self):
        return [e for e in self.entities if e.char == "E"]

    def get_q_enemies(self):
        return [e for e in self.entities if e.char == "Q"]

    def draw(self, stdscr):
        stdscr.clear()
        for y in range(self.height):
            for x in range(self.width):
                entity = self.get_entity_at(x, y)
                if entity:
                    stdscr.addstr(y, x * 2, entity.char)
                else:
                    stdscr.addstr(y, x * 2, "_")
        stdscr.addstr(self.height + 1, 0, "Use WASD to move. Press Q to quit.")
        stdscr.refresh()


# --- MAIN GAME LOOP ---
def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(0)

    world = World(GX, GY)
    player = Entity(1, GY - 2, "@", solid=True)
    world.add_entity(player)

    # Add base enemies
    enemies = [Enemy(10, GY - 2), Enemy(18, GY - 3), Enemy(24, GY - 2)]
    for e in enemies:
        world.add_entity(e)

    # Add goal
    goal = Entity(GX - 3, GY - 2, "G", solid=False)
    world.add_entity(goal)

    # Add floor
    for x in range(GX):
        world.add_entity(Entity(x, GY - 1, "#", solid=True))

    direction = (0, 0)
    player_moves = 0  # count number of player actions

    while not world.game_over and not world.win:
        key = stdscr.getch()
        moved_this_turn = False

        if key != -1:
            ch = chr(key).lower()
            if ch == "q":
                break
            elif ch == "w":
                direction = (0, -1)
            elif ch == "s":
                direction = (0, 1)
            elif ch == "a":
                direction = (-1, 0)
            elif ch == "d":
                direction = (1, 0)

        if direction != (0, 0):
            new_x = player.x + direction[0]
            new_y = player.y + direction[1]
            target = world.get_entity_at(new_x, new_y)

            if target:
                if target.char in ["E", "Q"]:
                    world.game_over = True
                elif target.char == "G":
                    world.win = True
                elif not target.solid:
                    player.x, player.y = new_x, new_y
                    moved_this_turn = True
            else:
                if not world.is_solid_at(new_x, new_y):
                    player.x, player.y = new_x, new_y
                    moved_this_turn = True

            if moved_this_turn:
                player_moves += 1

                # Regular enemies move once per player move
                for e in world.get_enemies():
                    e.take_turn(world)

                # Q enemies move once every 2 moves & check range
                for q in world.get_q_enemies():
                    q.take_turn(world, player_moves)

                # Spawn a new Q every 10 moves
                if player_moves % Q_SPAWN_INTERVAL == 0:
                    spawn_x = random.randint(2, GX - 4)
                    spawn_y = random.randint(1, GY - 3)
                    if not world.is_solid_at(spawn_x, spawn_y):
                        world.add_entity(QEnemy(spawn_x, spawn_y))

            direction = (0, 0)

        # Draw
        world.draw(stdscr)
        time.sleep(TICK_RATE)

    stdscr.clear()
    if world.win:
        stdscr.addstr(GY // 2, GX, "🎉 YOU WIN! 🎉")
    elif world.game_over:
        stdscr.addstr(GY // 2, GX, "💀 GAME OVER 💀")
    stdscr.addstr(GY // 2 + 2, GX - 5, "Press any key to exit...")
    stdscr.refresh()
    stdscr.nodelay(False)
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
