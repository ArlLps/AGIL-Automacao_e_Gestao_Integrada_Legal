# Personalizacao do Fork para Nova EJ

## Objetivo

Este guia descreve como preparar o fork do repositório base para uma nova Empresa Junior cliente, sem misturar dados entre organizações.

## Fluxo recomendado

1. Crie um fork privado ou um novo repositório a partir da base principal.
2. Renomeie o repositório e ajuste a descrição para a EJ cliente.
3. Clone o fork localmente e configure os segredos do ambiente antes de entregar acesso.

## Checklist de personalizacao

### 1. Identidade da organizacao

- Acesse `Gerenciamento > Organizacao`.
- Defina nome do produto, nome da organização, saudação padrão, assunto padrão de e-mail e linha de suporte.
- Ajuste os nomes de dinâmicas internas, como reconhecimento e mensagens positivas.

### 2. Diretorias de transparências

- Acesse `Gerenciamento > ATAs > Diretorias`.
- Cadastre as diretorias reais da EJ cliente.
- Preencha o campo `slug` com um identificador estável e curto.
- Use `aliases` para nomes alternativos que possam aparecer no PDF ou nas anotações.

### 3. Templates

- Acesse `Gerenciamento > ATAs > Template` e envie o modelo de ata da EJ.
- Acesse `Gerenciamento > Contratos` e envie os modelos de contrato que serão usados.
- Se o cliente for usar o template genérico, valide se ele cobre as diretorias configuradas.

### 4. Membros e exemplos

- Atualize `Gerenciamento > ATAs > Membros` com a base real da EJ.
- Troque o acervo em `Gerenciamento > ATAs > Acervo` por atas reais ou por um conjunto de demonstração da própria EJ.

### 5. Prompts e estilo

- Revise `Gerenciamento > ATAs > Prompts IA`.
- Ajuste instruções de linguagem, formalidade e siglas internas conforme o padrão documental da EJ.

### 6. Segredos e integrações

- Configure `GOOGLE_API_KEY` para IA.
- Configure `AUTHENTIQUE_TOKEN` se o cliente usar a Authentique.
- Configure `EMAIL_SENDER` e `EMAIL_PASSWORD` para o disparo de e-mails.
- Valide as permissões e o ambiente de deploy antes da entrega.

## Boas praticas por cliente

- Mantenha um fork ou repositório isolado por EJ.
- Não reutilize bases reais de membros, atas ou templates entre clientes.
- Faça o onboarding inicial em uma branch de implantação e só depois consolide na principal do cliente.
- Registre no próprio repositório do cliente as escolhas de templates, diretorias e integrações.

## O que normalmente ainda precisa de ajuste manual

- Conteúdo dos templates DOCX.
- Nomenclatura de cargos e áreas.
- Assuntos e textos padrão de notificação.
- Secrets e integrações externas.

## Entrega recomendada

- Repositório do cliente já parametrizado.
- Credenciais configuradas no ambiente de deploy.
- Templates enviados e ativos.
- Base de membros validada.
- Uma ATA e um contrato de teste gerados com sucesso.