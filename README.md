# Chrome用户配置文件自动化工具

这是一个Python自动化工具，可以使用指定的Chrome用户配置文件打开特定网站。

## 功能特点

- 自动检测系统中的Chrome用户配置文件
- 支持通过命令行参数指定用户配置文件和目标网站
- 如果未指定配置文件，会显示可用的配置文件列表供选择
- 跨平台支持（Windows、macOS、Linux）
- 详细的日志记录

## 安装

1. 确保已安装Python 3.6+
2. 克隆或下载本仓库
3. 安装依赖包：

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

```bash
python main.py
```

这将显示可用的Chrome用户配置文件列表，让你选择一个，然后打开默认网站（百度）。

### 指定用户配置文件

```bash
python main.py -p "Profile 1"
```

这将使用名为"Profile 1"的Chrome用户配置文件打开默认网站。

### 指定目标网站

```bash
python main.py -u "https://www.example.com"
```

这将让你选择一个Chrome用户配置文件，然后打开指定的网站。

### 同时指定用户配置文件和目标网站

```bash
python main.py -p "Profile 1" -u "https://www.example.com"
```

这将使用名为"Profile 1"的Chrome用户配置文件打开指定的网站。

## 配置

你可以在`config/settings.py`文件中修改默认设置：

- `DEFAULT_URL`：默认打开的网站URL
- `CHROME_BINARY_PATH`：Chrome浏览器可执行文件路径（如果需要指定）
- `IMPLICIT_WAIT_TIME`：WebDriver隐式等待时间
- 日志相关设置

## 注意事项

- 确保Chrome浏览器已安装在系统中
- 如果Chrome正在运行，可能会影响自动化操作，建议先关闭所有Chrome窗口
- 首次运行时会自动下载适合你系统的ChromeDriver 