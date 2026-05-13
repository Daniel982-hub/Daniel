# Gestor de Streaming

Sistema de gestão de uma plataforma de streaming desenvolvido em Python.  
Permite gerir utilizadores, conteúdos, histórico de visualizações, favoritos e recomendações.

---

## Estrutura do Projeto

```
├── main.py                   # Ponto de entrada — menu interativo no terminal
├── utils.py                  # Funções auxiliares (geração de IDs, validações)
├── utilizadores.py           # CRUD de Utilizadores
├── conteudo.py               # CRUD de Conteúdos (filmes e séries)
├── historico.py              # CRUD de Histórico de Visualizações
├── favoritos.py              # CRUD de Favoritos
├── recomendacoes.py          # CRUD de Recomendações
└── recomendacoes_server.py   # Gera recomendações automáticas a cada 10 segundos
```

---

## Como Executar

### Terminal 1 — menu interativo
```bash
python main.py
```

### Terminal 2 — recomendações automáticas
```bash
python recomendacoes_server.py
```

---

## Persistência de Dados

Cada módulo guarda os seus dados num ficheiro JSON criado automaticamente na mesma pasta:

| Ficheiro | Dados |
|----------|-------|
| `utilizadores.json` | Utilizadores |
| `conteudos.json` | Conteúdos |
| `historico.json` | Histórico de visualizações |
| `favoritos.json` | Favoritos |
| `recomendacoes.json` | Recomendações |

Todas as operações chamam `carregar()` no início e `guardar()` antes de retornar, garantindo que os dados persistem entre sessões.

---

## Convenção de Retorno

Todas as funções retornam um tuplo `(codigo_http, dados)` onde `dados` é sempre o **ID** do registo afetado:

| Operação | Código | Retorno |
|----------|--------|---------|
| Criar | 201 | ID do registo criado |
| Obter | 200 | ID do registo |
| Atualizar | 200 | ID do registo atualizado |
| Remover | 200 | ID do registo removido |
| Listar todos | 200 | Dicionário completo |
| Listar por utilizador | 200 | Lista de IDs |
| Erro | 400/404/409/500 | Mensagem de erro |

---

## Entidades

### Utilizador
| Campo | Tipo | Descrição |
|-------|------|-----------|
| idUtilizador | str | Identificador único (ex: U001) |
| nome | str | Nome do utilizador |
| email | str | Email (único) |
| palavraPasse | str | Palavra-passe |
| tipoPlano | str | `basic` ou `premium` |
| estado | int | `1` = ativo, `0` = inativo |

### Conteúdo
| Campo | Tipo | Descrição |
|-------|------|-----------|
| idConteudo | str | Identificador único (ex: C001) |
| titulo | str | Título do conteúdo |
| tipo | str | `filme` ou `serie` |
| genero | str | Género (ex: Drama, Ação) |
| anoLancamento | int | Ano de lançamento |
| classificacaoEtaria | str | Ex: M/12, M/18 |
| avaliacao | float | 0.0 a 10.0 |
| numeroAvaliadores | int | Número de avaliadores |
| duracao | int | Duração em minutos (filmes) |
| numeroTemporadas | int | Número de temporadas (séries) |
| produtor | str | Nome do produtor |
| realizador | str | Nome do realizador |

### Histórico de Visualizações
| Campo | Tipo | Descrição |
|-------|------|-----------|
| idHistorico | str | Identificador único (ex: H001) |
| idUtilizador | str | Referência ao utilizador |
| idConteudo | str | Referência ao conteúdo |
| dataVisualizacao | str | Data e hora da visualização |
| progresso | float | 0.0 a 100.0 (%) |

### Favoritos
| Campo | Tipo | Descrição |
|-------|------|-----------|
| idFavorito | str | Identificador único (ex: F001) |
| idUtilizador | str | Referência ao utilizador |
| lista_ids_Conteudo | list | Lista de IDs de conteúdos favoritos |
| data_criacao | str | Data de criação |
| data_atualizacao | str | Data da última atualização |

### Recomendação
| Campo | Tipo | Descrição |
|-------|------|-----------|
| idRecomendacao | str | Identificador único (ex: R001) |
| idUtilizador | str | Referência ao utilizador |
| idConteudo | str | Conteúdo recomendado |
| dataGeracao | str | Data e hora de geração |
| scoreRelevancia | float | 0.0 a 10.0 |
| motivo | str | Motivo da recomendação |

---

## Recomendações Automáticas

O `recomendacoes_server.py` corre num terminal separado e a cada **10 segundos** gera automaticamente uma recomendação para cada utilizador com base nos seus favoritos:

1. Se o utilizador tiver **favoritos**, recomenda um conteúdo do mesmo género que ainda não está na lista.
2. Se **não tiver favoritos**, recomenda o conteúdo com maior avaliação global.

Exemplo do output no terminal:
```
Servidor de recomendacoes iniciado — gera a cada 10 segundos. CTRL+C para parar.

[14:23:01] U001 -> R001 (Baseado nos seus favoritos (Drama))
[14:23:01] U002 -> R002 (Mais popular da plataforma)
```

---

## Códigos de Retorno

| Código | Significado |
|--------|-------------|
| 200 | OK — operação bem sucedida |
| 201 | Created — recurso criado |
| 400 | Bad Request — dados inválidos |
| 404 | Not Found — recurso não encontrado |
| 409 | Conflict — recurso já existe |
| 500 | Internal Server Error |
