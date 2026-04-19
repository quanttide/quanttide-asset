# config.py - 飞书知识库下载配置

import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.getenv("BASE_DIR", "./data/feishu_wiki")
SPACES_DIR = f"{BASE_DIR}/spaces"
PAGE_SIZE = int(os.getenv("PAGE_SIZE", "50"))
REQUEST_DELAY = float(os.getenv("REQUEST_DELAY", "0.2"))
