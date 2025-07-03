class Snake:
    """贪吃蛇类，管理蛇的身体、移动、增长等"""
    
    def __init__(self, init_pos=[100, 50]):
        self.pos = list(init_pos)  # 蛇头位置
        self.body = [[100, 50], [90, 50], [80, 50]]  # 蛇身坐标列表
        self.direction = 'RIGHT'  # 当前移动方向
        self.change_to = 'RIGHT'  # 待改变的方向
        
    def reset(self):
        """重置蛇到初始状态"""
        self.pos = [100, 50]
        self.body = [[100, 50], [90, 50], [80, 50]]
        self.direction = 'RIGHT'
        self.change_to = 'RIGHT'
        
    def update_direction(self, new_direction):
        """更新移动方向，防止反向移动"""
        if new_direction == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        elif new_direction == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        elif new_direction == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        elif new_direction == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'
            
    def move(self):
        """移动蛇头"""
        if self.direction == 'UP':
            self.pos[1] -= 10
        elif self.direction == 'DOWN':
            self.pos[1] += 10
        elif self.direction == 'LEFT':
            self.pos[0] -= 10
        elif self.direction == 'RIGHT':
            self.pos[0] += 10
            
    def grow(self, length_increase):
        """增长蛇身，在尾部延长"""
        tail = self.body[-1]
        for _ in range(length_increase - 1):
            self.body.append(list(tail))
            
    def update_body(self):
        """更新蛇身，头部跟随蛇头移动"""
        self.body.insert(0, list(self.pos))
        
    def shrink_tail(self):
        """缩短蛇尾"""
        self.body.pop()
        
    def check_self_collision(self):
        """检查是否撞到自己"""
        return any(self.pos[0] == block[0] and self.pos[1] == block[1] for block in self.body[1:])
        
    def check_boundary_collision(self, width, height):
        """检查是否撞到边界"""
        return (self.pos[0] < 0 or self.pos[0] > width-10 or 
                self.pos[1] < 0 or self.pos[1] > height-10)
        
    def check_collision_with_pos(self, pos):
        """检查是否与指定位置碰撞"""
        return self.pos[0] == pos[0] and self.pos[1] == pos[1]
        
    def get_length(self):
        """获取蛇的长度"""
        return len(self.body) 