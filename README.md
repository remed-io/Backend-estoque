# Temed.io - Backend 💊

API de gerenciamento de estoque para farmácias, desenvolvida em **FastAPI** e **PostgreSQL**.  
Permite o cadastro, consulta e movimentação de medicamentos, suplementos alimentares e produtos de cuidado pessoal, com controle de fornecedores, armazéns e rastreabilidade de estoque.

---

## Tecnologias Utilizadas

- Python 3.11+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker & Docker Compose
- Pytest

---

## Como rodar o projeto

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/remed-io/Backend-estoque.git
   cd Backend-estoque
   ```

2. **Suba o ambiente com Docker Compose:**
   ```bash
   docker-compose up --build
   ```
   O backend estará disponível em [http://localhost:8000](http://localhost:8000).

3. **Acesse a documentação automática da API:**
   - [Swagger UI](http://localhost:8000/docs)
   - [ReDoc](http://localhost:8000/redoc)

---

## Estrutura de Pastas

- `app/` — Código principal da aplicação. Cada classe de domínio (ex: Medicamento, Fornecedor, ItemEstoque, etc.) possui seu próprio diretório, contendo:
  - `model_*.py`: Modelos SQLAlchemy
  - `schema_*.py`: Schemas Pydantic
  - `service_*.py`: Lógica de negócio
  - `routes_*.py`: Endpoints da API
  - `test_*.py`: Testes automatizados referentes àquela classe
- `init.sql` — Script de criação do banco de dados
- `docker-compose.yml` — Orquestração dos serviços
- `Dockerfile` — Build da imagem do backend

---

## Testes

Os testes automatizados de cada classe estão localizados dentro do respectivo diretório em `app/`. Para rodar todos os testes, utilize:
```bash
pytest app/
```

---

## Documentação

A documentação completa do projeto está disponível no repositório [Docs](https://github.com/remed-io/Docs).

---

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature/fix: `git checkout -b feat/nome-da-feature`
3. Commit suas alterações: `git commit -m 'feat: minha nova feature'`
4. Push para o seu fork: `git push origin feat/nome-da-feature`
5. Abra um Pull Request

---

## Licença

MIT