#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
试题管理自动化模块
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from utils.logger import setup_logger

logger = setup_logger(__name__)

class QuestionType:
    """题型枚举"""
    SINGLE_CHOICE = "单选题"
    MULTIPLE_CHOICE = "多选题"
    JUDGMENT = "判断题"
    FILL_BLANK = "填空题"
    QUESTION_ANSWER = "问答题"
    GROUP = "组合题"
    RECORD = "录音题"

def add_question(driver, question_type):
    """
    添加指定类型的题目
    
    Args:
        driver: ChromeDriver实例
        question_type: 题目类型，使用QuestionType类中的常量
        
    Returns:
        bool: 操作是否成功
    """
    try:
        # 等待页面加载
        logger.info(f"准备添加{question_type}...")
        driver._random_sleep(1, 2)

        # 定位添加题目按钮（使用更可靠的选择器）
        add_btn = WebDriverWait(driver.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".suject-opreate .el-dropdown-link"))
            # 这里使用类选择器而不是完整路径，更可靠
        )

        # 移动到添加按钮并点击以显示下拉菜单
        logger.info("点击添加题目按钮...")
        actions = ActionChains(driver.driver)
        actions.move_to_element(add_btn).click().perform()
        driver._random_sleep(0.5, 1)

        # 等待下拉菜单出现并选择指定题型
        # 使用XPath选择器通过文本内容定位具体题型
        question_type_element = WebDriverWait(driver.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[contains(@class, 'el-dropdown-menu__item') and contains(text(), '{question_type}')]"))
        )
        
        logger.info(f"选择题型: {question_type}")
        question_type_element.click()
        driver._random_sleep(1, 2)

        logger.info(f"{question_type}添加成功")
        return True
        
    except Exception as e:
        logger.error(f"添加{question_type}时发生错误: {str(e)}")
        return False

def add_section(driver, section_name=""):
    """
    添加大题
    
    Args:
        driver: ChromeDriver实例
        section_name: 大题名称（可选）
        
    Returns:
        bool: 操作是否成功
    """
    try:
        # 定位添加大题按钮
        logger.info("准备添加大题...")
        add_section_btn = WebDriverWait(driver.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-big-question"))  # 这里需要根据实际类名调整
        )
        
        driver.click_element(add_section_btn)
        
        # 如果提供了大题名称，则设置名称
        if section_name:
            # 等待名称输入框出现并输入
            name_input = WebDriverWait(driver.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".section-name-input"))  # 这里需要根据实际类名调整
            )
            driver.input_text(name_input, section_name)
        
        logger.info(f"大题添加成功{': ' + section_name if section_name else ''}")
        return True
        
    except Exception as e:
        logger.error(f"添加大题时发生错误: {str(e)}")
        return False 