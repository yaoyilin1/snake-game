import random

class Food:
    """食物类，管理食物的生成、类型、位置"""
    
    def __init__(self, width, height, config=None):
        self.width = width
        self.height = height
        self.pos = [0, 0]
        
        # 从配置获取食物类型，如果没有配置则使用默认值
        if config:
            food_config = config.get_food_config()
            self.food_types = food_config.get('types', [])
        else:
            # 默认食物类型配置（保持向后兼容）
            self.food_types = [
                {'name': 'small', 'color': [255,255,255], 'length_increase': 1, 'probability': 0.6},
                {'name': 'medium', 'color': [0,191,255], 'length_increase': 3, 'probability': 0.3},
                {'name': 'large', 'color': [255,69,0], 'length_increase': 5, 'probability': 0.1}
            ]
        
        # 获取消息配置
        if config:
            messages_config = config.get_messages_config()
            self.food_messages = messages_config.get('food_messages', {})
        else:
            self.food_messages = {
                'small': '小点心也不错~',
                'medium': '中号美味，真不错！',
                'large': '哇！吃到大餐啦！'
            }
            
        self.type = self.food_types[0] if self.food_types else {}  # 默认第一种食物
        self.spawn()
        
    def spawn(self, snake_body=None, obstacles=None, star_pos=None):
        """生成新食物"""
        if not self.food_types:
            return
            
        # 按概率选择食物类型
        r = random.random()
        acc = 0
        for food_type in self.food_types:
            acc += food_type.get('probability', 0)
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
        food_name = self.type.get('name', 'small')
        return self.food_messages.get(food_name, '吃到食物了！') 