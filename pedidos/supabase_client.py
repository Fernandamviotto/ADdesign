from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do .env

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Por favor, configure as variáveis SUPABASE_URL e SUPABASE_KEY no .env")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Exemplo de função para autenticar usuário com email/senha
def sign_in(email: str, password: str):
    response = supabase.auth.sign_in(email=email, password=password)
    if response.user:
        return response.user
    else:
        raise Exception(f"Erro ao autenticar: {response.session}")

# Exemplo para obter dados da tabela 'pedidos'
def get_pedidos():
    data = supabase.table('pedido').select("*").execute()
    if data.error:
        raise Exception(f"Erro ao buscar pedidos: {data.error.message}")
    return data.data
