"""
Project: pygame
Creator: stan Z
Create time: 2021-03-08 19:37
IDE: PyCharm
Introduction:
"""
import pygame
import random

pygame.init()
######################################## 定义变量
MAP_WIDTH = 288  # 地图大小
MAP_HEIGHT = 512
FPS = 30  # 刷新率
PIPE_GAPS = [90, 100, 110, 120, 130, 140]  # 缺口的距离 有这6个随机距离
# PIPE_GAPS1 = []
PIPE_HEIGHT_RANGE = [int(MAP_HEIGHT * 0.3), int(MAP_HEIGHT * 0.7)]  # 管道长度范围
PIPE_DISTANCE = 120  # 管道之间距离

######################################## 加载素材
SPRITE_FILE = './assets/sprites/'
# 列表推导式 获得三种不同的鸟和三种状态
BIRDS = [[f'{SPRITE_FILE}{bird}-{move}.png' for move in ['upflap', 'midflap', 'downflap']] for bird in ['redbird', 'bluebird', 'yellowbird']]
BGPICS = [SPRITE_FILE + 'background-day.png', SPRITE_FILE + 'background-night.png']
PIPES = [SPRITE_FILE + 'pipe-green.png', SPRITE_FILE + 'pipe-red.png']
NUMBERS = [f'{SPRITE_FILE}{n}.png' for n in range(10)]

# 将图片设置成一个大字典 里面通过key-value存不同的场景图
IMAGES = {}
IMAGES['numbers'] = [pygame.image.load(number) for number in NUMBERS]  # 数字素材有10张 因此遍历
IMAGES['guide'] = pygame.image.load(SPRITE_FILE + 'message.png')
IMAGES['gameover'] = pygame.image.load(SPRITE_FILE + 'gameover.png')
IMAGES['floor'] = pygame.image.load(SPRITE_FILE + 'base.png')

# 地板的高是一个很常用的变量 因此我们专门拿出来
FLOOR_H = MAP_HEIGHT - IMAGES['floor'].get_height()  # 屏幕高减去floor图片的高 就是他在屏幕里的位置

SPRITE_SOUND = './assets/audio/'
SOUNDS = {}  # 同理声音素材也这样做
SOUNDS['start'] = pygame.mixer.Sound(SPRITE_SOUND + 'wing.wav')
SOUNDS['die'] = pygame.mixer.Sound(SPRITE_SOUND + 'die.wav')
SOUNDS['hit'] = pygame.mixer.Sound(SPRITE_SOUND + 'hit.wav')
SOUNDS['score'] = pygame.mixer.Sound(SPRITE_SOUND + 'wing.wav')
SOUNDS['flap'] = pygame.mixer.Sound(SPRITE_SOUND + 'wing.wav')
SOUNDS['death'] = pygame.mixer.Sound(SPRITE_SOUND + 'die.wav')
SOUNDS['main'] = pygame.mixer.Sound(SPRITE_SOUND + 'wing.ogg')
SOUNDS['world_clear'] = pygame.mixer.Sound(SPRITE_SOUND + 'wing.wav')


# 执行函数
def main():
    while True:
        IMAGES['bgpic'] = pygame.image.load(random.choice(BGPICS))  # random的choice方法可以随机从列表里返回一个元素 白天或者黑夜
        IMAGES['bird'] = [pygame.image.load(frame) for frame in random.choice(BIRDS)]  # 列表推导式 鸟也是随机
        pipe = pygame.image.load(random.choice(PIPES))
        IMAGES['pipe'] = [pipe, pygame.transform.flip(pipe, False, True)]  # flip是翻转 将管道放下面和上面 Flase水平不动，True上下翻转
        SOUNDS['start'].play()
        # SOUNDS['main'].play()
        menu_window()
        result = game_window()
        end_window(result)


