import pygame
import sys
import random
import pickle
import os

pygame.init()

# Images
barrier_img = pygame.image.load("assets/barrier.png")
tree_img = pygame.image.load("assets/tree.png")
barrier_img = pygame.transform.scale(barrier_img, (30, 30))
tree_img = pygame.transform.scale(tree_img, (30, 30))

# Display settings
window_size = 600
instruction_area_height = 220
screen = pygame.display.set_mode((window_size, window_size + instruction_area_height))
pygame.display.set_caption("Noise Pollution Simulator")

# Grid settings
grid_size = 5
cell_size = window_size // grid_size

font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 36, bold=True)

# Placement types
EMPTY = 0
BARRIER = 1
TREE = 2

# Sounds
select_sound = None
reduce_sound = None
if os.path.exists("assets/select.wav"):
    select_sound = pygame.mixer.Sound("assets/select.wav")
if os.path.exists("assets/reduce.wav"):
    reduce_sound = pygame.mixer.Sound("assets/reduce.wav")

# Levels definition
levels = [
    {"barriers":6, "trees":8},
    {"barriers":4, "trees":6},
    {"barriers":2, "trees":4}
]
current_level = 0

def create_grid():
    return [[{"noise": random.randint(50,90), "barriers":0, "trees":0} for _ in range(grid_size)] for _ in range(grid_size)]

grid = create_grid()
selected_cell = None
show_instructions = False
barriers_left = levels[current_level]["barriers"]
trees_left = levels[current_level]["trees"]
running = True
win = False
lose = False
game_completed = False
fade_alpha = 0
action_history = []   # NEW: store history for undo

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not (win or lose or game_completed):
                mx, my = pygame.mouse.get_pos()
                if my <= window_size:
                    col = mx // cell_size
                    row = my // cell_size
                    selected_cell = (row, col)
                    if select_sound:
                        select_sound.play()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                show_instructions = not show_instructions
            if event.key == pygame.K_s:
                with open("grid_state.pkl", "wb") as f:
                    pickle.dump((grid, current_level, barriers_left, trees_left, action_history), f)
            if event.key == pygame.K_l:
                if os.path.exists("grid_state.pkl"):
                    with open("grid_state.pkl", "rb") as f:
                        grid, current_level, barriers_left, trees_left, action_history = pickle.load(f)
                    win = lose = game_completed = False
                    fade_alpha = 0
            if event.key == pygame.K_n:
                grid = create_grid()
                current_level = 0
                barriers_left = levels[current_level]["barriers"]
                trees_left = levels[current_level]["trees"]
                win = lose = game_completed = False
                fade_alpha = 0
                action_history = []
            if event.key == pygame.K_u and action_history:
                last_action, (r,c) = action_history.pop()
                if last_action == "barrier":
                    grid[r][c]["noise"] +=10
                    grid[r][c]["barriers"] -=1
                    barriers_left +=1
                elif last_action == "tree":
                    grid[r][c]["noise"] +=5
                    grid[r][c]["trees"] -=1
                    trees_left +=1
            if selected_cell and not (win or lose or game_completed):
                r, c = selected_cell
                if event.key == pygame.K_r and barriers_left > 0:
                    grid[r][c]["noise"] = max(30, grid[r][c]["noise"] -10)
                    grid[r][c]["barriers"] +=1
                    barriers_left -=1
                    action_history.append(("barrier",(r,c)))
                    if reduce_sound:
                        reduce_sound.play()
                if event.key == pygame.K_t and trees_left >0:
                    grid[r][c]["noise"] = max(30, grid[r][c]["noise"] -5)
                    grid[r][c]["trees"] +=1
                    trees_left -=1
                    action_history.append(("tree",(r,c)))
                    if reduce_sound:
                        reduce_sound.play()

    total_noise = sum(cell["noise"] for row in grid for cell in row)
    num_cells = grid_size*grid_size
    avg_noise = total_noise / num_cells

    if avg_noise<60 and not lose and not game_completed:
        if current_level<2:
            win = True
        else:
            game_completed = True

    if (barriers_left==0 and trees_left==0 and avg_noise>=60 and not win):
        lose = True

    screen.fill((230,230,230))

    for r in range(grid_size):
        for c in range(grid_size):
            cell=grid[r][c]
            noise=cell["noise"]
            if noise<60:
                color=(144,238,144)
            elif noise<75:
                color=(255,255,153)
            else:
                color=(255,153,153)
            x=c*cell_size
            y=r*cell_size
            pygame.draw.rect(screen,color,(x,y,cell_size-2,cell_size-2))
            txt=font.render(str(noise),True,(0,0,0))
            screen.blit(txt,txt.get_rect(center=(x+cell_size//2,y+cell_size//2)))
            if selected_cell==(r,c):
                pygame.draw.rect(screen,(0,0,255),(x,y,cell_size-2,cell_size-2),3)
            # NEW: draw barriers
            for i in range(cell["barriers"]):
                screen.blit(barrier_img, (x+5+i*15, y+5))
            # NEW: draw trees
            for i in range(cell["trees"]):
                screen.blit(tree_img, (x+5+i*15, y+35))

    avg_text = font.render(f"Average Noise: {avg_noise:.1f} dB", True, (0,0,0))
    screen.blit(avg_text, (10, window_size + 5))
    lvl_text = font.render(f"Level {current_level+1}/3", True, (0,0,0))
    screen.blit(lvl_text, (10, window_size + 30))
    ctrl_text1 = font.render("H=Help S=Save L=Load U=Undo", True, (0,0,0))
    ctrl_text2 = font.render("N=New Game", True, (0,0,0))
    screen.blit(ctrl_text1, (300, window_size + 5))
    screen.blit(ctrl_text2, (300, window_size + 30))

    if show_instructions:
        instructions = [
            "Click a cell to select.",
            f"R = Barrier (-10 dB) [{barriers_left}]",
            f"T = Trees (-5 dB) [{trees_left}]",
            "U = Undo last action.",
            "Reduce average noise below 60 dB.",
            "Win to proceed to next level.",
            "N = New Game"
        ]
        base_y = window_size + 60
        for i, line in enumerate(instructions):
            inst = font.render(line, True, (0,0,0))
            screen.blit(inst, (10, base_y + i*22))

    if win or lose or game_completed:
        fade_alpha = min(fade_alpha+5,150)
        overlay = pygame.Surface((window_size,window_size))
        overlay.set_alpha(fade_alpha)
        overlay.fill((255,255,255))
        screen.blit(overlay,(0,0))
        if win:
            msg = "Level Cleared! Press N for Next Level."
            m_surf=big_font.render(msg,True,(0,128,0))
            screen.blit(m_surf,m_surf.get_rect(center=(window_size//2,window_size//2)))
        if lose:
            msg="You Lost! Press N to Retry."
            m_surf=big_font.render(msg,True,(200,0,0))
            screen.blit(m_surf,m_surf.get_rect(center=(window_size//2,window_size//2)))
        if game_completed:
            msg="All Levels Completed!"
            m_surf=big_font.render(msg,True,(0,128,0))
            screen.blit(m_surf,m_surf.get_rect(center=(window_size//2,window_size//2)))

    pygame.display.flip()

    if win and not game_completed:
        pygame.time.wait(1500)
        current_level+=1
        grid=create_grid()
        barriers_left=levels[current_level]["barriers"]
        trees_left=levels[current_level]["trees"]
        win=False
        fade_alpha=0
        action_history = []

pygame.quit()
sys.exit()
