import random

class ObstacleGroup:
    """障碍物组类，管理所有障碍物"""
    
    def __init__(self, width, height, obstacle_num=50, group_num=5):
        self.width = width
        self.height = height
        self.obstacle_num = obstacle_num
        self.group_num = group_num
        self.group_size = obstacle_num // group_num
        self.obstacles = []
        self.generate()
        
    def generate(self):
        """生成障碍物组"""
        self.obstacles = []
        tries = 0
        while len(self.obstacles) < self.obstacle_num and tries < 1000:
            tries += 1
            start_x = random.randrange(1, (self.width//10)-self.group_size) * 10
            start_y = random.randrange(1, (self.height//10)-self.group_size) * 10
            direction = random.choice(['H', 'V'])
            group = []
            for i in range(self.group_size):
                if direction == 'H':
                    pos = [start_x + i*10, start_y]
                else:
                    pos = [start_x, start_y + i*10]
                if pos in self.obstacles:
                    break
                group.append(pos)
            if len(group) == self.group_size:
                self.obstacles.extend(group)
            if len(self.obstacles) >= self.obstacle_num:
                break 