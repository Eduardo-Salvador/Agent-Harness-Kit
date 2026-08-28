# Agent Harness Kit

![Agent Harness Kit — contexto, tasks, checks e entrega](docs/assets/agent-harness-kit-banner.svg)

<p align="center">
  <strong>Dê aos agentes de código contexto durável, execução limitada e um caminho claro até a conclusão.</strong><br>
  Contratos agnósticos de plataforma com entradas nativas para Codex e Claude Code.
</p>

<p align="center">
  <img alt="Versão 0.5.3" src="https://img.shields.io/badge/vers%C3%A3o-0.5.3-4967ff">
  <img alt="Python 3.10 ou mais recente" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&amp;logoColor=white">
  <img alt="Instalado com uv" src="https://img.shields.io/badge/instalador-uv-DE5FE9?logo=uv&amp;logoColor=white">
  <img alt="Compatível com Codex" src="https://img.shields.io/badge/agente-Codex-11131a">
  <img alt="Compatível com Claude Code" src="https://img.shields.io/badge/agente-Claude_Code-D97757">
  <img alt="Licença MIT" src="https://img.shields.io/badge/licen%C3%A7a-MIT-ffb84d">
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="#comece-aqui">Comece aqui</a> · <a href="#escolha-o-ritmo">Modos</a> · <a href="docs/ARCHITECTURE.md">Arquitetura</a>
</p>

**Versão do código-fonte: `0.5.3`.** O Kit é um scaffold executável e orientado a artefatos. Agentes capazes seguem seus arquivos, contratos e validadores; ele não é um daemon que inicia agentes ou bloqueia o sistema operacional.

## Comece aqui

Instale a CLI uma vez com o [`uv`](https://docs.astral.sh/uv/):

```bash
uv tool install agent-harness-kit-cli
```

Depois, abra o projeto que você quer organizar e execute:

```bash
agent-harness install
```

Abra um **novo contexto do agente na raiz do projeto**. O Kit se apresentará, verificará somente o estado inicial necessário e começará uma descoberta curta antes de propor implementação.

> Quer apenas conferir antes? Execute `agent-harness install --dry-run`. Instruções existentes na raiz são preservadas por blocos gerenciados e coexistência com namespace.

## Escolha o ritmo

| Diga isto | O que acontece |
| --- | --- |
| “Use entrega normal” | Descoberta completa quando necessária, implementação limitada, checks e garantia independente |
| “Use modo hackathon” | No máximo duas perguntas coesas e depois um grafo focado em demo para chegar a um MVP testável |
| “Também quero aprender” | Adiciona estudo guiado somente após você aprovar o caminho Markdown, Obsidian, alvo/MCP do Notion ou outro destino |

O modo hackathon mantém estado, leases, checks e status, mas usa review leve por padrão e corta escopo secundário antes do caminho principal da demo.

## Prefere ouvir?

Ouça uma explicação curta em português sobre o que o projeto faz e como seu fluxo funciona.

https://github.com/user-attachments/assets/e3cf95a9-2615-41bc-aec1-f68ffce7df18

[Baixar o MP3 em português](media/agent-harness-kit-overview-pt-BR.mp3) · [Ler o roteiro em português](media/overview-script-pt-BR.txt)

## Por que ele existe

| Sem coordenação durável | Com o Kit |
| --- | --- |
| O agente varre tudo e tenta adivinhar o contexto | O contexto aprovado é lido antes de buscas amplas |
| Decisões humanas se misturam com tasks técnicas | `PENDING.md` e `TASK-GRAPH.md` têm autoridades separadas |
| Reviews se repetem indefinidamente | Uma review e no máximo uma re-review focada |
| A conclusão espera aprovação cerimonial | O trabalho aprovado nos checks é concluído, informado e avança |
| Vários agentes colidem | Áreas, leases de arquivos e handoffs são explícitos |
| Notas de estudo surgem em pastas arbitrárias | O estudo só começa após aprovação do destino |

## O que muda no projeto

- `PROJECT-CONTEXT.md` registra produto, restrições, modo e decisões importantes já aprovadas.
- `PENDING.md` responde o que ainda depende de uma pessoa e o que falta no nível do produto.
- `TASK-GRAPH.md` controla ordem técnica, dependências, leases, progresso e o próximo trabalho pronto.
- `AGENTS.md` e `CLAUDE.md` da raiz encaminham agentes capazes para as mesmas regras neutras contidas em `agent-harness-kit/`.

Frontend, backend, dados, infraestrutura, integração e estudo usam contextos separados quando a plataforma oferece essa capacidade. Cada nó ativo pode declarar `read_set` focado, `write_set` exclusivo, `impact_set` relacionado e revisão da fonte, reduzindo varreduras amplas sem inventar um segundo grafo.

## O ciclo de trabalho

1. O agente lê o contexto aprovado, depois as pendências humanas/macro e por último o grafo técnico.
2. Ele carrega somente a tarefa ativa e seu contexto direto, assume um lease exclusivo e implementa dentro do orçamento declarado.
3. Trabalho aprovado nos checks é concluído e informado imediatamente; a próxima tarefa pronta pode começar sem aprovação cerimonial.
4. A review independente funciona como garantia não bloqueante: uma revisão proporcional e, somente para bloqueio real, no máximo uma re-review focada. Não existe terceiro loop.

Toda atualização de progresso mostra etapa, andamento, trabalho que continuará automaticamente, pendências humanas e técnicas, bloqueios, próxima ação e caminhos inspecionáveis.

## Perfis

| Perfil | Inclui | Melhor uso |
| --- | --- | --- |
| `core` | Entrega, grafo, status, review e validação | Maioria dos projetos |
| `core-learning` | `core` mais aprendizado opcional do projeto | Prática guiada e debriefings |
| `full` | `core-learning` mais o pacote separado de estudo do harness | Estudar a própria engenharia de harness |

O aprendizado nunca é ativado silenciosamente. O usuário escolhe o caminho Markdown, local do Obsidian, alvo/MCP do Notion ou outro destino exato antes da criação de qualquer nota.

## Projeto novo ou harness existente

Em um projeto vazio, a descoberta vem antes de propostas de stack, arquitetura, marca ou funcionalidades. Em um repositório maduro, o Kit preserva as instruções existentes e usa coexistência com namespace; ele nunca sobrescreve silenciosamente `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.claude/` ou outra autoridade. Veja o [playbook de adoção madura](harness/playbooks/mature-harness-adoption.md).

## Limites honestos

- O Kit coordena agentes capazes por arquivos; não abre chats, integra branches, faz deploy ou publica notas autonomamente.
- Leases são contratos validados, não locks do sistema operacional.
- Threads, subagentes, worktrees, MCPs, rede e modelo dependem das capacidades e autorizações reais do host.
- Um grafo de conhecimento pode reduzir varreduras amplas, mas apenas consultas focadas e orçamentos de execução evitam desperdício; nenhuma ferramenta garante menos tokens. Consulte o [contrato de execução focada por grafo](docs/SCOPED-GRAPH-EXECUTION.md) para os limites de `read_set`, `write_set`, `impact_set`, proveniência e Graphify.

Quer aprofundar? Veja a [instalação passo a passo](docs/EMBEDDED-INSTALLATION.md), o [modo hackathon](docs/HACKATHON-MODE.md), a [arquitetura](docs/ARCHITECTURE.md), o [contrato de validação](docs/VALIDATION.md), a [auditoria de prontidão](docs/PUBLICATION-READINESS.md) e a [licença MIT](LICENSE).