def menu_window():
    SOUNDS['world_clear'].play()
    floor_gap = IMAGES['floor'].get_width() - MAP_WIDTH  # 地板间隙 336 - 288 = 48
    floor_x = 0

    # 标题位置
    guide_x = (MAP_WIDTH - IMAGES['guide'].get_width()) / 2
    guide_y = MAP_HEIGHT * 0.12

    # 小鸟位置
    bird_x = MAP_WIDTH * 0.2
    bird_y = MAP_HEIGHT * 0.5 - IMAGES['bird'][0].get_height() / 2
    bird_y_vel = 1  # 小鸟飞行的速率 按y坐标向下
    max_y_shift = 50  # 小鸟飞行的最大幅度
    y_shift = 0  # 小鸟起始幅度为0

    idx = 0  # 小鸟翅膀煽动频率
    frame_seq = [0] * 5 + [1] * 5 + [2] * 5 + [1] * 5  # 控制小鸟翅膀运动上中下

    while True:
        for event in pygame.event.get():  # 监控行为
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        if floor_x <= -floor_gap:  # 当地板跑到最大间隔的时候
            floor_x = floor_x + floor_gap  # 刷新地板的x轴
        else:
            floor_x -= 4  # 地板 x轴的移动速度

        if abs(y_shift) == max_y_shift:  # 如果y_shift的绝对值 = 最大幅度
            bird_y_vel *= -1  # 调转方向飞 同时飞行速度为1
        else:
            bird_y += bird_y_vel
        y_shift += bird_y_vel  # 小鸟y轴正负交替 上下飞

        # 小鸟翅膀
        idx += 1  # 翅膀煽动频率
        idx %= len(frame_seq)  # 通过取余得到 0 1 2
        frame_index = frame_seq[idx]  # 小鸟图片的下标 就是翅膀的状态

        SCREEN.blit(IMAGES['bgpic'], (0, 0))
        SCREEN.blit(IMAGES['floor'], (floor_x, FLOOR_H))
        SCREEN.blit(IMAGES['guide'], (guide_x, guide_y))
        SCREEN.blit(IMAGES['bird'][frame_index], (bird_x, bird_y))

        pygame.display.update()
        CLOCK.tick(FPS)  # 以每秒30帧刷新屏幕


def game_window():
    SOUNDS['world_clear'].stop()
    SOUNDS['main'].play()
    score = 0

    floor_gap = IMAGES['floor'].get_width() - MAP_WIDTH  # 地板间隙 336 - 288 = 48
    floor_x = 0

    # 小鸟位置
    bird_x = MAP_WIDTH * 0.2
    bird_y = MAP_HEIGHT * 0.5 - IMAGES['bird'][0].get_height() / 2
    bird = Bird(bird_x, bird_y)

    n_pair = round(MAP_WIDTH / PIPE_DISTANCE)  # 四舍五入取整数 屏幕宽度/两个管道之间的距离 这个距离时候刷新第二个管道  2.4
    pipe_group = pygame.sprite.Group()  # 是一个集合

    # 生成前面的管道
    pipe_x = MAP_WIDTH
    pipe_y = random.randint(PIPE_HEIGHT_RANGE[0], PIPE_HEIGHT_RANGE[1])  # 管道长度随机从153.6 到 358.4
    pipe1 = Pipe(pipe_x, pipe_y, upwards=True)  # 创建一个管道对象
    pipe_group.add(pipe1)  # 将对象添加到这个精灵集合里面
    pipe2 = Pipe(pipe_x, pipe_y - random.choice(PIPE_GAPS), upwards=False)  # 翻转的管道
    pipe_group.add(pipe2)

    SOUNDS['flap'].play()

    while True:
        flap = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # 空格拍翅膀
                SOUNDS['flap'].play()
                flap = True

        bird.update(flap)

        if floor_x <= -floor_gap:  # 当地板跑到最大间隔的时候
            floor_x = floor_x + floor_gap  # 刷新地板的x轴
        else:
            floor_x -= 4  # 地板 x轴的移动速度

        # 生成最后一个管道
        if len(pipe_group) / 2 < n_pair:  # 当管道组长度<2.4 时 意思就是两个半管道的时候
            # sprites()将管道组返回成列表
            last_pipe = pipe_group.sprites()[-1]
            pipe_x = last_pipe.rect.right + PIPE_DISTANCE
            pipe_y = random.randint(PIPE_HEIGHT_RANGE[0], PIPE_HEIGHT_RANGE[1])
            pipe1 = Pipe(pipe_x, pipe_y, upwards=True)
            pipe_group.add(pipe1)
            pipe2 = Pipe(pipe_x, pipe_y - random.choice(PIPE_GAPS), upwards=False)
            pipe_group.add(pipe2)

        pipe_group.update()
        # 鸟的矩形y坐标如果大于地板的高度 就死亡
        # pygame.sprite.spritecollideany 碰撞函数 如果bird和pipe_group碰撞了 就死亡
        if bird.rect.y > FLOOR_H or bird.rect.y < 0 or pygame.sprite.spritecollideany(bird, pipe_group):
            SOUNDS['score'].stop()
            SOUNDS['main'].stop()
            SOUNDS['hit'].play()
            SOUNDS['die'].play()
            SOUNDS['death'].play()
            # 保存死亡时的鸟儿 分数 管道 继续显示在结束窗口
            result = {'bird': bird, 'score': score, 'pipe_group': pipe_group}
            return result

        # 当小鸟左边大于 管道右边就得分
        if pipe_group.sprites()[0].rect.left == 0:
            SOUNDS['score'].play()
            score += 1

        SCREEN.blit(IMAGES['bgpic'], (0, 0))
        pipe_group.draw(SCREEN)
        SCREEN.blit(IMAGES['floor'], (floor_x, FLOOR_H))
        SCREEN.blit(bird.image, bird.rect)
        show_score(score)
        pygame.display.update()
        CLOCK.tick(FPS)


