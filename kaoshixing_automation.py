from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
import time
import logging
import sys
import os
import requests
import zipfile
import io
from selenium.webdriver.common.action_chains import ActionChains

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("kaoshixing_automation.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class KaoshixingAutomation:
    def __init__(self):
        """初始化自动化类"""
        self.driver = None
        
    def download_chromedriver(self):
        """手动下载与Chrome版本匹配的ChromeDriver"""
        try:
            # 为Chrome 133版本下载对应的ChromeDriver
            driver_version = "133.0.6943.141"  # 与您的Chrome版本匹配
            download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{driver_version}/win64/chromedriver-win64.zip"
            
            logger.info(f"正在下载ChromeDriver {driver_version}...")
            response = requests.get(download_url)
            
            if response.status_code != 200:
                logger.error(f"下载ChromeDriver失败，状态码: {response.status_code}")
                return None
                
            # 创建驱动程序目录
            driver_dir = os.path.join(os.path.expanduser("~"), ".wdm", "drivers", "chromedriver", "win64", driver_version)
            os.makedirs(driver_dir, exist_ok=True)
            
            # 解压驱动程序
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
                for file in zip_file.namelist():
                    if file.endswith("chromedriver.exe"):
                        with open(os.path.join(driver_dir, "chromedriver.exe"), "wb") as f:
                            f.write(zip_file.read(file))
            
            logger.info(f"ChromeDriver {driver_version} 下载并解压成功")
            return os.path.join(driver_dir, "chromedriver.exe")
            
        except Exception as e:
            logger.error(f"下载ChromeDriver时出错: {e}")
            return None
        
    def setup(self):
        """设置浏览器驱动，使用Chrome浏览器的特定用户配置文件，并模拟真人行为"""
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")  # 最大化窗口
            
            # 使用现有的Chrome配置文件
            # 获取当前用户的Chrome配置文件路径
            user_profile = os.path.expanduser('~')
            chrome_profile_path = os.path.join(user_profile, 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
            
            if os.path.exists(chrome_profile_path):
                logger.info(f"找到Chrome配置文件路径: {chrome_profile_path}")
                options.add_argument(f"user-data-dir={chrome_profile_path}")
                
                # 使用"Profile 2"配置文件，根据您提供的信息
                options.add_argument("profile-directory=Profile 2")
                logger.info("使用配置文件: Profile 2")
            else:
                logger.warning(f"未找到Chrome配置文件路径: {chrome_profile_path}")
            
            # 添加模拟真人行为的设置
            
            # 1. 禁用自动化控制特征
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            
            # 2. 添加模拟真人行为的UA
            options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36")
            
            # 3. 禁用webdriver属性，防止被检测为自动化工具
            options.add_argument("--disable-blink-features=AutomationControlled")
            
            # 4. 添加一些随机性，模拟真人行为
            options.add_argument("--disable-infobars")
            
            # 5. 禁用扩展和GPU加速，提高稳定性
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-gpu")
            
            # 手动下载ChromeDriver
            driver_path = self.download_chromedriver()
            
            if driver_path and os.path.exists(driver_path):
                logger.info(f"使用下载的ChromeDriver: {driver_path}")
                service = Service(driver_path)
                self.driver = webdriver.Chrome(service=service, options=options)
            else:
                # 尝试使用系统中的ChromeDriver
                logger.info("尝试使用系统中的ChromeDriver")
                self.driver = webdriver.Chrome(options=options)
            
            # 进一步修改webdriver属性，防止被检测
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    
                    // 覆盖Selenium特有的属性
                    Object.defineProperty(navigator, 'plugins', {
                        get: function() {
                            // 模拟常见插件
                            return [1, 2, 3, 4, 5];
                        }
                    });
                    
                    // 覆盖语言设置
                    Object.defineProperty(navigator, 'languages', {
                        get: function() {
                            return ['zh-CN', 'zh', 'en-US', 'en'];
                        }
                    });
                    
                    // 覆盖硬件并发性
                    Object.defineProperty(navigator, 'hardwareConcurrency', {
                        get: function() {
                            return 8;
                        }
                    });
                    
                    // 覆盖用户代理
                    window.navigator.chrome = {
                        runtime: {}
                    };
                """
            })
            
            logger.info("Chrome浏览器驱动初始化成功，已设置模拟真人行为")
        except Exception as e:
            logger.error(f"Chrome浏览器驱动初始化失败: {e}")
            raise
    
    def navigate_to_paper_create(self, url="https://v.kaoshixing.com/admin/paper/#/create?source=toLib"):
        """导航到试卷创建页面并点击特定元素"""
        try:
            self.driver.get(url)
            logger.info(f"打开试卷创建页面: {url}")
            
            # 等待页面完全加载
            logger.info("等待页面完全加载 (5秒)...")
            time.sleep(5)
            
            # 点击设置按钮 - 只使用一种方法
            logger.info("尝试点击设置按钮...")
            setting_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#paper-id > form > section > div > header > div.right.bottom > div.right-setting > span:nth-child(2)"))
            )
            setting_button.click()
            logger.info("成功点击设置按钮")
            
            # 等待设置对话框出现
            time.sleep(2)
            
            # 检查复选框当前状态
            checkbox = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#paper-id > div:nth-child(11) > div > div > div.el-dialog__body > div.setting-item.paper-feature > div.setting-content > div:nth-child(3) > label > span.el-checkbox__input > span"))
            )
            
            # 获取复选框的父元素（label）
            checkbox_label = checkbox.find_element(By.XPATH, "./../../..")
            
            # 检查复选框是否已经被选中
            is_checked = "is-checked" in checkbox_label.get_attribute("class")
            logger.info(f"复选框当前状态: {'已选中' if is_checked else '未选中'}")
            
            # 如果未选中，则点击选中
            if not is_checked:
                checkbox_label.click()
                logger.info("点击复选框使其选中")
                time.sleep(1)
                
                # 再次检查状态确认是否选中
                is_checked_after = "is-checked" in checkbox_label.get_attribute("class")
                logger.info(f"点击后复选框状态: {'已选中' if is_checked_after else '未选中'}")
            
            # 使用您提供的精确选择器点击确认按钮
            confirm_button_selector = "#paper-id > div:nth-child(11) > div > div > div.el-dialog__footer > div > button.el-button.el-button--primary.el-button--default.confirm-button"
            confirm_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, confirm_button_selector))
            )
            confirm_button.click()
            logger.info("点击确认按钮")
            
            time.sleep(2)
            logger.info("设置操作完成")
            
        except Exception as e:
            logger.error(f"在试卷创建页面点击元素时出错: {e}")
    
    def fill_paper_basic_info(self, title="自动创建的试卷", category="默认分类", description="这是一个通过自动化脚本创建的试卷"):
        """填写试卷基本信息"""
        try:
            # 填写试卷标题
            title_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='请输入试卷标题']"))
            )
            title_input.clear()
            title_input.send_keys(title)
            logger.info(f"填写试卷标题: {title}")
            
            # 选择试卷分类（如果有）
            try:
                category_select = self.driver.find_element(By.CSS_SELECTOR, ".el-select__input, .el-select")
                category_select.click()
                time.sleep(1)
                
                # 选择分类选项
                category_options = self.driver.find_elements(By.CSS_SELECTOR, ".el-select-dropdown__item")
                for option in category_options:
                    if category in option.text:
                        option.click()
                        logger.info(f"选择试卷分类: {category}")
                        break
            except:
                logger.warning("未找到试卷分类选择框或无需选择分类")
            
            # 填写试卷描述（如果有）
            try:
                description_textarea = self.driver.find_element(By.CSS_SELECTOR, "textarea[placeholder='请输入试卷描述']")
                description_textarea.clear()
                description_textarea.send_keys(description)
                logger.info(f"填写试卷描述: {description}")
            except:
                logger.warning("未找到试卷描述输入框")
            
            logger.info("试卷基本信息填写完成")
            
        except Exception as e:
            logger.error(f"填写试卷基本信息失败: {e}")
    
    def create_topics(self, count):
        """创建指定数量的大题"""
        try:
            # 获取当前已有的大题数量
            existing_topics = self.driver.find_elements(By.CSS_SELECTOR, ".subjec-card, .topic-card")
            logger.info(f"当前已有 {len(existing_topics)} 个大题")
            
            # 计算需要创建的新大题数量
            new_topics_to_create = max(0, count - len(existing_topics))
            logger.info(f"需要创建 {new_topics_to_create} 个新大题")
            
            if new_topics_to_create > 0:
                # 查找新增大题按钮
                add_topic_btn = None
                
                # 尝试多种方法查找添加大题按钮
                selectors = [
                    "button.el-button--primary.is-circle",
                    "button.el-button--primary i.el-icon-plus",
                    ".add-topic-btn",
                    "button.add-btn"
                ]
                
                for selector in selectors:
                    try:
                        add_topic_btn = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                        logger.info(f"使用选择器 '{selector}' 找到添加大题按钮")
                        break
                    except:
                        logger.info(f"选择器 '{selector}' 未找到元素")
                
                if not add_topic_btn:
                    # 尝试使用JavaScript查找按钮
                    add_topic_btn = self.driver.execute_script("""
                        // 尝试查找添加大题按钮
                        var btn = document.querySelector("button.el-button--primary.is-circle") || 
                                 document.querySelector("button.add-topic-btn") ||
                                 document.querySelector("button.add-btn");
                        
                        if (!btn) {
                            // 查找所有带加号图标的按钮
                            var buttons = document.querySelectorAll("button");
                            for (var i = 0; i < buttons.length; i++) {
                                if (buttons[i].innerHTML.includes("el-icon-plus") || 
                                    buttons[i].innerHTML.includes("+") ||
                                    buttons[i].classList.contains("is-circle")) {
                                    btn = buttons[i];
                                    break;
                                }
                            }
                        }
                        
                        return btn;
                    """)
                
                if not add_topic_btn:
                    logger.error("无法找到添加大题按钮")
                    return existing_topics
                
                # 创建新大题
                for i in range(new_topics_to_create):
                    try:
                        # 滚动到按钮位置
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", add_topic_btn)
                        time.sleep(0.5)
                        
                        # 点击添加大题按钮
                        add_topic_btn.click()
                        logger.info(f"点击添加大题按钮 ({i+1}/{new_topics_to_create})")
                        
                        # 等待新大题创建完成
                        time.sleep(2)
                    except Exception as e:
                        logger.error(f"创建第 {i+1} 个新大题失败: {e}")
            
            # 获取所有大题
            all_topics = self.driver.find_elements(By.CSS_SELECTOR, ".subjec-card, .topic-card")
            logger.info(f"当前共有 {len(all_topics)} 个大题")
            
            return all_topics[:count]  # 返回指定数量的大题
            
        except Exception as e:
            logger.error(f"创建大题失败: {e}")
            return []
    
    def add_question_to_topic(self, topic_index, question_type="问答题"):
        """为指定大题添加题目"""
        try:
            # 获取所有大题
            topics = self.driver.find_elements(By.CSS_SELECTOR, ".subjec-card, .topic-card")
            
            if topic_index >= len(topics):
                logger.error(f"大题索引 {topic_index+1} 超出范围，当前只有 {len(topics)} 个大题")
                return False
            
            topic = topics[topic_index]
            
            # 确保大题可见
            self.driver.execute_script("arguments[0].scrollIntoView(true);", topic)
            time.sleep(1)
            
            # 点击大题，确保它被激活
            topic.click()
            time.sleep(1)
            
            # 查找添加题目按钮 - 使用提供的选择器
            try:
                # 尝试使用提供的选择器
                dropdown_selectors = [
                    "#subject > div > div > div > div.content-suject-card > div.suject-opreate > div:nth-child(1) > div > div",
                    "//*[@id=\"subject\"]/div/div/div/div[2]/div[2]/div[1]/div/div",
                    "//div[@class='suject-opreate']/div[1]/div/div"
                ]
                
                dropdown_element = None
                for selector in dropdown_selectors:
                    try:
                        if selector.startswith("//"):
                            dropdown_element = WebDriverWait(self.driver, 5).until(
                                EC.element_to_be_clickable((By.XPATH, selector))
                            )
                        else:
                            dropdown_element = WebDriverWait(self.driver, 5).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                            )
                        logger.info(f"使用选择器 '{selector}' 找到下拉菜单")
                        break
                    except:
                        logger.info(f"选择器 '{selector}' 未找到元素")
                
                if dropdown_element:
                    # 悬停在下拉菜单上
                    actions = ActionChains(self.driver)
                    actions.move_to_element(dropdown_element).perform()
                    logger.info("悬停在下拉菜单上")
                    time.sleep(1)
                    
                    # 点击下拉菜单
                    dropdown_element.click()
                    logger.info("点击下拉菜单")
                    time.sleep(1)
                    
                    # 查找并点击"简答题"选项
                    menu_items = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".el-dropdown-menu__item, .dropdown-item, li"))
                    )
                    
                    for item in menu_items:
                        if "简答题" in item.text:
                            item.click()
                            logger.info("选择题型: 简答题")
                            question_type = "简答题"  # 更新题型
                            time.sleep(2)
                            break
                else:
                    # 如果找不到特定的下拉菜单，回退到原来的方法
                    logger.warning("未找到指定的下拉菜单，尝试使用备用方法")
                    
                    # 查找添加题目按钮
                    add_question_btn = None
                    
                    # 尝试多种方法查找添加题目按钮
                    try:
                        # 方法1: 直接在大题内查找
                        add_question_btn = topic.find_element(By.CSS_SELECTOR, "button:not(.is-disabled), .add-question-btn, .add-btn")
                    except:
                        # 方法2: 使用JavaScript查找
                        add_question_btn = self.driver.execute_script("""
                            var topic = arguments[0];
                            return topic.querySelector('button:not(.is-disabled)') || 
                                topic.querySelector('.add-question-btn') || 
                                topic.querySelector('.add-btn');
                        """, topic)
                    
                    if not add_question_btn:
                        logger.error(f"在第 {topic_index+1} 个大题中找不到添加题目按钮")
                        return False
                    
                    # 点击添加题目按钮
                    add_question_btn.click()
                    logger.info(f"点击第 {topic_index+1} 个大题的添加题目按钮")
                    time.sleep(1)
                    
                    # 选择题型
                    question_type_found = False
                    
                    # 方法1: 查找下拉菜单项
                    try:
                        menu_items = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".el-dropdown-menu__item, .dropdown-item"))
                        )
                        
                        for item in menu_items:
                            if question_type in item.text:
                                item.click()
                                question_type_found = True
                                logger.info(f"选择题型: {question_type}")
                                break
                    except:
                        logger.warning("未找到下拉菜单项，尝试其他方法")
                    
                    # 方法2: 如果没有找到下拉菜单，尝试查找题型选择对话框
                    if not question_type_found:
                        try:
                            type_btns = self.driver.find_elements(By.CSS_SELECTOR, ".question-type-item, .type-item")
                            for btn in type_btns:
                                if question_type in btn.text:
                                    btn.click()
                                    question_type_found = True
                                    logger.info(f"在对话框中选择题型: {question_type}")
                                    
                                    # 点击确认按钮
                                    confirm_btns = self.driver.find_elements(By.CSS_SELECTOR, "button.el-button--primary:not(.is-disabled)")
                                    for confirm_btn in confirm_btns:
                                        if "确定" in confirm_btn.text or "确认" in confirm_btn.text:
                                            confirm_btn.click()
                                            logger.info("点击确认按钮")
                                            break
                                    break
                        except:
                            logger.warning("未找到题型选择对话框")
                    
                    if not question_type_found:
                        logger.error(f"无法选择题型: {question_type}")
                        return False
            except Exception as e:
                logger.error(f"选择题型时出错: {e}")
                return False
            
            # 等待题目编辑器加载
            time.sleep(3)
            
            # 填写题目内容
            try:
                # 查找题干编辑区域
                stem_editor = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".ql-editor, .question-stem-editor, [contenteditable='true']"))
                )
                stem_editor.clear()
                stem_editor.send_keys(f"这是第 {topic_index+1} 个大题的{question_type}题干")
                logger.info(f"填写题干: 这是第 {topic_index+1} 个大题的{question_type}题干")
                
                # 如果是问答题或简答题，可能需要填写参考答案
                answer_editors = self.driver.find_elements(By.CSS_SELECTOR, ".answer-editor .ql-editor, .reference-answer [contenteditable='true']")
                if answer_editors:
                    answer_editors[0].clear()
                    answer_editors[0].send_keys(f"这是第 {topic_index+1} 个大题的{question_type}参考答案")
                    logger.info(f"填写参考答案: 这是第 {topic_index+1} 个大题的{question_type}参考答案")
                
                # 点击保存按钮
                save_btns = self.driver.find_elements(By.CSS_SELECTOR, "button.el-button--primary:not(.is-disabled)")
                for btn in save_btns:
                    if "保存" in btn.text:
                        btn.click()
                        logger.info("点击保存按钮")
                        break
                
                time.sleep(2)
                logger.info(f"成功为第 {topic_index+1} 个大题添加{question_type}")
                return True
                
            except Exception as e:
                logger.error(f"填写题目内容失败: {e}")
                return False
            
        except Exception as e:
            logger.error(f"为第 {topic_index+1} 个大题添加题目失败: {e}")
            return False
    
    def process_paper_creation(self, topic_count=5, questions_per_topic=2):
        """处理整个试卷创建流程"""
        try:
            # 填写试卷基本信息
            self.fill_paper_basic_info(title=f"自动创建的试卷 {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 创建大题
            topics = self.create_topics(topic_count)
            
            # 为每个大题添加题目
            for i in range(min(len(topics), topic_count)):
                for j in range(questions_per_topic):
                    self.add_question_to_topic(i, question_type="简答题")  # 默认使用简答题
                    time.sleep(2)
            
            # 点击保存试卷按钮
            save_btns = self.driver.find_elements(By.CSS_SELECTOR, "button.el-button--primary:not(.is-disabled)")
            for btn in save_btns:
                if "保存" in btn.text or "提交" in btn.text:
                    btn.click()
                    logger.info("点击保存试卷按钮")
                    break
            
            # 等待保存完成
            time.sleep(5)
            
            logger.info("试卷创建完成")
            
        except Exception as e:
            logger.error(f"试卷创建过程中出错: {e}")
    
    def close(self):
        """关闭浏览器驱动"""
        if self.driver:
            self.driver.quit()
            logger.info("浏览器已关闭")

# 主函数
def main():
    # 创建自动化实例
    automation = KaoshixingAutomation()
    
    try:
        # 设置浏览器驱动
        automation.setup()
        
        # 导航到试卷创建页面并点击特定元素
        automation.navigate_to_paper_create()
        
        # 获取用户输入
        topic_count = int(input("请输入需要创建的大题数量: "))
        questions_per_topic = int(input("请输入每个大题的题目数量: "))
        
        # 处理试卷创建
        automation.process_paper_creation(topic_count, questions_per_topic)
        
        input("操作完成，按Enter键退出...")
        
    except Exception as e:
        logger.error(f"程序执行出错: {e}")
    finally:
        # 关闭浏览器
        automation.close()

if __name__ == "__main__":
    main()