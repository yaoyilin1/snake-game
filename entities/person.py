import random

class Person:
    """小人类，管理单个小人的位置和移动"""
    
    def __init__(self, pos, direction):
        self.pos = list(pos)
        self.dir = list(direction)
        
    def move(self, obstacles, width, height):
        """移动小人"""
        new_x = self.pos[0] + self.dir[0]
        new_y = self.pos[1] + self.dir[1]
        
        # 检查边界和障碍物
        if (new_x < 0 or new_x > width-10 or new_y < 0 or new_y > height-10 or 
            [new_x, new_y] in obstacles):
            # 随机换方向
            self.dir = random.choice([(10,0),(-10,0),(0,10),(0,-10)])
        else:
            self.pos[0] = new_x
            self.pos[1] = new_y

class PersonManager:
    """小人管理器，管理所有小人"""
    
    def __init__(self, width, height, person_num=3):
        self.width = width
        self.height = height
        self.person_num = person_num
        self.persons = []
        self.move_interval = 10  # 移动间隔
        self.move_counter = 0
        self.init_persons()
        
    def init_persons(self):
        """初始化小人"""
        self.persons = []
        tries = 0
        while len(self.persons) < self.person_num and tries < 1000:
            tries += 1
            pos = [random.randrange(1, (self.width//10)) * 10, 
                   random.randrange(1, (self.height//10)) * 10]
            if pos not in [p.pos for p in self.persons]:
                direction = random.choice([(10,0),(-10,0),(0,10),(0,-10)])
                self.persons.append(Person(pos, direction))
                
    def update(self, obstacles):
        """更新所有小人位置"""
        self.move_counter += 1
        if self.move_counter >= self.move_interval:
            for person in self.persons:
                person.move(obstacles, self.width, self.height)
            self.move_counter = 0
            
    def check_collision(self, pos):
        """检查是否与指定位置碰撞"""
        return any(person.pos[0] == pos[0] and person.pos[1] == pos[1] 
                  for person in self.persons) 