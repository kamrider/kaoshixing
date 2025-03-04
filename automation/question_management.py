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
from selenium.webdriver.common.keys import Keys

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
        logger.info(f"准备添加{question_type}...")
        driver._random_sleep(1, 2)

        # 1. 首先定位并点击触发按钮
        trigger_button = WebDriverWait(driver.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".suject-opreate .el-dropdown-link"))
        )
        
        # 使用 JavaScript 点击按钮
        driver.driver.execute_script("""
            function clickButton(button) {
                // 确保元素在视图中
                button.scrollIntoView({ behavior: 'smooth', block: 'center' });
                
                // 模拟鼠标移入
                button.dispatchEvent(new MouseEvent('mouseenter', {
                    bubbles: true,
                    cancelable: true,
                    view: window
                }));
                
                // 短暂延迟后点击
                setTimeout(() => {
                    button.click();
                }, 100);
            }
            arguments[0].click();
        """, trigger_button)
        
        driver._random_sleep(2, 3)  # 等待下拉菜单出现

        # 2. 等待下拉菜单出现并获取所有选项
        menu_items = WebDriverWait(driver.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".el-dropdown-menu__item"))
        )

        # 3. 根据题型找到对应的选项
        item_positions = {
            "单选题": 0,
            "多选题": 1,
            "判断题": 2,
            "填空题": 3,
            "问答题": 4,
            "组合题": 5,
            "录音题": 6
        }

        position = item_positions.get(question_type)
        if position is None:
            raise Exception(f"未知的题型: {question_type}")

        if position >= len(menu_items):
            raise Exception(f"菜单项索引越界: {position}, 总数: {len(menu_items)}")

        target_item = menu_items[position]

        # 4. 使用 JavaScript 点击目标选项
        driver.driver.execute_script("""
            function clickMenuItem(item) {
                // 确保元素在视图中
                item.scrollIntoView({ behavior: 'smooth', block: 'center' });
                
                // 模拟鼠标移入
                item.dispatchEvent(new MouseEvent('mouseenter', {
                    bubbles: true,
                    cancelable: true,
                    view: window
                }));
                
                // 短暂延迟后点击
                setTimeout(() => {
                    item.click();
                }, 100);
            }
            arguments[0].click();
        """, target_item)

        driver._random_sleep(1, 2)
        logger.info(f"{question_type}添加成功")
        return True

    except Exception as e:
        logger.error(f"添加题目时发生错误: {str(e)}")
        import traceback
        logger.error(f"详细错误信息: {traceback.format_exc()}")
        
        # 如果失败，尝试使用键盘操作
        try:
            logger.info("尝试使用键盘操作...")
            actions = ActionChains(driver.driver)
            # 先点击触发按钮
            trigger_button = driver.driver.find_element(By.CSS_SELECTOR, ".suject-opreate .el-dropdown-link")
            actions.move_to_element(trigger_button).click().perform()
            driver._random_sleep(1, 2)
            
            # 使用方向键选择选项
            for _ in range(item_positions.get(question_type, 0)):
                actions.send_keys(Keys.ARROW_DOWN).perform()
                driver._random_sleep(0.5, 1)
            
            # 按回车确认
            actions.send_keys(Keys.ENTER).perform()
            driver._random_sleep(1, 2)
            
            logger.info(f"{question_type}添加成功（通过键盘操作）")
            return True
            
        except Exception as e:
            logger.error(f"键盘操作也失败了: {str(e)}")
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
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#wrap-affix-container > div > div > div.big-questions-aside > div.big-questions-footer > button > span"))
        )
        
        driver.click_element(add_section_btn)
        driver._random_sleep(1, 2)  # 添加等待时间，确保UI响应
        
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