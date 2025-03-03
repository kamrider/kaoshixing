#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
自动化脚本：使用指定的Chrome用户配置文件打开特定网站并执行操作
"""

import argparse
import sys
import os
from core.driver import ChromeDriver
from core.profile_manager import ProfileManager
from config.settings import DEFAULT_URL
from utils.logger import setup_logger
from utils.helpers import is_valid_url
from automation.paper_settings import configure_paper_settings

logger = setup_logger(__name__)

# 默认使用的配置文件名称
DEFAULT_PROFILE = "Profile 2"

def main():
    """主程序入口"""
    parser = argparse.ArgumentParser(description='使用指定的Chrome用户配置文件打开网站')
    parser.add_argument('-p', '--profile', type=str, default=DEFAULT_PROFILE, help='Chrome用户配置文件名称')
    parser.add_argument('-u', '--url', type=str, default=DEFAULT_URL, help='要打开的网站URL')
    args = parser.parse_args()
    
    try:
        # 获取Chrome用户配置文件
        profile_manager = ProfileManager()
        
        # 使用指定的配置文件或默认配置文件
        profile_name = args.profile
        
        # 检查指定的配置文件是否存在
        available_profiles = profile_manager.get_available_profiles()
        if profile_name not in available_profiles:
            logger.warning(f"指定的配置文件 '{profile_name}' 不存在")
            
            # 如果默认配置文件也不存在，则让用户选择
            if DEFAULT_PROFILE in available_profiles:
                logger.info(f"使用默认配置文件: {DEFAULT_PROFILE}")
                profile_name = DEFAULT_PROFILE
            else:
                if not available_profiles:
                    logger.error("未找到任何Chrome用户配置文件")
                    sys.exit(1)
                    
                print("可用的Chrome用户配置文件:")
                for i, profile in enumerate(available_profiles, 1):
                    print(f"{i}. {profile}")
                    
                choice = int(input("请选择用户配置文件编号: "))
                if 1 <= choice <= len(available_profiles):
                    profile_name = available_profiles[choice-1]
                else:
                    logger.error("无效的选择")
                    sys.exit(1)
        
        # 获取配置文件路径
        profile_path = profile_manager.get_profile_path(profile_name)
        if not profile_path:
            logger.error(f"找不到名为 '{profile_name}' 的Chrome用户配置文件")
            sys.exit(1)
            
        # 验证URL
        url = args.url
        if not is_valid_url(url):
            logger.warning(f"URL格式可能不正确: {url}")
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                logger.info(f"已将URL更正为: {url}")
            
        # 使用指定的配置文件启动Chrome并打开网站
        logger.info(f"使用配置文件 '{profile_name}' 打开网站: {url}")
        
        # 获取Chrome用户数据目录
        chrome_user_data_dir = profile_manager.chrome_user_data_dir
        
        # 启动Chrome浏览器
        with ChromeDriver(profile_path=profile_name) as driver:
            # 导航到目标网站
            if driver.navigate_to(url):
                # 执行自动化步骤
                if configure_paper_settings(driver):
                    logger.info("自动化任务执行成功")
                else:
                    logger.error("自动化任务执行失败")
            input("按Enter键退出...")
            
    except Exception as e:
        logger.error(f"发生错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()