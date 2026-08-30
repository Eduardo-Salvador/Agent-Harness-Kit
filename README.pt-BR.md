# Agent Harness Kit

![Agent Harness Kit — contexto, tasks, checks e entrega](docs/assets/agent-harness-kit-banner.svg)

<p align="center">
  <strong>Dê aos agentes de código contexto durável, execução limitada e um caminho claro até a conclusão.</strong><br>
  Contratos agnósticos de plataforma com entradas nativas para Codex e Claude Code.
</p>

<p align="center">
  <img alt="Versão 0.6.0" src="https://img.shields.io/badge/vers%C3%A3o-0.6.0-4967ff">
  <img alt="Python 3.10 ou mais recente" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&amp;logoColor=white">
  <img alt="Instale com uv, pipx ou pip" src="https://img.shields.io/badge/instalador-uv%20%7C%20pipx%20%7C%20pip-DE5FE9">
  <img alt="Compatível com Codex" src="https://img.shields.io/badge/agente-Codex-11131a">
  <img alt="Compatível com Claude Code" src="https://img.shields.io/badge/agente-Claude_Code-D97757">
  <img alt="Licença MIT" src="https://img.shields.io/badge/licen%C3%A7a-MIT-ffb84d">
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="#comece-aqui">Comece aqui</a> · <a href="#escolha-o-ritmo">Modos</a> · <a href="docs/ARCHITECTURE.md">Arquitetura</a>
</p>

**Versão do código-fonte: `0.6.0`.** O Kit é um scaffold executável e orientado a artefatos. Ele não mantém um daemon em segundo plano nem bloqueia o sistema operacional. Enquanto um agente orquestrador está ativo, pode disparar em paralelo subtasks independentes e prontas quando a plataforma comprova essa capacidade.

> **Um harness maduro o bastante para saber quando sair do caminho.** O router nativo não trata todo prompt como um grande projeto: gates determinísticos de segurança separam edições estáticas imediatas, pequenas mudanças verificadas em modo “vibe”, trabalho gerenciado pelo grafo e engenharia completa. A IA só é consultada diante de ambiguidade real; risco, checks com falha ou crescimento de escopo promovem automaticamente o trabalho, sem deixar a velocidade furar a segurança.

## Comece aqui

