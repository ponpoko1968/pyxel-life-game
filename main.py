import pyxel
import numpy as np
import random

class App:

    def __init__(self, width=128, height=128):
        self.width = width
        self.height = height
        self.color = {False:0, True:7}
        self.world = np.zeros((width, width), dtype=np.bool)
        self.generation = 0
        self.c = 0
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.world[x, y] = random.random() < 0.6
        #self.world[2, 3] = True
        pyxel.init(self.width, self.height, caption="life-game")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        next_world = self.world.copy()
        for y in range(0, self.height):
            for x in range(0, self.width):
                next_world[x, y] = self.judge_window(self.world, x, y)
        self.world = next_world
        self.generation += 1
        for y in range(0, self.height):
            for x in range(0, self.width):
                pyxel.pset(x, y, self.color[self.world[x, y]])
        pyxel.text(0, self.height-16, "gen: {}".format(self.generation), 14)


    def judge_window(self, world, _x, _y) -> bool:
        def judge(status, neighbor_count) -> bool:
            if status:
                if neighbor_count in [0, 1]:  # 過疎
                    return False
                if neighbor_count in [2, 3]:
                    return True  # 現状維持
                # neighbor_count in range(4, 9): #過密
                return False
            else:
                return neighbor_count == 3



        neighbor_pos = [(_x - 1, _y - 1), (_x, _y - 1), (_x + 1, _y - 1),
                        (_x - 1, _y), (_x + 1, _y),
                        (_x - 1, _y + 1), (_x, _y + 1), (_x + 1, _y + 1),
        ]
        count = 0
        # 上下左右の端のセルは、それぞれ反対側に閉じているとして処理
        for pos in neighbor_pos:
            (x, y) = pos
            if x < 0 :
                x = self.width-1
            elif x >= self.width:
                x = 0

            if y < 0 :
                y = self.height-1
            elif y >= self.height:
                y = 0
            count += 1 if world[x, y] else 0
        return judge(world[_x,_y], count)

App(width=256, height=256)
