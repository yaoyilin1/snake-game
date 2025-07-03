# -*- coding: utf-8 -*-
"""
游戏实体包
包含游戏中的所有实体对象
"""

from .food import Food
from .star import Star
from .person import Person, PersonManager
from .obstacles import ObstacleGroup

__all__ = ['Food', 'Star', 'Person', 'PersonManager', 'ObstacleGroup'] 