def end_window(result):
    # 显示gameover的图片
    gameover_x = MAP_WIDTH * 0.5 - IMAGES['gameover'].get_width() / 2
    gameover_y = MAP_HEIGHT * 0.4
    bird = result['bird']
    pipe_group = result['pipe_group']

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and bird.rect.y > FLOOR_H:
                SOUNDS['death'].stop()
                return

        # 使用类go_die方法 鸟儿撞墙后 旋转往下
        bird.go_die()
        SCREEN.blit(IMAGES['bgpic'], (0, 0))
        pipe_group.draw(SCREEN)
        SCREEN.blit(IMAGES['floor'], (0, FLOOR_H))
        SCREEN.blit(IMAGES['gameover'], (gameover_x, gameover_y))
        show_score(result['score'])
        SCREEN.blit(bird.image, bird.rect)
        pygame.display.update()
        CLOCK.tick(FPS)


# 显示得分
def show_score(score):
    score_str = str(score)
    w = IMAGES['numbers'][0].get_width()
    x = MAP_WIDTH / 2 - 2 * w / 2
    y = MAP_HEIGHT * 0.1
    for number in score_str:  # IMAGES['numbers'] = [pygame.image.load(number) for number in NUMBERS]
        SCREEN.blit(IMAGES['numbers'][int(number)], (x, y))
        x += w


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # super(Bird, self).__init__(x, y)
        pygame.sprite.Sprite.__init__(self)
        self.frames = IMAGES['bird']  # 鸟儿框架
        self.frame_list = [0] * 5 + [1] * 5 + [2] * 5 + [1] * 5  # 控制小鸟翅膀运动上中下
        self.frame_index = 0
        self.image = self.frames[self.frame_list[self.frame_index]]  # 和菜单界面小鸟扇翅膀一个原理
        self.rect = self.image.get_rect()  # 鸟儿的矩形
        self.rect.x = x
        self.rect.y = y
        self.gravity = 1  # 重力
        self.flap_acc = -10  # 翅膀拍打往上飞 y坐标-10
        self.y_vel = -10  # y坐标的速度
        self.max_y_vel = 15  # y轴下落最大速度
        self.rotate = 0  # 脑袋朝向
        self.rotate_vel = -3  # 转向速度
        self.max_rotate = -30  # 最大转向速度
        self.flap_rotate = 45  # 按了空格只会脑袋朝向上30度

    def update(self, flap=False):
        if flap:
            self.y_vel = self.flap_acc  # 拍打翅膀 则y速度-10向上
            self.rotate = self.flap_rotate
        else:
            self.rotate = self.rotate + self.rotate_vel

        self.y_vel = min(self.y_vel + self.gravity, self.max_y_vel)
        self.rect.y += self.y_vel  # 小鸟向上移动的距离
        self.rorate = max(self.rotate + self.rotate_vel, self.max_rotate)

        self.frame_index += 1  # 扇翅膀的速率
        self.frame_index %= len(self.frame_list)  # 0~20
        self.image = self.frames[self.frame_list[self.frame_index]]
        self.image = pygame.transform.rotate(self.image, self.rotate)  # transform变形方法 旋转

    def go_die(self):
        if self.rect.y < FLOOR_H:
            self.y_vel = self.max_y_vel
            self.rect.y += self.y_vel
            self.rotate = -90
            self.image = self.frames[self.frame_list[self.frame_index]]
            self.image = pygame.transform.rotate(self.image, self.rotate)


# 管道类
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, upwards=True):
        pygame.sprite.Sprite.__init__(self)
        self.x_vel = -4  # 管道移动速度
        # 默认属性为真 则是正向管道
        if upwards:
            self.image = IMAGES['pipe'][0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.top = y
        # 利用flip方法 旋转管道成为反向管道
        else:
            self.image = IMAGES['pipe'][1]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.bottom = y

    def update(self):
        self.rect.x += self.x_vel  # 管道x轴加移动速度
        if self.rect.right < 0:
            self.kill()


if __name__ == '__main__':
    main()

