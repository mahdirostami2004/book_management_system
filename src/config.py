
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_CONFIG = {
    'db_path': os.path.join(PROJECT_ROOT, 'database', 'shahr_ketab.db')  
}
