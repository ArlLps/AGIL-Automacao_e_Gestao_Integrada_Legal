import requests
import json
import difflib
from datetime import datetime, timedelta
import streamlit as st
import pytz
import holidays
import config
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def calculate_deadline():
    """
    Calcula data de bloqueio (deadline) +2 dias úteis.
    Retorna formato ISO 8601 com Offset (ex: -03:00), que é nativo e seguro.
    """
    # Define Fuso Horário de Brasília explicitamente
    try:
        tz = pytz.timezone(config.TIMEZONE)
    except:
        tz = pytz.timezone('America/Sao_Paulo')
    
    now = datetime.now(tz)
    
    # Tenta carregar feriados
    try:
        br_holidays = holidays.Brazil(state=config.ESTADO_FERIADOS)
    except:
        br_holidays = {}

    days_added = 0
    current_date = now
    
    # Lógica de Dias Úteis
    while days_added < 2:
        current_date += timedelta(days=1)
        # Se for dia útil (0-4 segunda-sexta) e não for feriado
        # A comparação (date in holidays) exige objeto date, não datetime
        if current_date.weekday() < 5 and current_date.date() not in br_holidays:
            days_added += 1
            
    # Define horário final do dia e remove microssegundos (CRÍTICO)
    deadline = current_date.replace(hour=23, minute=59, second=59, microsecond=0)
    
    # O método isoformat() gera: '2026-02-06T23:59:59-03:00'
    # Isso atende à regra "especifique o offset" da documentação
    return deadline.isoformat()

def get_signers_emails(names_text, emails_db_path='email.json'):
    try:
        with open(emails_db_path, 'r', encoding='utf-8') as f:
            db_emails = json.load(f)
    except FileNotFoundError:
        return [], ["Erro: Arquivo email.json não encontrado"], []

    raw_names = [n.strip().rstrip('.') for n in names_text.split('\n') if n.strip()]
    signers = []
    missing = []
    display_map = []
    
    known_names = list(db_emails.keys())

    for name in raw_names:
        if name in db_emails:
            email = db_emails[name]
            signers.append({"email": email, "action": "SIGN"})
            display_map.append((name, email, "Exato"))
            continue
            
        matches = difflib.get_close_matches(name, known_names, n=1, cutoff=0.6)
        if matches:
            matched_name = matches[0]
            email = db_emails[matched_name]
            signers.append({"email": email, "action": "SIGN"})
            display_map.append((name, email, f"Aproximado de '{matched_name}'"))
        else:
            missing.append(name)
            display_map.append((name, "❌ NÃO ENCONTRADO", "Erro"))

    return signers, missing, display_map

def send_to_authentique(file_obj, signers, doc_name="ATA de Reunião"):
    """
    Envia para API Authentique (V2) com tratamento de erros de conexão e validação.
    """
    
    url = "https://api.autentique.com.br/v2/graphql"
    
    if "AUTHENTIQUE_TOKEN" not in st.secrets:
        raise Exception("Token da Authentique não configurado no secrets.")
        
    token = st.secrets["AUTHENTIQUE_TOKEN"]
    deadline = calculate_deadline() 
    
    # Query GraphQL
    query = """
    mutation CreateDocumentMutation($document: DocumentInput!, $signers: [SignerInput!]!, $file: Upload!) {
        createDocument(document: $document, signers: $signers, file: $file) {
            id
            name
            deadline_at
        }
    }
    """
    
    # Variáveis
    variables = {
        "document": {
            "name": doc_name,
            "deadline_at": deadline
        },
        "signers": signers,
        "file": None
    }
    
    operations = json.dumps({"query": query, "variables": variables})
    map_data = json.dumps({"0": ["variables.file"]})
    
    file_obj.seek(0)
    
    files = {
        "operations": (None, operations, "application/json"),
        "map": (None, map_data, "application/json"),
        "0": (doc_name, file_obj, "application/pdf")
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        response = session.post(url, headers=headers, files=files, timeout=60)
        
        if response.status_code != 200:
            raise Exception(f"Erro API ({response.status_code}): {response.text}")
            
        data = response.json()
        
        if "errors" in data:
            # Captura erro específico de validação para mostrar mensagem clara
            errors_str = json.dumps(data['errors'])
            if "invalid_date" in errors_str:
                raise Exception(f"Erro de Data na API (Formato Inválido). Enviado: {deadline}")
            raise Exception(f"Erro Retornado pela Authentique: {errors_str}")
            
        return data["data"]["createDocument"]["id"]
        
    except requests.exceptions.ConnectionError:
        raise Exception("Erro de Conexão: Falha ao conectar à Autentique. Verifique a URL e sua internet.")
    except Exception as e:
        raise Exception(f"Falha no envio: {str(e)}")