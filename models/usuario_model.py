from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Usuario:
    id: Optional[int] = None
    cpf: Optional[str] = None
    cnpj: Optional[str] = None
    nome: Optional[str] = None
    data_nascimento: Optional[date] = None
    genero: Optional[str] = None
    endereco_cidade: Optional[str] = None
    endereco_bairro: Optional[str] = None
    endereco_cep: Optional[str] = None
    endereco_numero: Optional[str] = None
    endereco_complemento: Optional[str] = None
    endereco_logradouro: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None
    perfil: Optional[int] = None
 
    
    

    
