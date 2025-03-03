#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
全局设置文件，包含默认URL和Chrome相关配置
"""

import os

# 默认URL
DEFAULT_URL = "https://v.kaoshixing.com/admin/paper/#/create?source=toLib"  # 考试星创建试卷页面

# Chrome相关设置
CHROME_BINARY_PATH = None  # Chrome浏览器可执行文件路径，None表示使用默认路径

# 如果需要指定Chrome浏览器路径，取消下面的注释并修改路径
# Windows系统示例
# CHROME_BINARY_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
# macOS系统示例
# CHROME_BINARY_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# Linux系统示例
# CHROME_BINARY_PATH = "/usr/bin/google-chrome"

# WebDriver设置
IMPLICIT_WAIT_TIME = 10  # 隐式等待时间（秒）

# 日志设置
LOG_LEVEL = "INFO"  # 日志级别：DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs", "app.log")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S" 