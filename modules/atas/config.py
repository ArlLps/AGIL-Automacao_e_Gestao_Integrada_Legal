import json
import os

MODULE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(MODULE_DIR, "data")
EXAMPLES_DIR = os.path.join(MODULE_DIR, "examples")
EMAIL_DB_PATH = os.path.join(DATA_DIR, "email.json")
TEMP_DOCX_PATH = os.path.join(DATA_DIR, "temp_ata.docx")
TEMP_PDF_PATH = os.path.join(DATA_DIR, "temp_ata.pdf")
ATA_TEMPLATES_DIR = os.path.join(DATA_DIR, "templates")
AI_PROMPTS_PATH = os.path.join(DATA_DIR, "ai_prompts.json")
ATA_TEMPLATE_REGISTRY_PATH = os.path.join(DATA_DIR, "ata_templates.json")
EXAMPLES_REGISTRY_PATH = os.path.join(DATA_DIR, "examples_registry.json")
DIRECTORATES_PATH = os.path.join(DATA_DIR, "directorates.json")

# Configurações Gerais
DEFAULT_DIRECTORATES = [
    {
        "name": "Projetos",
        "slug": "projetos",
        "aliases": ["projetos"],
    },
    {
        "name": "Marketing",
        "slug": "marketing",
        "aliases": ["marketing"],
    },
    {
        "name": "Negócios",
        "slug": "negocios",
        "aliases": ["negócios", "negocios"],
    },
    {
        "name": "Jurídico-Financeiro",
        "slug": "jf",
        "aliases": ["jf", "jurídico-financeiro", "juridico-financeiro"],
    },
    {
        "name": "Parcerias",
        "slug": "parcerias",
        "aliases": ["parcerias"],
    },
    {
        "name": "Gestão de Pessoas",
        "slug": "gp",
        "aliases": ["gp", "gestão de pessoas", "gestao de pessoas"],
    },
    {
        "name": "Qualidade",
        "slug": "qualidade",
        "aliases": ["qualidade"],
    },
    {
        "name": "Diretoria Executiva",
        "slug": "direx",
        "aliases": ["direx", "diretoria executiva"],
    },
]

ESTADO_FERIADOS = 'MG'
TIMEZONE = 'America/Sao_Paulo'

# --- PROMPTS E EXEMPLOS (FEW-SHOT LEARNING) ---

DEFAULT_PROMPT_TRANSPARENCIAS_SYSTEM = """
Persona (Função): Você é o "Redator Especialista em Transparências" da organização. Sua função exclusiva é receber dados brutos (anotações ou tópicos de slides) das diretorias e transformá-los na seção "Transparências" da ata de reunião geral. Você atua sob as diretrizes da coordenação responsável.
Objetivo Primário: Converter listas e tópicos soltos em um texto narrativo, formal, coeso e padronizado, estruturado estritamente em parágrafos contínuos para as subseções "Realizadas" e "Planejadas" de cada diretoria.

Regras de Ouro (Invioláveis):
PROIBIÇÃO TOTAL DE TÓPICOS (Bullets): Nunca use listas, marcadores (bullets) ou quebras de linha para enumerar atividades. O texto deve ser sempre um parágrafo corrido e único para "Realizadas" e um parágrafo único para "Planejadas".
ZERO FORMATAÇÃO: Não use negrito, itálico ou formatação markdown no corpo do texto.
NOMES POR EXTENSO (Absoluto): Nomes de membros devem ser escritos com base na estrutura "Nome Primeiro-Sobrenome", respeitando nomes compostos. NUNCA use abreviações, iniciais ou apelidos.
CONTROLE DE SIGLAS: Utilize apenas siglas internas já consagradas (ex: PCO, PS, CSAT, DIREX). Na dúvida, ou para ferramentas e projetos, escreva por extenso.
TOM DE VOZ: Estritamente formal, impessoal e objetivo. Não adicione opiniões, não invente dados e não use jargões informais.

Padrão de Estrutura e Escrita Obrigatório:
Para cada diretoria analisada, você deve gerar exatamente duas linhas de texto (uma para Realizadas, outra para Planejadas), seguindo esta exata estrutura de abertura:
Para o bloco de Realizadas: * Início obrigatório: As atividades realizadas pela [Diretoria/Coordenadoria] de [Nome da Área] incluíram...
Conectivos para fluidez (use para evitar frases longas demais): Houve também..., Além disso..., Adicionalmente, foi feito..., Por fim....
Para o bloco de Planejadas: * Início obrigatório: As atividades planejadas incluem...
Conectivos para fluidez: Estão previstas também..., A coordenadoria visa..., A diretoria também planeja....

Processo de Execução:
Leia os tópicos fornecidos para a diretoria específica.
Identifique os nomes das pessoas e garanta que estão por extenso.
Agrupe as atividades concluídas no parágrafo "Realizadas:".
Agrupe as atividades futuras no parágrafo "Planejadas:".
Entregue apenas o parágrafo formatado, sem introduções ou conversas extras.

EXEMPLO DE SAÍDA IDEAL DE REALIZADAS (Siga este tom e formato):
"As atividades realizadas pela diretoria de Projetos incluíram a Reunião Semanal de Projetos, as sprints dos projetos Consenso e Constru coordenadas por Isadora Corrêa e João Pedro Franco, a atualização e encerramento do projeto Sinomar, e a confecção dos websites. Além disso, João Gabriel de Mendonça realizou a precificação de website e Pedro Henrique Oliveira finalizou a capacitação de ITEL."

EXEMPLO DE SAÍDA IDEAL DE PLANEJADAS (Siga este tom e formato):
"As atividades planejadas incluem a Reunião Semanal de Projetos e a continuação dos projetos em andamento. A diretoria também planeja terminar a precificação de Website com João Gabriel de Mendonça, definir a parceria com a Constru e iniciar um núcleo de pesquisas."
"""

