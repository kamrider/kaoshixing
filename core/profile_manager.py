#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Chrome配置文件管理模块，负责获取和管理Chrome用户配置文件
"""

import os
import platform
import re
from pathlib import Path
from utils.logger import setup_logger

logger = setup_logger(__name__)

class ProfileManager:
    """Chrome用户配置文件管理类"""
    
    def __init__(self):
        """初始化配置文件管理器"""
        self.chrome_user_data_dir = self._get_chrome_user_data_dir()
        logger.info(f"Chrome用户数据目录: {self.chrome_user_data_dir}")
        
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
            
    def get_available_profiles(self):
        """
        获取可用的Chrome用户配置文件列表
        
        Returns:
            list: 配置文件名称列表
        """
        if not self.chrome_user_data_dir or not os.path.exists(self.chrome_user_data_dir):
            logger.error(f"Chrome用户数据目录不存在: {self.chrome_user_data_dir}")
            return []
            
        profiles = []
        
        # 默认配置文件
        default_profile_path = os.path.join(self.chrome_user_data_dir, "Default")
        if os.path.exists(default_profile_path) and os.path.isdir(default_profile_path):
            profiles.append("Default")
            
        # 其他配置文件（Profile 1, Profile 2, ...）
        profile_pattern = re.compile(r"Profile \d+")
        for item in os.listdir(self.chrome_user_data_dir):
            item_path = os.path.join(self.chrome_user_data_dir, item)
            if os.path.isdir(item_path) and profile_pattern.match(item):
                profiles.append(item)
                
        logger.info(f"找到 {len(profiles)} 个Chrome用户配置文件")
        return profiles
        
    def get_profile_path(self, profile_name):
        """
        获取指定配置文件的完整路径
        
        Args:
            profile_name (str): 配置文件名称
            
        Returns:
            str: 配置文件完整路径
        """
        if not self.chrome_user_data_dir:
            return None
            
        # 检查配置文件是否存在
        profile_path = os.path.join(self.chrome_user_data_dir, profile_name)
        if not os.path.exists(profile_path) or not os.path.isdir(profile_path):
            logger.error(f"配置文件不存在: {profile_path}")
            return None
            
        # 返回用户数据目录，profile_name将在ChromeDriver中通过--profile-directory参数指定
        return profile_name
        
    def get_profile_name_from_path(self, profile_path):
        """
        从路径中提取配置文件名称
        
        Args:
            profile_path (str): 配置文件路径
            
        Returns:
            str: 配置文件名称
        """
        if not profile_path:
            return None
            
        path = Path(profile_path)
        return path.name 