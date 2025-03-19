import pygame
import random
import time  # 시간 측정을 위한 모듈 추가

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("비행기 장애물 피하기")

# 색상
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 비행기 설정
plane_width, plane_height = 50, 50
plane_x = WIDTH // 2 - plane_width // 2
plane_y = HEIGHT - 100
plane_speed = 8

# 장애물 설정
obstacle_width, obstacle_height = 60, 60
obstacle_x = random.randint(0, WIDTH - obstacle_width)
obstacle_y = -50
obstacle_speed = 12

# 추가 장애물 설정
extra_obstacle_x = random.randint(0, WIDTH - obstacle_width)
extra_obstacle_y = -50
extra_obstacle_active = False  # 추가 장애물 활성화 여부

# 점수 설정
score = 0
font = pygame.font.SysFont(None, 36)  # 점수를 표시할 폰트 설정

# 게임 시작 시간 기록
start_time = time.time()

# 게임 루프
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 키 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and plane_x > 0:
        plane_x -= plane_speed
    if keys[pygame.K_RIGHT] and plane_x < WIDTH - plane_width:
        plane_x += plane_speed
    
    # 1분 경과 시 장애물 속도 증가 및 추가 장애물 활성화
    elapsed_time = time.time() - start_time
    if elapsed_time > 60 and not extra_obstacle_active:
        obstacle_speed *= 2
        extra_obstacle_active = True

    # 장애물 이동
    obstacle_y += obstacle_speed
    if obstacle_y > HEIGHT:
        obstacle_y = -50
        obstacle_x = random.randint(0, WIDTH - obstacle_width)
        score += 1  # 장애물을 피할 때 점수 증가

    # 추가 장애물 이동
    if extra_obstacle_active:
        extra_obstacle_y += obstacle_speed
        if extra_obstacle_y > HEIGHT:
            extra_obstacle_y = -50
            extra_obstacle_x = random.randint(0, WIDTH - obstacle_width)
            score += 1  # 추가 장애물을 피할 때 점수 증가

    # 충돌 체크
    if (plane_x < obstacle_x + obstacle_width and
        plane_x + plane_width > obstacle_x and
        plane_y < obstacle_y + obstacle_height and
        plane_y + plane_height > obstacle_y):
        print("게임 오버!")
        running = False

    if extra_obstacle_active and (
        plane_x < extra_obstacle_x + obstacle_width and
        plane_x + plane_width > extra_obstacle_x and
        plane_y < extra_obstacle_y + obstacle_height and
        plane_y + plane_height > extra_obstacle_y):
        print("게임 오버!")
        running = False

    # 비행기 & 장애물 그리기
    pygame.draw.rect(screen, (0, 0, 255), (plane_x, plane_y, plane_width, plane_height))
    pygame.draw.rect(screen, RED, (obstacle_x, obstacle_y, obstacle_width, obstacle_height))
    if extra_obstacle_active:
        pygame.draw.rect(screen, RED, (extra_obstacle_x, extra_obstacle_y, obstacle_width, obstacle_height))
    
    # 점수 표시
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))  # 검은색 텍스트
    screen.blit(score_text, (10, 10))  # 왼쪽 상단에 점수 표시
    
    pygame.display.update()
    clock.tick(30)

# 게임 종료 후 점수 표시
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Pygame 화면 다시 설정
screen.fill(WHITE)
game_over_text = font.render("게임 오버!", True, (0, 0, 0))  # 검은색 텍스트
score_text = font.render(f"최종 점수: {score}", True, (0, 0, 0))  # 검은색 텍스트
screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 10))
pygame.display.update()
pygame.time.delay(4000)  # 4초 대기

pygame.quit()  # Pygame 종료 호출을 여기로 이동
