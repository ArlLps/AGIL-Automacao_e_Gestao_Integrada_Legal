# Onboarding White-Label

## Objetivo

Este pacote inicial prepara o produto para distribuicao com ativos neutros, sem dados reais de clientes ou de uma organizacao especifica.

## O que acompanha o repositório

- Perfil neutro da organizacao em `modules/core/data/organization_profile.json`
- Template generico de ATA em `modules/atas/data/templates/ata_reuniao_generica.docx`
- Dois exemplos ficticios de atas em `modules/atas/examples/`
- Base ficticia de membros e e-mails em `modules/atas/data/email.json`
- Template generico de contrato em `modules/contratos/data/templates/contrato_prestacao_servicos_generico.docx`

## Primeira configuracao recomendada

1. Acesse `Gerenciamento > Organizacao` e defina nome do produto, nome da organizacao e destinatarios padrao.
2. Ajuste os nomes de dinâmicas internas, como reconhecimento e mensagens positivas, se o cliente usar outra nomenclatura.
3. Revise os prompts de IA em `Gerenciamento > ATAs > Prompts IA`.
4. Substitua ou complemente a lista ficticia de membros em `Gerenciamento > ATAs > Membros`.
5. Ajuste os templates ativos em `Gerenciamento > ATAs > Template` e `Gerenciamento > Contratos` caso o cliente tenha modelos proprios.
6. Atualize o acervo de exemplos em `Gerenciamento > ATAs > Acervo` para refletir o estilo desejado.

## Observacoes

- Os templates enviados no pacote sao apenas ponto de partida e podem ser substituidos sem alterar codigo.
- O repositorio nao depende mais de ativos reais da CONSELT para funcionar.
- O produto agora pode ser entregue para outra Empresa Junior com parametrizacao inicial e sem carregamento de dados sensiveis.