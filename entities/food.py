import random

class Food:
    """食物类，管理食物的生成、类型、位置"""
    
    # 食物类型配置
    FOOD_TYPES = [
        {'name': 'small', 'color': (255,255,255), 'length': 1, 'prob': 0.6},   # 小食物，白色
        {'name': 'medium', 'color': (0,191,255), 'length': 3, 'prob': 0.3},    # 中食物，深天蓝
        {'name': 'large', 'color': (255,69,0), 'length': 5, 'prob': 0.1}       # 大食物，橙红色
    ]
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pos = [0, 0]
        self.type = self.FOOD_TYPES[0]  # 默认小食物
        self.spawn()
        
    def spawn(self, snake_body=None, obstacles=None, star_pos=None):
        """生成新食物"""
        # 按概率选择食物类型
        r = random.random()
        acc = 0
        for food_type in self.FOOD_TYPES:
            acc += food_type['prob']
            if r <= acc:
                self.type = food_type
                break
                
        # 生成不与蛇、障碍物、星星重叠的位置
        while True:
            pos = [random.randrange(1, (self.width//10)) * 10, 
                   random.randrange(1, (self.height//10)) * 10]
            if (snake_body is None or pos not in snake_body) and \
               (obstacles is None or pos not in obstacles) and \
               (star_pos is None or pos != star_pos):
                self.pos = pos
                break
                
    def get_message(self):
        """根据食物类型返回提示消息"""
        if self.type['name'] == 'large':
            return '哇！吃到大餐啦！'
        elif self.type['name'] == 'medium':
            return '中号美味，真不错！'
        else:
            return '小点心也不错~' 