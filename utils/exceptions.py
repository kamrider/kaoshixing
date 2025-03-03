#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
自定义异常模块
"""

class ChromeProfileError(Exception):
    """Chrome用户配置文件相关错误"""
    pass
    
class BrowserError(Exception):
    """浏览器操作相关错误"""
    pass
    
class ConfigError(Exception):
    """配置相关错误"""
    pass 