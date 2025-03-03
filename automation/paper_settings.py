#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
考试星试卷设置自动化脚本
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.driver import ChromeDriver
from utils.logger import setup_logger

logger = setup_logger(__name__)

def automate_paper_settings():
    """自动化配置试卷设置"""
    try:
        with ChromeDriver(profile_path="Profile 2") as driver:
            # 等待页面加载
            wait = WebDriverWait(driver.driver, 10)
            
            # 1. 点击设置按钮
            logger.info("点击设置按钮")
            settings_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".right-setting-item"))
            )
            driver.click_element(settings_btn)
            
            # 2. 点击复选框
            logger.info("点击复选框")
            checkbox = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".setting-item.paper-feature .el-checkbox__input")
                )
            )
            driver.click_element(checkbox)
            
            # 3. 点击确认按钮
            logger.info("点击确认按钮")
            confirm_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".el-button--primary.confirm-button")
                )
            )
            driver.click_element(confirm_btn)
            
            logger.info("设置完成")
            input("按Enter键退出...")
            
    except Exception as e:
        logger.error(f"自动化过程出错: {str(e)}")
        raise

if __name__ == "__main__":
    automate_paper_settings() 