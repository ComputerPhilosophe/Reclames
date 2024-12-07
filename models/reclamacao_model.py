from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional



@dataclass
class Reclamacao:
    id: Optional[int] = None  
    usuario_id: Optional[int] = None  
    titulo: Optional[str] = None  
    historia: Optional[str] = None  
    celular: Optional[str] = None  
    arquivos: Optional[List[str]] = None  
    criado_em: Optional[datetime] = None

def __post_init__(self):
        if self.criado_em is None:
            self.criado_em = datetime.now()    