# AGIL - Automação e Gestão Integrada Legal

Este repositório está organizado como um **sistema integrado modular** para centralizar automações de processos de uma organização.

## Estrutura

```
app.py
pages/
	01_ATAs.py
	02_Contratos.py
modules/
	atas/
		page_atas.py
		config.py
		ia_utils.py
		authentique_utils.py
		email_utils.py
		history_utils.py
		data/
			email.json
			ai_prompts.json
			ata_templates.json
			examples_registry.json
			templates/
		examples/
			*.docx
	contratos/
		page_contratos.py
		config.py
		document_utils.py
		authentique_utils.py
		data/
			template_registry.json
			templates/
	core/
		settings.py
		data/
			organization_profile.json
	ui/
		sidebar.py
```

## Módulos atuais

- `ATAs`: automação completa de geração, revisão, assinatura e notificação de atas.
- `Contratos`: preenchimento de contrato com template DOCX, conversão para PDF e envio para assinatura via Authentique.
- `Gerenciamento`: central administrativa para gerenciar identidade da organização, prompts, membros, templates e acervo de conhecimento.

## Como executar

1. Instale as dependências:
	 - `pip install -r requirements.txt`
2. Execute a interface inicial:
	 - `streamlit run app.py`
3. No primeiro uso, acesse `Gerenciamento` para configurar a organização, cadastrar membros e ativar templates.
4. Depois disso, escolha o módulo `ATAs` ou `Contratos`.

## Onboarding

- O repositório acompanha um kit neutro de onboarding com templates genéricos, exemplos fictícios e dados iniciais de demonstração.
- As orientações de parametrização inicial estão em `docs/onboarding.md`.

## Próximos passos

- Adicionar novos módulos em `modules/<nome_do_modulo>/`.
- Conectar o menu da interface inicial aos novos módulos.
