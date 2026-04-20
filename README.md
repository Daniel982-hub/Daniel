# 🎬 Gestor de Filmes e Séries

## 📌 Descrição
Sistema em Python que simula uma plataforma de streaming (tipo Netflix), permitindo gerir utilizadores, conteúdos e histórico de visualização.

## 🧱 Entidades

### Utilizador
| Campo | Descrição |
|---|---|
| idUtilizador | Gerado automaticamente (ex: U001) |
| nome | Nome do utilizador |
| email | Email |
| palavraPasse | Palavra-passe |
| tipoPlano | basic ou premium |
| estado | 1 = Ativo, 0 = Inativo |

### Conteúdo
| Campo | Descrição |
|---|---|
| idConteudo | Gerado automaticamente (ex: C001) |
| titulo | Título do filme/série |
| tipo | filme ou série |
| genero | Género (ação, drama, etc.) |
| anoLancamento | Ano de lançamento |
| classificacaoEtaria | Ex: M/6, M/12, M/16, M/18 |
| avaliacao | Nota de 0 a 10 |
| numeroAvaliadores | Nº de pessoas que avaliaram |
| duracao | Duração em minutos (filmes) |
| numeroTemporadas | Nº de temporadas (séries) |
| produtor | Nome do produtor |
| realizador | Nome do realizador |

### HistóricoVisualização
| Campo | Descrição |
|---|---|
| idHistorico | Gerado automaticamente (ex: H001) |
| idUtilizador | Referência ao utilizador |
| idConteudo | Referência ao conteúdo |
| dataVisualizacao | Data/hora automática da visualização |
| progresso | Progresso em % (0-100) |

## 📁 Estrutura do Projeto
```
projeto/
├── main.py          → Menu terminal, ponto de entrada, verifica códigos de retorno
├── utilizadores.py  → Dicionário + CRUD com returns (código HTTP, mensagem)
├── conteudo.py      → Dicionário + CRUD com returns (código HTTP, mensagem)
├── historico.py     → Dicionário + CRUD com returns (código HTTP, mensagem)
├── utils.py         → Contadores, geração de IDs e validações
└── README.md        → Documentação
```

## 🔁 Códigos HTTP usados
| Código | Significado |
|---|---|
| 200 | OK — operação bem sucedida |
| 201 | Created — recurso criado com sucesso |
| 400 | Bad Request — dados inválidos |
| 404 | Not Found — recurso não encontrado |
| 409 | Conflict — recurso já existe |
| 500 | Internal Error — erro inesperado |

## ⚙️ Funcionalidades
✔ CRUD completo de Utilizadores  
✔ CRUD completo de Conteúdos (filmes e séries)  
✔ CRUD completo de Histórico de Visualizações  
✔ IDs gerados automaticamente (U001, C001, H001, ...)  
✔ Data/hora de visualização preenchida automaticamente  
✔ Validação de todos os inputs  

## ▶️ Executar
```bash
python main.py
```

## 📝 Observações
- Os dados são guardados apenas em memória (sem base de dados).
- Cada módulo usa **dicionários** com o ID como chave.
- As funções retornam sempre um **tuplo** `(codigo_http, dados_ou_mensagem)`.
- O `utils.py` gere os contadores de IDs e as validações genéricas.
