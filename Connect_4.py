import pygame
from typing import Iterable


tri_points = []
available_circles = []
turns = ["red", "blue"]
curr_turn = "red"
turn_i = 0
clock = pygame.time.Clock()
running = True
screen = None
offsety = 113

BOARD = []

for i in range(7):
    temp = []
    for j in range(6):
        temp.append(None)

    BOARD.append([temp, 0])


class Circle:
    def __init__(
        self,
        surface: pygame.Surface,
        color: str,
        cords: Iterable,
        radius: int,
    ) -> None:
        self.surface = surface
        self.color = color
        self.cords_x, self.cords_y = cords
        self.radius = radius

    def draw(self):
        pygame.draw.circle(
            self.surface, self.color, (self.cords_x, self.cords_y), self.radius
        )


class Triangle:
    def __init__(self, surface: pygame.Surface, color: str, points: Iterable) -> None:
        self.surface = surface
        self.color = color
        self.p1, self.p2, self.p3 = points

        tri_points.append(points)

    def draw(self):
        pygame.draw.polygon(self.surface, self.color, (self.p1, self.p2, self.p3))


def point_in_triangle(v1, v2, v3, mouse_x, mouse_y):
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    d1 = sign((mouse_x, mouse_y), v1, v2)
    d2 = sign((mouse_x, mouse_y), v2, v3)
    d3 = sign((mouse_x, mouse_y), v3, v1)

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)


def setup(color: str):
    pygame.init()
    global screen
    screen = pygame.display.set_mode((1280, 800))

    startx = 200
    starty = 140

    offsetx = 140

    c = 7
    r = 6

    screen.fill("black")

    # Draw the board
    for i in range(c):
        for j in range(r):
            circle = Circle(
                screen, color, (startx + i * offsetx, starty + j * offsety), 45
            )
            circle.draw()
            if j == r - 1:
                available_circles.append([circle.cords_x, circle.cords_y])
    pygame.draw.rect(screen, color, (startx - 80, starty - 60, 1000, 700), 3)

    for i in range(c):
        triangle = Triangle(
            screen,
            "white",
            (
                (startx - 30 + i * offsetx, starty - 100),
                (startx + 30 + i * offsetx, starty - 100),
                (startx + i * offsetx, starty - 75),
            ),
        )
        triangle.draw()


def diagonals(t):
    ans = []
    for i in range(len(t)):
        for j in range(len(t[i])):
            temp = []
            right = 0
            down = 0
            while right + j < len(t[i]) and down + i < len(t):
                temp.append(t[i + down][j + right])
                right += 1
                down += 1

            ans.append(temp)

    return ans


def the_game():
    mouse_click = pygame.mouse.get_pressed()

    if mouse_click[0] == 1:
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        global curr_turn
        global turn_i
        for i, triangle_vertices in enumerate(tri_points):
            if point_in_triangle(*triangle_vertices, mouse_pos_x, mouse_pos_y):
                if BOARD[i][1] >= 6:
                    break

                x, y = available_circles[i]

                c = Circle(screen, curr_turn, (x, y), 45)
                c.draw()

                BOARD[i][0][BOARD[i][1]] = curr_turn
                BOARD[i][1] += 1

                available_circles[i][1] -= offsety
                turn_i += 1

                curr_turn = turns[turn_i % 2]

                clock.tick(10)

                break


def check_for_winner():
    # Check for a winner in rows
    for row in BOARD:
        left = 0
        right = 4
        while right <= len(row[0]):
            quad = row[0][left:right]
            if all(i == "red" for i in quad) or all(i == "blue" for i in quad):
                print(quad)
                return quad[0]

            right += 1
            left += 1

    # Check for a winner in columns
    for row in zip(*list(list(zip(*BOARD))[0])):
        left = 0
        right = 4
        while right <= len(row):
            quad = row[left:right]
            if all(i == "red" for i in quad) or all(i == "blue" for i in quad):
                print(quad)
                return quad[0]

            right += 1
            left += 1

    # Check for a winner in diagonals
    temp = [BOARD[i][0] for i in range(len(BOARD))]
    top_left = diagonals(temp)
    top_right = diagonals(temp[::-1])

    top_left = [i for i in top_left if len(i) >= 4]
    top_right = [i for i in top_right if len(i) >= 4]

    for row in top_right:
        left = 0
        right = 4
        while right <= len(row):
            quad = row[left:right]
            if all(i == "red" for i in quad) or all(i == "blue" for i in quad):
                print(quad)
                return quad[0]

            right += 1
            left += 1

    for row in top_left:
        left = 0
        right = 4
        while right <= len(row):
            quad = row[left:right]
            if all(i == "red" for i in quad) or all(i == "blue" for i in quad):
                print(quad)
                return quad[0]

            right += 1
            left += 1

    return None


def main():
    global running
    setup("white")

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        the_game()

        if check_for_winner() is not None:
            setup(check_for_winner())
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit(0)

                pygame.display.flip()
                clock.tick(60)

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()


if __name__ == "__main__":
    main()
