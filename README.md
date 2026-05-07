# Gestor de Streaming

Sistema de gestão de uma plataforma de streaming desenvolvido em Python.  
Permite gerir utilizadores, conteúdos, histórico de visualizações, favoritos e recomendações.

---

## Estrutura do Projeto

```
src/
├── main.py                   # Ponto de entrada — menu interativo no terminal
├── utils.py                  # Funções auxiliares (geração de IDs, validações)
├── utilizadores.py           # CRUD de Utilizadores
├── conteudo.py               # CRUD de Conteúdos (filmes e séries)
├── historico.py              # CRUD de Histórico de Visualizações
├── favoritos.py              # CRUD de Favoritos
├── recomendacoes.py          # CRUD de Recomendações + geração automática diária
└── recomendacoes_server.py   # Servidor HTTP para as Recomendações (porta 8001)
```

---

## Como Executar

### Terminal principal (menu interativo)
```bash
python main.py
```

### Servidor HTTP de Recomendações (terminal separado)
```bash
python recomendacoes_server.py
```

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

## Servidor HTTP — Recomendações

Base URL: `http://localhost:8001`

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/recomendacoes` | Lista todas as recomendações |
| GET | `/recomendacoes/<rid>` | Obtém uma recomendação por ID |
| GET | `/recomendacoes/utilizador/<uid>` | Recomendações de um utilizador |
| POST | `/recomendacoes` | Cria recomendação manual |
| POST | `/recomendacoes/diarias` | Gera recomendações diárias automáticas |
| PUT | `/recomendacoes/<rid>` | Atualiza uma recomendação |
| DELETE | `/recomendacoes/<rid>` | Remove uma recomendação |

### Lógica de Recomendação Automática
O endpoint `POST /recomendacoes/diarias` percorre todos os utilizadores e para cada um:
1. Verifica se já recebeu uma recomendação hoje — se sim, ignora.
2. Se tiver **favoritos**, recomenda um conteúdo do mesmo género que ainda não está nos favoritos.
3. Se **não tiver favoritos**, recomenda o conteúdo com maior avaliação global.

### Exemplos de Pedidos

**Criar recomendação manual:**
```json
POST /recomendacoes
{
  "idUtilizador": "U001",
  "idConteudo": "C002",
  "motivo": "Escolha do editor"
}
```

**Atualizar recomendação:**
```json
PUT /recomendacoes/R001
{
  "motivo": "Tendencia popular",
  "scoreRelevancia": 9.0
}
```

---

## Códigos HTTP Utilizados

| Código | Significado |
|--------|-------------|
| 200 | OK — operação bem sucedida |
| 201 | Created — recurso criado |
| 400 | Bad Request — dados inválidos |
| 404 | Not Found — recurso não encontrado |
| 409 | Conflict — recurso já existe |
| 500 | Internal Server Error |
