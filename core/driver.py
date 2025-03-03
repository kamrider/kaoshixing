#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WebDriver管理模块，负责Chrome浏览器的启动和控制
"""

import os
import time
import random
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.settings import CHROME_BINARY_PATH, IMPLICIT_WAIT_TIME
from utils.logger import setup_logger

logger = setup_logger(__name__)

class ChromeDriver:
    """Chrome WebDriver管理类"""
    
    def __init__(self, profile_path=None, headless=False):
        """
        初始化Chrome WebDriver
        
        Args:
            profile_path (str): Chrome用户配置文件名称
            headless (bool): 是否以无头模式运行
        """
        self.profile_name = profile_path
        self.headless = headless
        self.driver = None
        self.user_data_dir = self._get_chrome_user_data_dir()
        
    def _get_chrome_user_data_dir(self):
        """
        获取Chrome用户数据目录
        
        Returns:
            str: Chrome用户数据目录路径
        """
        system = platform.system()
        
        if system == "Windows":
            # Windows系统下的Chrome用户数据目录
            user_profile = os.environ.get("USERPROFILE")
            return os.path.join(user_profile, "AppData", "Local", "Google", "Chrome", "User Data")
        elif system == "Darwin":
            # macOS系统下的Chrome用户数据目录
            home = os.environ.get("HOME")
            return os.path.join(home, "Library", "Application Support", "Google", "Chrome")
        elif system == "Linux":
            # Linux系统下的Chrome用户数据目录
            home = os.environ.get("HOME")
            return os.path.join(home, ".config", "google-chrome")
        else:
            logger.error(f"不支持的操作系统: {system}")
            return None
        
    def __enter__(self):
        """上下文管理器入口，启动浏览器"""
        self.start()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出，关闭浏览器"""
        self.quit()
        
    def start(self):
        """启动Chrome浏览器"""
        options = Options()
        
        # 如果指定了用户数据目录和配置文件名称
        if self.user_data_dir and self.profile_name:
            logger.info(f"使用Chrome用户配置文件: {self.profile_name}")
            options.add_argument(f"user-data-dir={self.user_data_dir}")
            options.add_argument(f"--profile-directory={self.profile_name}")
        
        # 设置Chrome二进制文件路径（如果指定）
        if CHROME_BINARY_PATH and os.path.exists(CHROME_BINARY_PATH):
            options.binary_location = CHROME_BINARY_PATH
            
        # 无头模式设置
        if self.headless:
            options.add_argument("--headless=new")
            
        # 其他常用设置
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--start-maximized")
        
        # 添加解决Chrome崩溃的选项
        options.add_argument("--remote-debugging-port=9222")  # 启用远程调试端口
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-sync")
        options.add_argument("--no-first-run")
        options.add_argument("--safebrowsing-disable-auto-update")
        options.add_argument("--password-store=basic")
        
        # 添加反自动化检测的选项
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        # 设置随机的用户代理
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.54",
        ]
        options.add_argument(f"--user-agent={random.choice(user_agents)}")
        
        # 启动Chrome浏览器
        try:
            # 直接使用Chrome驱动
            self.driver = webdriver.Chrome(options=options)
            
            # 修改navigator.webdriver属性，绕过反爬检测
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # 设置隐式等待时间
            self.driver.implicitly_wait(IMPLICIT_WAIT_TIME)
            logger.info("Chrome浏览器启动成功")
            return self.driver
        except Exception as e:
            logger.error(f"启动Chrome浏览器失败: {str(e)}")
            raise
            
    def quit(self):
        """关闭Chrome浏览器"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Chrome浏览器已关闭")
            except Exception as e:
                logger.error(f"关闭Chrome浏览器失败: {str(e)}")
            finally:
                self.driver = None
                
    def navigate_to(self, url):
        """
        导航到指定URL
        
        Args:
            url (str): 要访问的URL
        """
        if not self.driver:
            self.start()
            
        try:
            logger.info(f"正在访问URL: {url}")
            self.driver.get(url)
            
            # 随机等待一段时间，模拟人类行为
            self._random_sleep(1, 3)
            
            # 随机滚动页面，模拟人类行为
            self._random_scroll()
            
            logger.info(f"成功访问URL: {url}")
            return True
        except Exception as e:
            logger.error(f"访问URL失败: {str(e)}")
            return False
            
    def _random_sleep(self, min_seconds=0.5, max_seconds=2.0):
        """
        随机等待一段时间，模拟人类行为
        
        Args:
            min_seconds (float): 最小等待时间（秒）
            max_seconds (float): 最大等待时间（秒）
        """
        sleep_time = random.uniform(min_seconds, max_seconds)
        time.sleep(sleep_time)
        
    def _random_scroll(self, scroll_count=None):
        """
        随机滚动页面，模拟人类行为
        
        Args:
            scroll_count (int, optional): 滚动次数，如果为None则随机1-5次
        """
        if not scroll_count:
            scroll_count = random.randint(1, 5)
            
        for _ in range(scroll_count):
            # 随机滚动距离
            scroll_distance = random.randint(100, 500)
            scroll_direction = random.choice([1, -1])  # 1表示向下滚动，-1表示向上滚动
            
            # 执行滚动
            self.driver.execute_script(f"window.scrollBy(0, {scroll_distance * scroll_direction})")
            
            # 随机等待
            self._random_sleep(0.2, 1.0)
            
    def click_element(self, element, random_delay=True):
        """
        模拟人类点击元素
        
        Args:
            element: 要点击的WebElement元素
            random_delay (bool): 是否在点击前随机等待
        """
        try:
            # 确保元素可见
            WebDriverWait(self.driver, 10).until(EC.visibility_of(element))
            
            # 随机等待
            if random_delay:
                self._random_sleep(0.1, 1.0)
                
            # 移动到元素位置
            ActionChains(self.driver).move_to_element(element).perform()
            
            # 再次随机等待
            if random_delay:
                self._random_sleep(0.1, 0.5)
                
            # 点击元素
            element.click()
            
            # 点击后随机等待
            self._random_sleep(0.5, 2.0)
            
            return True
        except Exception as e:
            logger.error(f"点击元素失败: {str(e)}")
            return False
            
    def input_text(self, element, text, clear_first=True, random_typing=True):
        """
        模拟人类输入文本
        
        Args:
            element: 要输入文本的WebElement元素
            text (str): 要输入的文本
            clear_first (bool): 是否先清空输入框
            random_typing (bool): 是否模拟人类随机输入速度
        """
        try:
            # 确保元素可见
            WebDriverWait(self.driver, 10).until(EC.visibility_of(element))
            
            # 移动到元素位置
            ActionChains(self.driver).move_to_element(element).perform()
            self._random_sleep(0.1, 0.5)
            
            # 点击元素
            element.click()
            self._random_sleep(0.1, 0.5)
            
            # 清空输入框
            if clear_first:
                element.clear()
                self._random_sleep(0.1, 0.5)
                
            # 模拟人类输入
            if random_typing:
                for char in text:
                    element.send_keys(char)
                    # 随机输入速度
                    self._random_sleep(0.05, 0.2)
            else:
                element.send_keys(text)
                
            # 输入完成后随机等待
            self._random_sleep(0.3, 1.0)
            
            return True
        except Exception as e:
            logger.error(f"输入文本失败: {str(e)}")
            return False