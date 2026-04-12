from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

PEDIDO_FILE = DATA_DIR / "PEDIDO-_1_.xlsx"
ITEM_PEDIDO_FILE = DATA_DIR / "ITEM_PEDIDO-_2_.xlsx"
ITENS_FILE = DATA_DIR / "ITENS-_3_.xlsx"