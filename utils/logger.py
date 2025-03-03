#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
日志工具模块，用于记录程序运行日志
"""

import os
import logging
from logging.handlers import RotatingFileHandler

# 尝试导入配置，如果失败则使用默认值
try:
    from config.settings import LOG_LEVEL, LOG_FILE, LOG_FORMAT, LOG_DATE_FORMAT
except ImportError:
    LOG_LEVEL = "INFO"
    LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs", "app.log")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 确保日志目录存在
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def setup_logger(name):
    """
    设置并返回一个命名的日志记录器
    
    Args:
        name (str): 日志记录器名称
        
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    # 创建日志记录器
    logger = logging.getLogger(name)
    
    # 如果已经配置过，直接返回
    if logger.handlers:
        return logger
        
    # 设置日志级别
    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(level)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # 创建文件处理器（滚动日志文件）
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    
    # 创建格式化器
    formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # 添加处理器到日志记录器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger 