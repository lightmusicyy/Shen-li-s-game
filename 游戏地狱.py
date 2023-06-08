# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 23:06:35 2023

@author: yy
"""

import pygame
import random

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

# 下一关按钮
next_level_rect = pygame.Rect(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2, 100, 50)

# 重试按钮
retry_rect = pygame.Rect(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2 + 60, 100, 50)

def generate_terrain():
    terrain = []
    for _ in range(30):
        while True:
            w = random.randint(20, 50)
            h = random.randint(20, 50)
            x = random.randint(0, WINDOW_WIDTH - w)
            y = random.randint(0, WINDOW_HEIGHT - h)
            rect = pygame.Rect(x, y, w, h)
            if not char_rect.colliderect(rect):
                terrain.append([rect, [random.choice([1, -1]), random.choice([1, -1])]])
                break
    return terrain

terrain = generate_terrain()

speed = 5

# 游戏主循环
run = True
next_level = False
game_over = False
levels = 0
while run:
    pygame.time.delay(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if next_level and next_level_rect.collidepoint(event.pos):
                char_rect.topleft = (0, 0)
                terrain = generate_terrain()
                next_level = False
                game_over = False
                levels += 1
            if game_over and retry_rect.collidepoint(event.pos):
                char_rect.topleft = (0, 0)
                terrain = generate_terrain()
                game_over = False
                levels = 0

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            char_rect.move_ip(-speed, 0)
        if keys[pygame.K_RIGHT]:
            char_rect.move_ip(speed, 0)
        if keys[pygame.K_UP]:
            char_rect.move_ip(0, -speed)
        if keys[pygame.K_DOWN]:
            char_rect.move_ip(0, speed)

        # 碰撞检测
        for item in terrain:
            rect, dir = item
            if char_rect.colliderect(rect):
                game_over = True
                break

    window.fill((0, 0, 0))
    window.blit(character, char_rect)

    # 移动地形
    for item in terrain:
        rect, dir = item
        rect.move_ip(*dir)
        if rect.left < 0 or rect.right > WINDOW_WIDTH:
            dir[0] *= -1
        if rect.top < 0 or rect.bottom > WINDOW_HEIGHT:
            dir[1] *= -1
        pygame.draw.rect(window, (255, 255, 255), rect)

    if game_over:
        text = font.render("Failed", True, (255, 0, 0))
        window.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2))
        pygame.draw.rect(window, (0, 255, 0), retry_rect)
        retry_text = font.render("Try Again", True, (255, 255, 255))
        window.blit(retry_text, (retry_rect.x + 50 - retry_text.get_width() // 2, retry_rect.y + 25 - retry_text.get_height() // 2))
    else:
        # 检查是否到达右下角
        if WINDOW_WIDTH - char_rect.right < speed and WINDOW_HEIGHT - char_rect.bottom < speed:
            text = font.render("Congratulations", True, (255, 0, 0))
            window.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2))
            pygame.draw.rect(window, (0, 255, 0), next_level_rect)
            next_text = font.render("Next Level", True, (255, 255, 255))
            window.blit(next_text, (next_level_rect.x + 50 - next_text.get_width() // 2, next_level_rect.y + 25 - next_text.get_height() // 2))
            next_level = True

    # 在界面上标注过关条件
    condition_text = font.render("Aim:go to the bottom right corner", True, (100, 100, 100))
    window.blit(condition_text, (0, 0))

    # 在右下角设置通关字样
    target_text = font.render("Customs clearance area", True, (255, 255, 255))
    window.blit(target_text, (WINDOW_WIDTH - target_text.get_width(), WINDOW_HEIGHT - target_text.get_height()))

    # 记录已通过的关卡数
    levels_text = font.render("Hell layers:" + str(levels), True, (255, 255, 255))
    window.blit(levels_text, (0, 30))

    pygame.display.update()

pygame.quit()
