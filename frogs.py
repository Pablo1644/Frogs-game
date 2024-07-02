import pygame
import random
import ctypes
from make_frogs import make_frogs

running = True
pygame.init()

bg = pygame.image.load("bg.png")
bg_width, bg_height = bg.get_width(), bg.get_height()
screen = pygame.display.set_mode((bg_width, bg_height))

screen.blit(bg, (0, 0))
pygame.display.set_caption('ŻABKI')
programIcon = pygame.image.load('frogICON.jpg ')
pygame.display.set_icon(programIcon)

font = pygame.font.Font(None, 40)


class Frog:
    def __init__(self):
        self.size = 40
        self.X = 100
        self.Y = 200
        self.nr_of_frogs = 9
        self.frogs = []
        self.frog_images = []  # List to store frog images
        self.selected_frog_index = None  # Track which frog is selected
        self.can_move_up = [False] * self.nr_of_frogs  # Track if each frog can move up
        self.can_move_down = [False] * self.nr_of_frogs  # Track if each frog can move down
        self.sibling_moved_up = False  # Track if a sibling frog has moved up
        make_frogs(self.nr_of_frogs)
        # Create rectangles for each frog
        for i in range(self.nr_of_frogs):
            frog_rect = pygame.Rect(self.X + 2 * i * self.size, self.Y, self.size, self.size)
            self.frogs.append(frog_rect)

        self.frog_indices = list(range(1, self.nr_of_frogs + 1))
        random.shuffle(self.frog_indices)  # List for numbers for frogs

        self.counter = 0  # counter for counting moves

    def setup(self):
        self.frog_images = []  # Clear previous images to reload
        for i in self.frog_indices:
            frog_image = pygame.image.load(f'{i}.png')  # Adjust to load correct images
            self.frog_images.append(frog_image)

        for idx, froggy in enumerate(self.frogs):
            frog_image = self.frog_images[idx]
            screen.blit(frog_image, froggy.topleft)  # Draw each frog image

    def move(self):
        if self.selected_frog_index is not None:
            if self.can_move_up[self.selected_frog_index]:
                self.frogs[self.selected_frog_index].y -= self.size  # Move selected frog up
                self.can_move_up[self.selected_frog_index] = False
                self.can_move_down[self.selected_frog_index] = True  # Allow moving down after moving up
                self.sibling_moved_up = True  # Mark that a sibling frog has moved up
                return True  # Return True indicating a frog was moved up
            elif self.can_move_down[self.selected_frog_index]:
                self.frogs[self.selected_frog_index].y += self.size  # Move selected frog down
                self.can_move_down[self.selected_frog_index] = False  # Reset the move down flag after moving down
                self.selected_frog_index = None  # Deselect the frog after it has moved down
        return False

    def transition(self, move_right):
        if move_right:
            self.frogs[self.selected_frog_index + 1].x -= 2 * self.size
            self.frogs[self.selected_frog_index].x += 2 * self.size
            self.frogs[self.selected_frog_index].y += self.size
            # Swap positions in the list
            self.frogs[self.selected_frog_index], self.frogs[self.selected_frog_index + 1] = (
                self.frogs[self.selected_frog_index + 1],
                self.frogs[self.selected_frog_index],
            )
            self.frog_indices[self.selected_frog_index], self.frog_indices[self.selected_frog_index + 1] = (
                self.frog_indices[self.selected_frog_index + 1],
                self.frog_indices[self.selected_frog_index],
            )
        else:
            self.frogs[self.selected_frog_index - 1].x += 2 * self.size
            self.frogs[self.selected_frog_index].x -= 2 * self.size
            self.frogs[self.selected_frog_index].y += self.size
            # Swap positions in the list
            self.frogs[self.selected_frog_index], self.frogs[self.selected_frog_index - 1] = (
                self.frogs[self.selected_frog_index - 1],
                self.frogs[self.selected_frog_index],
            )
            self.frog_indices[self.selected_frog_index], self.frog_indices[self.selected_frog_index - 1] = (
                self.frog_indices[self.selected_frog_index - 1],
                self.frog_indices[self.selected_frog_index],
            )


        self.selected_frog_index = None  # Deselect the frog after transition
        self.sibling_moved_up = False  # Reset the sibling moved up flag
        # Reset all frogs to prevent them from moving up or down until explicitly allowed again
        self.can_move_up = [False] * self.nr_of_frogs
        self.can_move_down = [False] * self.nr_of_frogs

    def is_clicked(self, pos):
        if self.selected_frog_index is None:  # Allow selection only if no frog is currently selected
            for idx, froggy in enumerate(self.frogs):
                if froggy.collidepoint(pos):
                    if idx > 0 and self.can_move_up[idx - 1]:
                        pass
                    if idx < self.nr_of_frogs - 1 and self.can_move_up[idx + 1]:
                        pass

                    self.selected_frog_index = idx
                    if not self.can_move_up[idx] and not self.can_move_down[idx]:
                        self.can_move_up[idx] = True
                    self.move()
                    return True
        else:  # A frog is currently selected
            selected_frog_idx = self.selected_frog_index
            froggy = self.frogs[selected_frog_idx]
            if froggy.collidepoint(pos):
                self.move()
                return True
            else:
                # Check if the clicked position is on an adjacent frog
                for idx, adjacent_frog in enumerate(self.frogs):
                    if adjacent_frog.collidepoint(pos):
                        if idx == selected_frog_idx - 1 or idx == selected_frog_idx + 1:
                            if self.sibling_moved_up:  # Check if sibling frog was moved up
                                self.transition(idx == selected_frog_idx + 1)
                                self.counter += 1

                                return True
        return False

    def get_frog_indices(self):
        return self.frog_indices


frog = Frog()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if frog.is_clicked(event.pos):
                pass  # Movement handled in is_clicked

    screen.blit(bg, (0, 0))  # Blit the background image

    frog.setup()  # Draw all frogs at their current positions
    ind = frog.get_frog_indices()
    if ind == [i for i in range(1, len(ind) + 1)]:
        ctypes.windll.user32.MessageBoxW(0, "END OF GAME WITH MOVES: "+str(frog.counter), "YOU WON!", 48)
        running = False

    counter_text = f"MOVES: {frog.counter}"
    text_surface = font.render(counter_text, True, (100, 100, 100))  # Render text surface
    text_rect = text_surface.get_rect(center=(bg_width // 2, bg_height // 2))  # Center text
    screen.blit(text_surface, text_rect)  # Blit text onto screen

    pygame.display.update()  # Update the display to show the changes