DEFAULT_PROMPT_PAUTAS_SYSTEM = """
Persona (Função): Você é o "Redator Especialista em Pautas Eventuais" da organização. Sua função é redigir o texto narrativo das discussões, dinâmicas ou capacitações que ocorrem fora das pautas fixas da reunião geral. Você atua sob as diretrizes da coordenação responsável.
Objetivo Primário: Transformar anotações sobre discussões e apresentações em um texto narrativo, coeso, formal e impessoal (3ª pessoa), resumindo a pauta de forma clara e direta.

Regras de Ouro (Invioláveis):
TEXTO CORRIDO (Zero Tópicos): NUNCA, sob nenhuma hipótese, use listas, marcadores (bullet points) ou quebras de linha desnecessárias. O texto deve ser construído em parágrafos contínuos.
NOMES COMPLETOS SEMPRE (Absoluto): Ao citar quem apresentou ou participou da pauta, use estritamente e estrutura com base na estrutura "Nome Primeiro-Sobrenome". É terminantemente proibido usar apenas o primeiro nome, apelidos ou iniciais.
ZERO MARKDOWN: Não utilize negrito, itálico ou qualquer formatação de texto. Entregue apenas o texto limpo para facilitar o copia e cola.
IMPESSOALIDADE E TOM: Mantenha um tom oficial de Ata. Evite adjetivos emocionais, divagações ou opiniões não baseadas nos fatos fornecidos.
SIGLAS CONTROLADAS: Use apenas siglas internas reconhecidas (ex: PCO, DIREX, EMEJ). Na dúvida, escreva o termo por extenso.

Padrão de Escrita e Estruturação:
Introdução obrigatória do tema/palestrante: Comece com estruturas como: Nesta pauta, o/a membro/a [Nome Completo] apresentou..., Iniciou-se a discussão sobre..., Na pauta "[Nome da Pauta]", foi comunicado que....
Desenvolvimento e Conexão de ideias: Dê fluidez à narrativa utilizando conectivos como: Foi destacado que..., Em seguida, abordou-se..., Ademais, os membros discutiram..., Outra questão debatida foi....
Conclusão da Pauta: Encerre o assunto de forma clara com: Por fim, a pauta foi encerrada com..., Como deliberação final, decidiu-se que....

EXEMPLO DE SAÍDA IDEAL (Siga este tom e estilo rigorosamente):
"Nessa pauta, o diretor Nícholas Frutuoso explicou o funcionamento da sabatina e pediu que cada trainee se apresentasse. Em seguida, iniciaram-se as rodadas de perguntas presididas pelo diretor, onde os membros efetivos demonstraram interesse em questionar os candidatos sobre suas motivações. Por fim, foi aberto um espaço para considerações finais dos avaliados."
"""


