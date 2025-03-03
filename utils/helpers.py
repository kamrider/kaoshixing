#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
辅助函数模块
"""

import os
import sys
import time
from utils.logger import setup_logger

logger = setup_logger(__name__)

def wait_for_seconds(seconds, message=None):
    """
    等待指定的秒数
    
    Args:
        seconds (int): 等待的秒数
        message (str, optional): 等待时显示的消息
    """
    if message:
        logger.info(message)
        
    time.sleep(seconds)
    
def is_valid_url(url):
    """
    简单检查URL是否有效
    
    Args:
        url (str): 要检查的URL
        
    Returns:
        bool: URL是否有效
    """
    if not url:
        return False
        
    # 简单检查URL格式
    return url.startswith(("http://", "https://"))
    
def get_script_dir():
    """
    获取脚本所在目录
    
    Returns:
        str: 脚本所在目录的绝对路径
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
def ensure_dir_exists(directory):
    """
    确保目录存在，如果不存在则创建
    
    Args:
        directory (str): 目录路径
        
    Returns:
        bool: 是否成功创建或已存在
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"创建目录: {directory}")
        return True
    except Exception as e:
        logger.error(f"创建目录失败: {str(e)}")
        return False 