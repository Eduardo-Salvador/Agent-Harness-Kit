# Agent Harness Kit

![Agent Harness Kit — contexto, tasks, checks e entrega](docs/assets/agent-harness-kit-banner.svg)

<p align="center">
  <strong>Dê aos agentes de código contexto durável, execução limitada e um caminho claro até a conclusão.</strong><br>
  Contratos agnósticos de plataforma com entradas nativas para Codex e Claude Code.
</p>

<p align="center">
  <img alt="Versão 0.7.1" src="https://img.shields.io/badge/vers%C3%A3o-0.7.1-4967ff">
  <img alt="Python 3.10 ou mais recente" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&amp;logoColor=white">
  <img alt="Instale com uv, pipx ou pip" src="https://img.shields.io/badge/instalador-uv%20%7C%20pipx%20%7C%20pip-DE5FE9">
  <img alt="Compatível com Codex" src="https://img.shields.io/badge/agente-Codex-11131a">
  <img alt="Compatível com Claude Code" src="https://img.shields.io/badge/agente-Claude_Code-D97757">
  <img alt="Licença MIT" src="https://img.shields.io/badge/licen%C3%A7a-MIT-ffb84d">
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="#comece-aqui">Comece aqui</a> · <a href="#escolha-o-ritmo">Modos</a> · <a href="docs/ARCHITECTURE.md">Arquitetura</a>
</p>

**Versão do código-fonte: `0.7.1`.** A descoberta inicial agora resolve arquitetura e organização de pastas pelo contexto aprovado ou pelas evidências do repositório, pergunta somente quando algo continua incerto e trata convenções de código como opcionais. A execução continua adaptativa: quatro lanes estáveis, assurance independente `none|light|full`, formatos compacto/completo, resume guiado por evidência real, preflight obrigatório, handoffs apenas com consumidor e uma escada proporcional de testes.

> **Um harness maduro o bastante para saber quando sair do caminho.** O router nativo não trata todo prompt como um grande projeto: gates determinísticos de segurança separam edições estáticas imediatas, pequenas mudanças verificadas em modo “vibe”, trabalho gerenciado pelo grafo e engenharia completa. A IA só é consultada diante de ambiguidade real; risco, checks com falha ou crescimento de escopo promovem automaticamente o trabalho, sem deixar a velocidade furar a segurança.

## Comece aqui

