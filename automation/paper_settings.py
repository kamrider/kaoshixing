#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
试卷设置自动化模块
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import setup_logger

logger = setup_logger(__name__)

def configure_paper_settings(driver):
    """
    配置试卷设置
    
    Args:
        driver: ChromeDriver实例
        
    Returns:
        bool: 操作是否成功
    """
    try:
        # 等待页面加载完成
        logger.info("等待页面加载...")
        driver._random_sleep(2, 3)

        # 1. 点击设置按钮
        logger.info("点击设置按钮...")
        settings_btn = WebDriverWait(driver.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#paper-id > form > section > div > header > div.right.bottom > div.right-setting > span:nth-child(2)"))
        )
        driver.click_element(settings_btn)

        # 2. 点击第五个复选框
        logger.info("点击复选框...")
        checkbox = WebDriverWait(driver.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#paper-id > div:nth-child(11) > div > div > div.el-dialog__body > div.setting-item.paper-feature > div.setting-content > div:nth-child(3) > label > span.el-checkbox__input > span"))
        )
        driver.click_element(checkbox)

        # 3. 点击确认按钮
        logger.info("点击确认按钮...")
        confirm_btn = WebDriverWait(driver.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#paper-id > div:nth-child(11) > div > div > div.el-dialog__footer > div > button.el-button.el-button--primary.el-button--default.confirm-button"))
        )
        driver.click_element(confirm_btn)

        logger.info("试卷设置配置完成")
        return True
    except Exception as e:
        logger.error(f"配置试卷设置时发生错误: {str(e)}")
        return False 