Abra qualquer terminal, inclusive o terminal integrado do VS Code em **Terminal > New Terminal**, e instale a CLI uma vez. O [`uv`](https://docs.astral.sh/uv/) é a opção isolada recomendada:

```bash
uv tool install agent-harness-kit-cli
```

Também é possível usar `pipx` ou instalar diretamente do PyPI com `pip`:

```bash
pipx install agent-harness-kit-cli
python -m pip install agent-harness-kit-cli
```

No Windows, você também pode executar `py -m pip install agent-harness-kit-cli`. Ao usar `pip` diretamente, prefira um ambiente virtual; `uv` e `pipx` isolam a CLI automaticamente.

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

https://github.com/user-attachments/assets/d89fe815-da49-452e-bcd4-18f33f728f18

[Baixar o MP3 em português](media/agent-harness-kit-overview-pt-BR.mp3) · [Ler o roteiro em português](media/overview-script-pt-BR.txt)

## Por que ele existe

| Sem coordenação durável | Com o Kit |
| --- | --- |
| O agente varre tudo e tenta adivinhar o contexto | O contexto aprovado é lido antes de buscas amplas |
| Uma context window longa fica lenta e cara | O estado durável do grafo permite retomar em uma janela nova somente pelo entorno ativo, sem depender do histórico do chat |
| Decisões humanas se misturam com tasks técnicas | `PENDING.md` e `TASK-GRAPH.md` têm autoridades separadas |
| Reviews se repetem ou ecoam o implementador | Um contexto novo revisa a SPEC uma vez, com no máximo uma re-review focada |
| A conclusão espera aprovação cerimonial | O trabalho aprovado nos checks é concluído, informado e avança |
| Vários agentes colidem | Áreas, leases de arquivos e handoffs são explícitos |
| Trabalho independente espera em fila linear | O orquestrador ativo ocupa a capacidade paralela comprovada e repõe a primeira vaga liberada |
| Uma troca mínima de CSS/texto aciona o harness inteiro | Edições `direct-trivial` vão direto ao arquivo, sem entrevista, SPEC, grafo, TDD ou review |
| Uma pequena correção local de comportamento aciona toda a cerimônia | `vibe` altera diretamente um workstream de baixo risco, não cria artefatos e precisa passar em um check focado |
| Notas de estudo surgem em pastas arbitrárias | O estudo só começa após aprovação do destino |
| Ideias de feature viram código cedo demais | A descoberta automática compara caminhos e registra primeiro um brief aprovado |
| Tasks vagas fazem o agente improvisar e reler tudo | Trabalho não trivial recebe um writing plan conciso e pequenas specs executáveis |
| Testes aparecem somente depois do código | Tasks de comportamento provam RED primeiro, chegam ao GREEN mínimo e rodam regressão proporcional |
| Tasks pequenas do grafo criam pilhas de evidências | Tasks determinísticas elegíveis como `graph-only` registram apenas resultado/check na transição do grafo |

## O que muda no projeto

- `PROJECT-CONTEXT.md` registra produto, restrições, modo e decisões importantes já aprovadas.
- `FEATURE-*.md` fecha lacunas de comportamento; `PLAN-*.md` decompõe trabalho não trivial aprovado sem criar outro plano por task.
- `PENDING.md` responde o que ainda depende de uma pessoa e o que falta no nível do produto.
- `TASK-GRAPH.md` controla ordem técnica, dependências, leases, progresso e o próximo trabalho pronto; cada `TASK.md` é uma spec executável autocontida.
- `CODEX-AGENT-DISPATCH.md` comprova qual agente dinâmico do Codex foi criado, com qual role, contexto limitado, modelo/raciocínio, contexto retornado e resposta do adaptador.
- `AGENTS.md` e `CLAUDE.md` da raiz encaminham agentes capazes para as mesmas regras neutras contidas em `agent-harness-kit/`.

Frontend, backend, dados, infraestrutura, integração e estudo usam contextos separados quando a plataforma oferece essa capacidade. Cada nó ativo pode declarar `read_set` focado, `write_set` exclusivo, `impact_set` relacionado e revisão da fonte, reduzindo varreduras amplas sem inventar um segundo grafo.

Conversas longas ficam naturalmente mais lentas e consomem mais tokens em todas as famílias de modelos, porque cada turno precisa processar mais material acumulado. O Kit trata isso como algo normal: contexto do projeto, pendências, grafo, specs e decisões são a memória durável. Abra uma context window nova, siga a ordem de retomada e carregue apenas o entorno do nó ativo; a nova janela enxerga o que está concluído, ativo, pronto, bloqueado e qual é o próximo passo sem reler o chat anterior.

## O ciclo de trabalho

Toda solicitação é roteada antes de o Harness carregar o contexto do projeto ou iniciar cerimônias. Regras determinísticas escolhem primeiro entre quatro caminhos: `direct-trivial` para edições estáticas/mecânicas, `vibe` para uma pequena mudança local de comportamento já decidida com check focado e zero artefatos, `graph-only` para trabalho de baixo risco que realmente precisa de agendamento/ownership e `full-harness` para trabalho consequente ou ambíguo. Um classificador de IA econômico só é usado quando o caminho continua ambíguo e classificar custa menos que fazer o trabalho.

Um pedido explícito de Harness completo sempre vence. Autenticação, segurança/privacidade, contratos de dados/schema/API, dependências, migrações, permissões/acessibilidade, efeitos externos, integrações, vários workstreams, decisões consequentes, ambiguidade não resolvida ou verificação com falha forçam `full-harness`, mesmo quando foi pedido um caminho rápido. Se o escopo crescer durante uma edição rápida, o agente para e promove antes de novas mudanças.

Você pode inspecionar a mesma pré-classificação no terminal com `agent-harness route "seu pedido"`. Use `--mode vibe` ou `--mode full` para declarar uma preferência, `--workstreams 2` quando houver mais de uma área e `--graph-bound --graph-only-eligible` para trabalho de baixo risco já especificado no grafo. O comando sempre devolve um dos quatro caminhos em JSON; diante de ambiguidade, usa `full-harness` com segurança e sinaliza que um classificador de IA econômico pode refinar a decisão.

1. O agente lê o contexto aprovado, depois as pendências humanas/macro e por último o grafo técnico.
2. Uma feature nova com decisões de produto abertas entra automaticamente em um brainstorm focado: o contexto conhecido é reaproveitado, caminhos viáveis são comparados e você aprova um brief antes de o grafo mudar.
3. Trabalho não trivial já aprovado vira um writing plan com unidades verificáveis de aproximadamente dois a cinco minutos; trabalho realmente simples mantém apenas uma spec inline curta.
4. No Codex, o dispatcher nativo escolhe a role neutra, monta somente o pacote de contexto focado, resolve modelo/raciocínio e cria um subagente executável novo com `fork_turns: none`. Ele registra identidade, contexto e resposta retornados; sem subagentes, a implementação degrada explicitamente para execução sequencial, enquanto a revisão ainda exige outro contexto novo. Depois, o agente executa sua SPEC autocontida sem inventar comportamento. Código segue RED → GREEN → REFACTOR; contradição ou RED inválido volta ao planejamento.
5. Quando dois ou mais nós sem colisão estão prontos e a plataforma informa capacidade numérica, o orquestrador reserva leases e contextos distintos, dispara todo o lote seguro sem esperar entre chamadas e repõe uma vaga após o primeiro evento de conclusão ou atenção. Ramos dependentes convergem por um nó explícito de integração.
6. Trabalho aprovado nos checks é concluído e informado imediatamente; a próxima tarefa pronta pode começar sem aprovação cerimonial. Uma task `graph-only` inline-simple elegível roda seu check determinístico e avança somente o grafo — sem handoff, pacote de review, artefato de review ou logs copiados. Comportamento, TDD, contratos, risco, integrações, checks falhos e assurance continuam no fluxo completo de handoff/review.
7. Para `handoff-review`, depois da verificação o orquestrador lança um revisor independente em contexto novo — de preferência um subagente quando disponível. Ele recebe a SPEC versionada, diff relevante, handoff e evidências de teste, reconstrói a aceitação antes de ler o código e nunca depende do prompt original ou da memória do implementador. A garantia segue não bloqueante: uma review proporcional e, apenas para bloqueio real, no máximo uma re-review focada. Não existe terceiro loop.

No trabalho gerenciado pelo grafo, toda atualização mostra etapa, andamento, trabalho automático, pendências humanas e técnicas, bloqueios, próxima ação e caminhos inspecionáveis. `direct-trivial` e `vibe` retornam apenas um resumo curto da edição e do check; vibe sempre informa sua verificação focada aprovada.

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

- O Kit não roda sem supervisão nem abre chats visíveis sozinho. Durante uma sessão ativa de orquestração, pode lançar subagentes/tasks internas compatíveis em paralelo; integração, deploy, publicação e criação de tasks visíveis continuam exigindo capacidade e autoridade próprias.
- Leases são contratos validados, não locks do sistema operacional.
- Threads, subagentes, worktrees, MCPs, rede e modelo dependem das capacidades e autorizações reais do host. Quando o roteamento automático está explicitamente aprovado e o host oferece overrides, o dispatch aplica modelo/raciocínio resolvidos e registra a confirmação do adaptador; caso contrário, a rota fica visivelmente manual ou bloqueada.
- Um grafo de conhecimento pode reduzir varreduras amplas, mas apenas consultas focadas e orçamentos de execução evitam desperdício; nenhuma ferramenta garante menos tokens. Consulte o [contrato de execução focada por grafo](docs/SCOPED-GRAPH-EXECUTION.md) para os limites de `read_set`, `write_set`, `impact_set`, proveniência e Graphify.

Quer aprofundar? Veja a [instalação passo a passo](docs/EMBEDDED-INSTALLATION.md), o [modo hackathon](docs/HACKATHON-MODE.md), a [arquitetura](docs/ARCHITECTURE.md), o [contrato de validação](docs/VALIDATION.md), a [auditoria de prontidão](docs/PUBLICATION-READINESS.md) e a [licença MIT](LICENSE).