Abra qualquer terminal, inclusive o terminal integrado do VS Code em **Terminal > New Terminal**, e instale a CLI uma vez. O [`uv`](https://docs.astral.sh/uv/) é a opção isolada recomendada:

```bash
uv tool install agent-harness-kit-cli
```

Já instalou antes? `uv tool install` não atualiza automaticamente uma ferramenta existente. Execute `uv tool upgrade agent-harness-kit-cli` e confirme com `agent-harness --version` antes de instalar em outro projeto.

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

A instalação fica imediatamente detectável pelos agentes compatíveis. Ela cria a pasta contida `agent-harness-kit/` **e também** cria ou atualiza estes dois arquivos na raiz do projeto:

```text
seu-projeto/
├── AGENTS.md          # entrada do Codex
├── CLAUDE.md          # entrada do Claude Code
└── agent-harness-kit/ # distribuição versionada do Kit
```

Instruções que já existiam na raiz são preservadas fora de um pequeno bloco gerenciado. Execute `agent-harness doctor` para conferir as três entradas. Depois, abra um **novo contexto do agente na raiz do projeto** para o host recarregar `AGENTS.md` ou `CLAUDE.md`; nos hosts que carregam instruções da raiz normalmente, não é necessário colar nenhum prompt de ativação.

> Quer apenas conferir antes? Execute `agent-harness install --dry-run`. Instruções existentes na raiz são preservadas por blocos gerenciados e coexistência com namespace.

## O que ele efetivamente faz

O Agent Harness Kit é uma camada local de governança de execução para agentes de programação. Codex ou Claude continuam escrevendo o software; o Kit determina como o trabalho é delimitado, ordenado, verificado, retomado e, quando o host permite, distribuído entre agentes independentes.

- `route` seleciona o caminho de execução mais leve e seguro e um nível de assurance independente.
- `preflight` verifica arquivos, scripts, nomes de ambiente, comandos, validador, necessidades de navegador/sandbox e capacidade de workers antes da decomposição.
- Contexto e estado de grafo duráveis permitem que uma conversa nova retome a partir da evidência atual do repositório/runtime, sem reconstruir o trabalho pelo histórico do chat.
- Na primeira execução, o agente reaproveita decisões comprovadas, resolve arquitetura e organização de pastas antes do planejamento e só pergunta sobre convenções de código opcionais quando o repositório ainda não as definiu. O usuário pode especificar a estrutura, escolher opções relevantes ou pedir uma recomendação.
- Leases de ownership e `schedule` selecionam o maior lote sem colisões entre os nós prontos do grafo.
- `transition` avança o grafo atomicamente e registra eventos encadeados por hash; `metrics` relata sinais de cerimônia, implementação, gates, review e remediação.
- Uma escada proporcional de testes e reviews criadas apenas para consumidores reais mantêm trabalho pequeno realmente pequeno sem perder garantia independente quando ela é necessária.

A CLI executa instalação, inspeção, roteamento, preflight, agendamento, transições de estado, métricas e preparação de dispatch de forma determinística. O host do agente executa a programação, a criação real de subagentes, a review, a integração e a entrega conforme suas capacidades e permissões.

## Escolha o ritmo

| Diga isto | O que acontece |
| --- | --- |
| “Use entrega normal” | Descoberta completa quando necessária, implementação limitada, checks e garantia independente |
| “Use modo hackathon” | No máximo duas perguntas coesas e depois um grafo focado em demo para chegar a um MVP testável |
| “Também quero aprender” | Adiciona estudo guiado somente após você aprovar o caminho Markdown, Obsidian, alvo/MCP do Notion ou outro destino |

O modo hackathon mantém estado, leases, checks e status, mas usa review leve por padrão e corta escopo secundário antes do caminho principal da demo.

## Prefere ouvir?

Ouça uma explicação curta em português sobre o que o projeto faz e como seu fluxo funciona.

[Ouvir ou baixar o MP3 em português](media/agent-harness-kit-overview-pt-BR.mp3) · [Abrir o MP4 compatível com GitHub](media/agent-harness-kit-overview-pt-BR.mp4) · [Ler o roteiro em português](media/overview-script-pt-BR.txt)

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

Toda solicitação mutável usa um de quatro caminhos públicos: `direct-trivial`, `vibe`, `graph-only` ou `full-harness`. Assurance é uma decisão separada: `none`, `light` ou `full`. O Harness completo é automático apenas para dois ou mais agentes reais, loop humano, auditoria exigida, modelo insuficiente, ambiguidade consequente não resolvida ou pedido explícito. Mudanças reais de segurança/privacidade/autorização/destrutivas exigem auditoria completa; palavras como API ou dependência, sozinhas, não forçam o caminho.

O Harness completo pode ser compacto para um resultado delimitado ou completo para discovery, coordenação multiagente, governança humana ou auditoria total. Auditoria e diagnóstico somente leitura não acionam first-run. Ao retomar, o agente sonda primeiro o estado real de árvore/processos/testes e consulta artefatos duráveis apenas para preencher lacunas; evidência atual supera handoffs obsoletos.

Você pode inspecionar a mesma pré-classificação no terminal com `agent-harness route "seu pedido"`. Use `--mode vibe` ou `--mode full` para declarar uma preferência, `--workstreams 2` quando houver mais de uma área e `--graph-bound --graph-only-eligible` para trabalho de baixo risco já especificado no grafo. O comando sempre devolve um dos quatro caminhos em JSON; diante de ambiguidade, usa `full-harness` com segurança e sinaliza que um classificador de IA econômico pode refinar a decisão.

1. O agente lê o contexto aprovado, depois as pendências humanas/macro e por último o grafo técnico.
2. Uma feature nova com decisões de produto abertas entra automaticamente em um brainstorm focado: o contexto conhecido é reaproveitado, caminhos viáveis são comparados e você aprova um brief antes de o grafo mudar.
3. Trabalho planejado usa unidades verificáveis de 15–30 minutos ativos; exceções justificam atomicidade, custo de runtime ou risco.
4. No Codex, o dispatcher nativo escolhe a role neutra, monta somente o pacote de contexto focado, resolve modelo/raciocínio e cria um subagente executável novo com `fork_turns: none`. Ele registra identidade, contexto e resposta retornados; sem subagentes, a implementação degrada explicitamente para execução sequencial, enquanto a revisão ainda exige outro contexto novo. Depois, o agente executa sua SPEC autocontida sem inventar comportamento. Código segue RED → GREEN → REFACTOR; contradição ou RED inválido volta ao planejamento.
5. Quando dois ou mais nós sem colisão estão prontos e a capacidade é maior que um, o orquestrador dispara o lote seguro, informa a quantidade de workers ativos e repõe a primeira vaga. Após 60–90 segundos sem progresso observável, avisa; na segunda ocorrência consecutiva, interrompe e reatribui.
6. A verificação sobe apenas quando necessário: `focused` → `workspace` → `integration` → `global/checkpoint` → `delivery`. Recuperação técnica dentro do escopo continua automaticamente; mudanças de produto, escopo, custo material, permissão ou integridade experimental exigem decisão.
7. Nós no mesmo contexto usam spec inline e transição. Handoff/pacote de review existe somente para consumidor separado real. `assurance: light|full` preserva review independente; `none` fecha com verificação do executor.

No trabalho gerenciado pelo grafo, toda atualização mostra etapa, andamento, trabalho automático, pendências humanas e técnicas, bloqueios, próxima ação e caminhos inspecionáveis. `direct-trivial` e `vibe` retornam apenas um resumo curto da edição e do check; vibe sempre informa sua verificação focada aprovada.

## Perfis

| Perfil | Inclui | Melhor uso |
| --- | --- | --- |
| `core` | Entrega, grafo, status, review e validação | Maioria dos projetos |
| `core-learning` | `core` mais aprendizado opcional do projeto | Prática guiada e debriefings |
| `full` | `core-learning` mais o pacote separado de estudo do harness | Estudar a própria engenharia de harness |

O aprendizado nunca é ativado silenciosamente. O usuário escolhe o caminho Markdown, local do Obsidian, alvo/MCP do Notion ou outro destino exato antes da criação de qualquer nota.

## Projeto novo ou harness existente

Em um projeto vazio, a descoberta vem antes de propostas de stack, arquitetura, marca ou funcionalidades. Depois de entender a intenção do produto, o agente pergunta pela arquitetura e organização de pastas somente quando não consegue recuperá-las do contexto aprovado ou das evidências do projeto; convenções de código opcionais podem ser informadas, delegadas aos padrões normais da stack ou omitidas. Em um repositório maduro, o Kit preserva a estrutura comprovada e as instruções existentes; ele nunca sobrescreve nem reorganiza silenciosamente `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.claude/` ou outra autoridade. Veja o [playbook de adoção madura](harness/playbooks/mature-harness-adoption.md).

## Limites honestos

- O Kit não roda sem supervisão nem abre chats visíveis sozinho. Durante uma sessão ativa de orquestração, pode lançar subagentes/tasks internas compatíveis em paralelo; integração, deploy, publicação e criação de tasks visíveis continuam exigindo capacidade e autoridade próprias.
- Leases são contratos validados, não locks do sistema operacional.
- Threads, subagentes, worktrees, MCPs, rede e modelo dependem das capacidades e autorizações reais do host. Quando o roteamento automático está explicitamente aprovado e o host oferece overrides, o dispatch aplica modelo/raciocínio resolvidos e registra a confirmação do adaptador; caso contrário, a rota fica visivelmente manual ou bloqueada.
- Um grafo de conhecimento pode reduzir varreduras amplas, mas apenas consultas focadas e orçamentos de execução evitam desperdício; nenhuma ferramenta garante menos tokens. Consulte o [contrato de execução focada por grafo](docs/SCOPED-GRAPH-EXECUTION.md) para os limites de `read_set`, `write_set`, `impact_set`, proveniência e Graphify.

Quer aprofundar? Veja a [instalação passo a passo](docs/EMBEDDED-INSTALLATION.md), o [modo hackathon](docs/HACKATHON-MODE.md), a [arquitetura](docs/ARCHITECTURE.md), o [contrato de validação](docs/VALIDATION.md), a [auditoria de prontidão](docs/PUBLICATION-READINESS.md) e a [licença MIT](LICENSE).
