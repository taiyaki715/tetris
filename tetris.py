import copy
import pygame
from pygame.locals import *
import random
import sys
import threading
import time


class Block:
    I_BLOCK = [[[1, 1, 1, 1],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]],
               [[0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0]],
               [[1, 1, 1, 1],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]],
               [[0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0]]]

    L_BLOCK = [[[0, 0, 1],
                [1, 1, 1],
                [0, 0, 0]],
               [[0, 1, 0],
                [0, 1, 0],
                [0, 1, 1]],
               [[0, 0, 0],
                [1, 1, 1],
                [1, 0, 0]],
               [[1, 1, 0],
                [0, 1, 0],
                [0, 1, 0]]]

    J_BLOCK = [[[1, 0, 0],
                [1, 1, 1],
                [0, 0, 0]],
               [[0, 1, 1],
                [0, 1, 0],
                [0, 1, 0]],
               [[0, 0, 0],
                [1, 1, 1],
                [0, 0, 1]],
               [[0, 1, 0],
                [0, 1, 0],
                [1, 1, 0]]]

    Z_BLOCK = [[[1, 1, 0],
                [0, 1, 1],
                [0, 0, 0]],
               [[0, 0, 1],
                [0, 1, 1],
                [0, 1, 0]],
               [[0, 0, 0],
                [1, 1, 0],
                [0, 1, 1]],
               [[0, 1, 0],
                [1, 1, 0],
                [1, 0, 0]]]

    S_BLOCK = [[[0, 1, 1],
                [1, 1, 0],
                [0, 0, 0]],
               [[0, 1, 0],
                [0, 1, 1],
                [0, 0, 1]],
               [[0, 0, 0],
                [0, 1, 1],
                [1, 1, 0]],
               [[1, 0, 0],
                [1, 1, 0],
                [0, 1, 0]]]

    T_BLOCK = [[[0, 1, 0],
                [1, 1, 1],
                [0, 0, 0]],
               [[0, 1, 0],
                [0, 1, 1],
                [0, 1, 0]],
               [[0, 0, 0],
                [1, 1, 1],
                [0, 1, 0]],
               [[0, 1, 0],
                [1, 1, 0],
                [0, 1, 0]]]

    O_BLOCK = [[[1, 1],
               [1, 1]]]

    def __init__(self, block, x=3, y=0):
        self.position_x = x  # x位置
        self.position_y = y  # y位置
        self.rotation = 0  # 回転状態
        self.block = None  # 配列格納用

        if block == 0:
            self.block_type = self.I_BLOCK
            self.color = (80, 255, 255)

        elif block == 1:
            self.block_type = self.L_BLOCK
            self.color = (255, 127, 80)

        elif block == 2:
            self.block_type = self.J_BLOCK
            self.color = (100, 100, 255)

        elif block == 3:
            self.block_type = self.Z_BLOCK
            self.color = (255, 80, 100)

        elif block == 4:
            self.block_type = self.S_BLOCK
            self.color = (80, 255, 80)

        elif block == 5:
            self.block_type = self.T_BLOCK
            self.color = (255, 80, 255)

        elif block == 6:
            self.block_type = self.O_BLOCK
            self.color = (255, 255, 100)

        self.update()

    def update(self):
        # ブロックの配列を更新
        self.block = self.block_type[self.rotation]

    def get(self):
        # ブロックの配列を取得
        return self.block

    def move(self, direction):
        # ブロックを移動
        if direction == 0:
            self.position_x += 1
        if direction == 1:
            self.position_x -= 1
        if direction == 2:
            self.position_y += 1
        if direction == 3:
            self.position_y -= 1

    def rotate(self):
        # ブロックを回転
        if not self.block_type == self.O_BLOCK:
            self.rotation += 1
        if self.rotation == 4:
            self.rotation = 0
        self.update()

    def get_rotated(self):
        # 回転後のインスタンスを取得
        dup = copy.deepcopy(self)
        dup.rotate()
        return dup

    def get_size(self):
        # ブロックの配列サイズを取得
        return len(self.block), len(self.block[0])


