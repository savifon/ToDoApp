import sys
from pathlib import Path

# Adiciona o diretório raiz ao path do Python
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))