def _read_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as file_obj:
            return json.load(file_obj)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def _resolve_registry_path(path_value):
    if not path_value:
        return None
    if os.path.isabs(path_value):
        return path_value
    return os.path.normpath(os.path.join(MODULE_DIR, path_value))


def get_directorates():
    directorates = _read_json(DIRECTORATES_PATH, DEFAULT_DIRECTORATES)
    normalized = []
    for entry in directorates:
        name = str(entry.get("name", "")).strip()
        slug = str(entry.get("slug", "")).strip()
        aliases = [str(alias).strip() for alias in entry.get("aliases", []) if str(alias).strip()]
        if not name or not slug:
            continue
        if name.lower() not in [alias.lower() for alias in aliases]:
            aliases.append(name)
        normalized.append(
            {
                "name": name,
                "slug": slug,
                "aliases": aliases,
            }
        )
    return normalized or DEFAULT_DIRECTORATES


def get_directorate_names():
    return [entry["name"] for entry in get_directorates()]


def get_map_jinja():
    mapping = {}
    for entry in get_directorates():
        for alias in entry.get("aliases", []):
            mapping[alias.lower()] = entry["slug"]
    return mapping


def build_transparency_template():
    return {
        entry["name"]: {
            "Realizado": "Não foram apresentadas atividades.",
            "Planejado": "Não foram apresentadas atividades.",
        }
        for entry in get_directorates()
    }


def normalize_transparency_payload(payload):
    if not isinstance(payload, dict):
        return build_transparency_template()

    normalized = build_transparency_template()
    mapping = get_map_jinja()
    slug_to_name = {entry["slug"]: entry["name"] for entry in get_directorates()}

    for raw_name, value in payload.items():
        slug = mapping.get(str(raw_name).strip().lower())
        if not slug:
            continue
        canonical_name = slug_to_name[slug]
        if isinstance(value, dict):
            normalized[canonical_name] = {
                "Realizado": value.get("Realizado", "Não foram apresentadas atividades."),
                "Planejado": value.get("Planejado", "Não foram apresentadas atividades."),
            }

    return normalized


def get_ai_prompts():
    prompts = _read_json(AI_PROMPTS_PATH, {})
    return {
        "transparencias": prompts.get("transparencias", DEFAULT_PROMPT_TRANSPARENCIAS_SYSTEM),
        "pautas": prompts.get("pautas", DEFAULT_PROMPT_PAUTAS_SYSTEM),
    }


def get_prompt_transparencias_system():
    return get_ai_prompts()["transparencias"]


def get_prompt_pautas_system():
    return get_ai_prompts()["pautas"]


def get_active_ata_template_path():
    registry = _read_json(ATA_TEMPLATE_REGISTRY_PATH, {})
    templates = registry.get("templates", [])
    active_template = registry.get("active_template")

    for entry in templates:
        resolved_path = _resolve_registry_path(entry.get("path", ""))
        if entry.get("id") == active_template and resolved_path and os.path.exists(resolved_path):
            return resolved_path

    return None


def get_active_example_paths(max_items=None):
    registry = _read_json(EXAMPLES_REGISTRY_PATH, {})
    active_examples = registry.get("active_examples", [])
    available_examples = {
        file_name: os.path.join(EXAMPLES_DIR, file_name)
        for file_name in os.listdir(EXAMPLES_DIR)
        if file_name.lower().endswith(".docx") and not file_name.startswith("~$")
    } if os.path.exists(EXAMPLES_DIR) else {}

    selected = [available_examples[file_name] for file_name in active_examples if file_name in available_examples]
    if max_items is not None:
        return selected[:max_items]
    return selected


DIRECTORIAS = get_directorate_names()
MAP_JINJA = get_map_jinja()
PROMPT_TRANSPARENCIAS_SYSTEM = DEFAULT_PROMPT_TRANSPARENCIAS_SYSTEM
PROMPT_PAUTAS_SYSTEM = DEFAULT_PROMPT_PAUTAS_SYSTEM