class Game:
    WINDOW_WIDTH = 600  # ウィンドウの幅
    WINDOW_HEIGHT = 600  # ウィンドウの高さ
    BOARD_WIDTH = 300  # ゲームボードの幅
    BOARD_HEIGHT = 600  # ゲームボードの高さ
    BOARD_OFFSET_X = 0  # ゲームボードのx方向の偏差
    BOARD_OFFSET_Y = 0  # ゲームボードのy方向の偏差
    BG_COLOR = (50, 50, 50)  # 背景色
    LINE_COLOR = (200, 200, 200)  # 背景線の色
    LINE_WIDTH = 1  # 背景線の太さ
    N_LINES_X = 10  # ゲームボードのX方向サイズ
    N_LINES_Y = 20  # ゲームボードのY方向サイズ
    SCORE_BOARD_X = 320  # スコア表示のX座標
    SCORE_BOARD_Y = 30  # スコア表示のY座標
    FPS = 30  # フレームレート

    def __init__(self):
        # ボードデータ管理用リスト生成
        self.record = [[(0, 0, 0) for j in range(self.N_LINES_X)] for i in range(self.N_LINES_Y)]

        # 得点管理用変数初期化
        self.score = 0
        self.n_deleted_lines = 0

        # pygame初期化
        pygame.init()
        self.font = pygame.font.Font(None, 40)

        # ウィンドウ設定
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption('TETRIS')

        # 最初のブロックを設定
        self.current_block = Block(random.randint(0, 6))

        self.clock = pygame.time.Clock()

    def main(self):
        self.main_menu()
        # メインループ
        while True:
            # フレームレート設定
            self.clock.tick(self.FPS)
            # キーボードイベント処理
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        if 'right' not in self.hit():
                            self.current_block.move(0)
                    if event.key == K_LEFT:
                        if 'left' not in self.hit():
                            self.current_block.move(1)
                    if event.key == K_r:
                        if self.can_rotate():
                            self.current_block.rotate()
            key = pygame.key.get_pressed()
            if key[K_DOWN]:
                if pygame.time.get_ticks() % 1 == 0:
                    self.current_block.move(2)

            # ブロック自動落下処理
            elif pygame.time.get_ticks() % 1000 < 35:
                self.current_block.move(2)

            # ブロックが一番下に付いたときの処理
            if 'bottom' in self.hit():
                self.set()
                self.current_block = Block(random.randint(0, 6))

            # 列消しチェック
            n_deleted_lines = self.check_line()
            if n_deleted_lines:
                self.score += n_deleted_lines * 300

            # ゲームオーバーチェック
            self.check_gameover()

            # ディスプレイ更新
            self.screen.fill(self.BG_COLOR)
            self.draw_board()
            self.draw_score()
            pygame.display.update()

            time.sleep(0.0005)

    def main_menu(self):
        flag_start_game = False  # ゲーム開始フラグ

        while True:
            # マウス位置取得
            mouse_pos = pygame.mouse.get_pos()

            # イベント取得
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    flag_start_game = True

            # ボタンクリック、色変化処理
            if self.WINDOW_WIDTH//2-150 < mouse_pos[0] < self.WINDOW_WIDTH//2+150 and \
                    self.WINDOW_HEIGHT//2-50 < mouse_pos[1] < self.WINDOW_HEIGHT//2:
                button_color = (255, 70, 70)
                if flag_start_game:
                    time.sleep(0.3)
                    break
            else:
                button_color = (255, 255, 255)

            # 描画
            self.screen.fill(self.BG_COLOR)
            pygame.draw.rect(self.screen, button_color,
                             (self.WINDOW_WIDTH//2-150, self.WINDOW_HEIGHT//2-50, 300, 50))
            text_start = self.font.render('START', True, (30, 30, 30))
            self.screen.blit(text_start, (self.WINDOW_WIDTH//2-50, self.WINDOW_HEIGHT//2-40))
            pygame.display.update()

    def draw_board(self):
        # 縦線を描画
        for i in range(self.N_LINES_X):
            pygame.draw.line(self.screen, self.LINE_COLOR,
                             (int(self.BOARD_WIDTH/self.N_LINES_X*i+self.BOARD_OFFSET_X), 0),
                             (int(self.BOARD_WIDTH/self.N_LINES_X*i+self.BOARD_OFFSET_X), self.BOARD_HEIGHT),
                             self.LINE_WIDTH)

        # 横線を描画
        for i in range(self.N_LINES_Y):
            pygame.draw.line(self.screen, self.LINE_COLOR,
                             (self.BOARD_OFFSET_X,
                              int(self.BOARD_HEIGHT/self.N_LINES_Y*i+self.BOARD_OFFSET_Y+self.BOARD_OFFSET_Y)),
                             (self.BOARD_WIDTH+self.BOARD_OFFSET_X,
                              int(self.BOARD_HEIGHT/self.N_LINES_Y*i+self.BOARD_OFFSET_Y+self.BOARD_OFFSET_Y)),
                             self.LINE_WIDTH)

        # 配置されたブロックを描画
        for y in range(self.N_LINES_Y):
            for x in range(self.N_LINES_X):
                if self.record[y][x] != (0, 0, 0):
                    self.draw_block(x, y, self.record[y][x])

        # 操作中のブロックを描画
        for y in range(self.current_block.get_size()[0]):
            for x in range(self.current_block.get_size()[1]):
                if self.current_block.get()[y][x] != 0:
                    self.draw_block(self.current_block.position_x+x, self.current_block.position_y+y,
                                    self.current_block.color)

    def draw_block(self, x, y, c):
        # ブロックの周りの影
        pygame.draw.rect(self.screen, (c[0]/10*5, c[1]/10*5, c[2]/10*5),
                         (self.BOARD_WIDTH//self.N_LINES_X*x+self.BOARD_OFFSET_X,
                          self.BOARD_HEIGHT//self.N_LINES_Y*y+self.BOARD_OFFSET_Y,
                          self.BOARD_WIDTH//self.N_LINES_X,
                          self.BOARD_HEIGHT//self.N_LINES_Y), 2)

        # ブロックの角の影
        pygame.draw.line(self.screen, (c[0]/10*2, c[1]/10*2, c[2]/10*2),
                         (self.BOARD_WIDTH//self.N_LINES_X*x+self.BOARD_OFFSET_X,
                          self.BOARD_HEIGHT//self.N_LINES_Y*y+self.BOARD_OFFSET_Y),
                         (self.BOARD_WIDTH//self.N_LINES_X*x+self.BOARD_WIDTH//self.N_LINES_X+self.BOARD_OFFSET_X,
                          self.BOARD_HEIGHT//self.N_LINES_Y*y+self.BOARD_HEIGHT//self.N_LINES_Y+self.BOARD_OFFSET_Y))
        pygame.draw.line(self.screen, (c[0]/10*2, c[1]/10*2, c[2]/10*2),
                         (self.BOARD_WIDTH//self.N_LINES_X*x+self.BOARD_WIDTH//self.N_LINES_X+self.BOARD_OFFSET_X,
                          self.BOARD_HEIGHT//self.N_LINES_Y*y+self.BOARD_OFFSET_Y),
                         (self.BOARD_WIDTH//self.N_LINES_X*x+self.BOARD_OFFSET_X,
                          self.BOARD_HEIGHT//self.N_LINES_Y*y+self.BOARD_HEIGHT//self.N_LINES_Y+self.BOARD_OFFSET_Y))

        # ブロック本体
        pygame.draw.rect(self.screen, c,
                         (self.BOARD_WIDTH//self.N_LINES_X*x+3+self.BOARD_OFFSET_X,
                          self.BOARD_HEIGHT//self.N_LINES_Y*y+3+self.BOARD_OFFSET_Y,
                          self.BOARD_WIDTH//self.N_LINES_X-5,
                          self.BOARD_HEIGHT//self.N_LINES_Y-5))

    def draw_score(self):
        text_str_score = self.font.render('SCORE', True, (255, 255, 255))
        self.screen.blit(text_str_score, (self.SCORE_BOARD_X, self.SCORE_BOARD_Y))
        text_score = self.font.render(f'{self.score}', True, (255, 255, 255))
        self.screen.blit(text_score, (self.SCORE_BOARD_X+120, self.SCORE_BOARD_Y))

    def hit(self):
        # ブロック衝突判定
        hit = []
        for y in range(self.current_block.get_size()[0]):
            for x in range(self.current_block.get_size()[1]):
                if self.current_block.get()[y][x] == 1:
                    if self.current_block.position_x+x == 0:
                        hit.append('left')
                    elif self.record[self.current_block.position_y+y][self.current_block.position_x+x-1] != (0, 0, 0):
                        hit.append('left')
                    if self.current_block.position_x+x == self.N_LINES_X-1:
                        hit.append('right')
                    elif self.record[self.current_block.position_y+y][self.current_block.position_x+x+1] != (0, 0, 0):
                        hit.append('right')
                    if self.current_block.position_y+y == self.N_LINES_Y-1:
                        hit.append('bottom')
                    elif self.record[self.current_block.position_y+y+1][self.current_block.position_x+x] != (0, 0, 0):
                        hit.append('bottom')
        return hit

    def can_rotate(self):
        # 現在のブロックが回転可能か確認
        rotated = self.current_block.get_rotated()
        for y in range(rotated.get_size()[0]):
            for x in range(rotated.get_size()[1]):
                if rotated.get()[y][x] == 1:
                    if not 0 <= self.current_block.position_x+x <= self.N_LINES_X-1:
                        return False
                    if not 0 <= self.current_block.position_y+y <= self.N_LINES_Y-1:
                        return False
                    if self.record[self.current_block.position_y+y][self.current_block.position_x+x] != (0, 0, 0):
                        return False
        return True

    def set(self):
        # 操作しているブロックをrecordに追加
        for dy in range(self.current_block.get_size()[0]):
            for dx in range(self.current_block.get_size()[1]):
                if self.current_block.get()[dy][dx] == 1:
                    self.record[self.current_block.position_y + dy][self.current_block.position_x + dx] = \
                        self.current_block.color

    def check_line(self):
        # ラインが揃ってるか確認
        # 揃ってたら一列消す
        n_lines = 0
        for y in range(self.N_LINES_Y):
            if all(e != (0, 0, 0) for e in self.record[y]):
                n_lines += 1
                for c in reversed(range(y)):
                    self.record[c+1] = self.record[c][:]
        return n_lines

    def check_gameover(self):
        # ゲームオーバーになっているか確認
        if 'bottom' in self.hit():
            if self.current_block.position_y == 0:
                text = self.font.render('GAME OVER', True, (255, 255, 255))
                self.screen.blit(text, (70, 300))
                pygame.display.update()
                time.sleep(3)
                pygame.quit()
                sys.exit()


class Button:
    def __init__(self, master, posx, posy, x, y, button_color=(255, 255, 255), onmouse_button_color=(255, 255, 255),
                 func=None):
        self.master = master
        self.button_position_x = posx
        self.button_position_y = posy
        self.button_width = x
        self.button_height = y
        self.button_color = button_color
        self.on_mouse_button_color = onmouse_button_color
        self.rel_func = func
        self.text = ''
        self.text_font = None

    def main(self):
        pygame.draw.rect(self.master, self.button_color,
                         (self.button_position_x, self.button_position_y, self.button_width, self.button_height))
        pygame.display.update()

    def place(self):
        thread = threading.Thread(target=self.main)
        thread.start()

    def set_text(self, text, font_name=None, size=15):
        self.text = text
        self.text_font = pygame.font.Font(font_name, size)


if __name__ == '__main__':
    game = Game()
    game.main()
