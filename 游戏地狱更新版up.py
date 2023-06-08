import pygame
import random
import math
import numpy as np
# 设置窗口大小
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# 初始化 Pygame
pygame.init()

# 创建窗口
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 加载角色图像
character = pygame.image.load('1.png')
character = pygame.transform.scale(character, (WINDOW_WIDTH // 10, WINDOW_HEIGHT // 10))

font = pygame.font.Font(None, 36)

# 角色的位置和大小
char_rect = character.get_rect(topleft=(0, 0))

# 创建关卡选择按钮
level_buttons = []
for i in range(1, 21):
    rect = pygame.Rect(50 * ((i - 1) % 5), 100 + 50 * ((i - 1) // 5), 40, 40)
    level_buttons.append(rect)

# 游戏状态
state = 'level_select'

# 游戏主循环
run = True
levels = 0

def generate_terrain():
    terrain = []
    for _ in range(5 + 5*round(math.log(5 * (levels + 1)))):
        while True:
            w = random.randint(20, 50)
            h = random.randint(20, 50)
            x = random.randint(0, WINDOW_WIDTH - w)
            y = random.randint(0, WINDOW_HEIGHT - h)
            rect = pygame.Rect(x, y, w, h)
            if not char_rect.colliderect(rect):
                dir = [random.choice([1, -1]) * (1 + 0.1 * levels), random.choice([1, -1]) * (1 + 0.1 * levels)]
                terrain.append([rect, dir])
                break
    return terrain

terrain = generate_terrain()

speed = 5
invincible_time = 0
success_time = 0

while run:
    pygame.time.delay(50)
    invincible_time += 1
    success_time += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # 在关卡选择状态下处理鼠标点击
        elif state == 'level_select' and event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(level_buttons, 1):
                if rect.collidepoint(event.pos):
                    state = 'playing'
                    levels = i
                    terrain = generate_terrain()
                    invincible_time = 0
                    success_time = 0
                    char_rect.topleft = (0, 0)
                    break

        # 在游戏结束状态下处理鼠标点击
        elif state == 'game_over' and event.type == pygame.MOUSEBUTTONDOWN:
            if retry_rect.collidepoint(event.pos):
                state = 'level_select'
                levels = 0

        # 在成功通关状态下处理鼠标点击
        elif state == 'level_clear' and event.type == pygame.MOUSEBUTTONDOWN:
            if next_level_rect.collidepoint(event.pos):
                state = 'playing'
                levels += 1
                terrain = generate_terrain()
                invincible_time = 0
                success_time = 0
                char_rect.topleft = (0, 0)
            elif choose_level_rect.collidepoint(event.pos):
                state = 'level_select'
                levels = 0

    if state == 'playing':
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and char_rect.left - speed >= 0:
            char_rect.move_ip(-speed, 0)
        if keys[pygame.K_RIGHT] and char_rect.right + speed <= WINDOW_WIDTH:
            char_rect.move_ip(speed, 0)
        if keys[pygame.K_UP] and char_rect.top - speed >= 0:
            char_rect.move_ip(0, -speed)
        if keys[pygame.K_DOWN] and char_rect.bottom + speed <= WINDOW_HEIGHT:
            char_rect.move_ip(0, speed)

        # 碰撞检测
        if invincible_time > 40:  # 2秒无敌时间结束
            for item in terrain:
                rect, dir = item
                if char_rect.colliderect(rect):
                    state = 'game_over'
                    break

        # 移动地形
        for item in terrain:
            rect, dir = item
            rect.move_ip(*dir)

            if rect.left < 0 or rect.right > WINDOW_WIDTH:
                dir[0] *= -1
            if rect.top < 0 or rect.bottom > WINDOW_HEIGHT:
                dir[1] *= -1

    window.fill((0, 0, 0))

    # 在关卡选择状态下绘制关卡按钮
    if state == 'level_select':
        for i, rect in enumerate(level_buttons, 1):
            pygame.draw.rect(window, (0, 255, 0), rect)
            level_text = font.render(str(i), True, (0, 0, 0))
            window.blit(level_text, (rect.x + 20 - level_text.get_width() // 2, rect.y + 20 - level_text.get_height() // 2))
        level_select_text = font.render("Choice your level", True, (255, 255, 255))
        window.blit(level_select_text, (WINDOW_WIDTH // 2 - level_select_text.get_width() // 2, 50))

    # 在玩游戏状态下更新和绘制游戏
    elif state == 'playing':
        # 绘制地形
        for item in terrain:
            rect, _ = item
            pygame.draw.rect(window, (255, 255, 255), rect)

        # 如果处于无敌状态，让角色闪烁，结束后一直显示
        if invincible_time <= 40:
            if invincible_time % 10 < 5:
                window.blit(character, char_rect)
        else:
            window.blit(character, char_rect)

        # 检查是否到达右下角
        if WINDOW_WIDTH - char_rect.right < speed and WINDOW_HEIGHT - char_rect.bottom < speed:
            state = 'level_clear'
            success_time = 0

    # 在游戏结束状态下绘制游戏结束屏幕
    elif state == 'game_over':
        text = font.render("Failed", True, (255, 0, 0))
        window.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2))
        retry_rect = pygame.Rect(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2 + 60, 100, 50)
        pygame.draw.rect(window, (0, 255, 0), retry_rect)
        retry_text = font.render("Try Again", True, (255, 255, 255))
        window.blit(retry_text, (retry_rect.x + 50 - retry_text.get_width() // 2, retry_rect.y + 25 - retry_text.get_height() // 2))
        levels = 0

    # 在关卡成功通关状态下绘制按钮选项
    elif state == 'level_clear':
        next_level_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2, 200, 50)
        choose_level_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 60, 200, 50)
        pygame.draw.rect(window, (0, 255, 0), next_level_rect)
        pygame.draw.rect(window, (0, 0, 255), choose_level_rect)
        next_text = font.render("Next Levels", True, (255, 255, 255))
        choose_text = font.render("Choose My Level", True, (255, 255, 255))
        window.blit(next_text, (next_level_rect.x + 100 - next_text.get_width() // 2, next_level_rect.y + 25 - next_text.get_height() // 2))
        window.blit(choose_text, (choose_level_rect.x + 100 - choose_text.get_width() // 2, choose_level_rect.y + 25 - choose_text.get_height() // 2))
    # 在界面上标注过关条件
    condition_text = font.render("Aim:go to the bottom right corner", True, (255, 255, 255))
    window.blit(condition_text, (0, 0))

    # 在右下角设置通关字样
    target_text = font.render("Customs clearance area", True, (255, 255, 255))
    window.blit(target_text, (WINDOW_WIDTH - target_text.get_width(), WINDOW_HEIGHT - target_text.get_height()))

    # 记录已通过的关卡数
    levels_text = font.render("Hell layers:" + str(levels), True, (255, 255, 255))
    window.blit(levels_text, (0, 30))
    pygame.display.update()

pygame.quit()
