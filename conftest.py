import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

# settings.py требует эти env при импорте; load_dotenv(override=False) их не затрёт,
# если в реальном .env заданы свои значения.
os.environ.setdefault("BOT_TOKEN", "123456:TEST")
os.environ.setdefault("ADMIN_IDS", "1")
os.environ.setdefault("TIMEZONE", "Europe/Moscow")
