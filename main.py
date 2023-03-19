from src.db.base import create_tables
from src.management import bot

if __name__ == "__main__":
    create_tables()
    bot()
