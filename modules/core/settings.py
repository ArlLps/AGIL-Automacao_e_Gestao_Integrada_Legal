import json
import os


MODULE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(MODULE_DIR, "data")
ORGANIZATION_SETTINGS_PATH = os.path.join(DATA_DIR, "organization_profile.json")

DEFAULT_SETTINGS = {
    "product_name": "AGIL",
    "organization_name": "sua organizacao",
    "homepage_caption": "Plataforma modular para centralizar processos automatizados da sua organizacao.",
    "default_notification_recipients": "",
    "notification_greeting": "Bom dia, boa tarde e boa noite!",
}


def _read_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as file_obj:
            return json.load(file_obj)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def _write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file_obj:
        json.dump(data, file_obj, ensure_ascii=False, indent=4)


def ensure_settings_file():
    if not os.path.exists(ORGANIZATION_SETTINGS_PATH):
        _write_json(ORGANIZATION_SETTINGS_PATH, DEFAULT_SETTINGS)


def load_settings():
    ensure_settings_file()
    settings = DEFAULT_SETTINGS.copy()
    settings.update(_read_json(ORGANIZATION_SETTINGS_PATH, {}))
    return settings


def save_settings(settings):
    merged = DEFAULT_SETTINGS.copy()
    merged.update(settings)
    _write_json(ORGANIZATION_SETTINGS_PATH, merged)


def get_product_name():
    return load_settings()["product_name"]


def get_organization_name():
    return load_settings()["organization_name"]


def get_homepage_caption():
    return load_settings()["homepage_caption"]


def get_default_notification_recipients():
    return load_settings()["default_notification_recipients"]


def get_notification_greeting():
    return load_settings()["notification_greeting"]