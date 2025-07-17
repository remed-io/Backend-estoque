# ReMed.io - Backend 🧪

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

## Guia de Testes no Swagger 📋

Para testar completamente a aplicação, siga esta ordem de cadastros no Swagger (`http://localhost:8000/docs`):

### 1. **Fornecedor** (Obrigatório primeiro)
```json
POST /fornecedores/
{
  "nome": "Laboratório ABC",
  "cnpj": "12345678000199",
  "contato": "(11) 99999-9999"
}
```

### 2. **Armazém** (Obrigatório)
```json
POST /armazens/
{
  "local_armazem": "Depósito Central",
  "quantidade_minima": 10
}
```

### 3. **Funcionário** (Obrigatório para movimentações)
```json
POST /funcionarios/
{
  "nome": "João Silva",
  "cpf": "12345678901",
  "email": "joao@farmacia.com",
  "cargo": "Farmacêutico",
  "senha": "senha123456"
}
```

### 4. **Produtos** (Escolha um ou mais tipos)

#### 4.1. Medicamento
```json
POST /medicamentos/
{
  "nome": "Paracetamol 500mg",
  "descricao": "Analgésico e antitérmico",
  "dosagem": "500mg",
  "principio_ativo": "Paracetamol",
  "tarja": "Sem tarja",
  "necessita_receita": false,
  "forma_farmaceutica": "Comprimido",
  "fabricante": "Laboratório ABC",
  "registro_anvisa": "1234567890"
}
```

#### 4.2. Subcategoria de Cuidado Pessoal (necessária antes do produto)
```json
POST /subcategorias-cuidado-pessoal/
{
  "nome": "Higiene Bucal",
  "descricao": "Produtos para cuidado dos dentes e boca"
}
```

#### 4.3. Cuidado Pessoal
```json
POST /cuidados-pessoais/
{
  "nome": "Creme Dental Mentolado",
  "descricao": "Pasta de dente com mentol",
  "subcategoria_id": 1,
  "quantidade": "90g",
  "volume": "90ml",
  "uso_recomendado": "Escovar 3x ao dia",
  "publico_alvo": "Adultos",
  "fabricante": "Higiene Total"
}
```

#### 4.4. Suplemento Alimentar
```json
POST /suplementos-alimentares/
{
  "nome": "Vitamina C 1000mg",
  "descricao": "Suplemento de vitamina C",
  "principio_ativo": "Ácido Ascórbico",
  "sabor": "Laranja",
  "peso_volume": "60 cápsulas",
  "fabricante": "NutriVida",
  "registro_anvisa": "9876543210"
}
```

### 5. **Item Estoque** (Vincular produto ao estoque)

#### Para Medicamento:
```json
POST /itens-estoque/
{
  "codigo_barras": "7891234567890",
  "preco": 15.90,
  "data_validade": "2026-12-31T00:00:00",
  "fornecedor_id": 1,
  "lote": "LOT001",
  "produto_medicamento_id": 1,
  "produto_cuidado_pessoal_id": null,
  "produto_suplemento_alimentar_id": null
}
```

#### Para Cuidado Pessoal:
```json
POST /itens-estoque/
{
  "codigo_barras": "7891234567891",
  "preco": 8.50,
  "data_validade": "2027-06-30T00:00:00",
  "fornecedor_id": 1,
  "lote": "LOT002",
  "produto_medicamento_id": null,
  "produto_cuidado_pessoal_id": 1,
  "produto_suplemento_alimentar_id": null
}
```

#### Para Suplemento:
```json
POST /itens-estoque/
{
  "codigo_barras": "7891234567892",
  "preco": 35.00,
  "data_validade": "2025-08-15T00:00:00",
  "fornecedor_id": 1,
  "lote": "LOT003",
  "produto_medicamento_id": null,
  "produto_cuidado_pessoal_id": null,
  "produto_suplemento_alimentar_id": 1
}
```

### 6. **Item Armazenado** (Adicionar produtos ao armazém)
```json
POST /itens-armazenados/
{
  "armazem_id": 1,
  "item_estoque_id": 1,
  "quantidade": 100
}
```

### 7. **Movimentação de Estoque**

#### Entrada:
```json
POST /movimentacoes-estoque/
{
  "data_movimentacao": "2025-01-15T10:00:00",
  "tipo": "entrada",
  "quantidade": 50,
  "item_estoque_id": 1,
  "funcionario_id": 1,
  "armazem_id": 1
}
```

#### Saída (Venda):
```json
POST /movimentacoes-estoque/
{
  "data_movimentacao": "2025-01-15T14:30:00",
  "tipo": "saida",
  "quantidade": 2,
  "item_estoque_id": 1,
  "funcionario_id": 1,
  "cpf_comprador": "98765432100",
  "nome_comprador": "Maria Santos",
  "receita_digital": "REC123456789",
  "armazem_id": 1
}
```

### 8. **Restrições Alimentares** (Para Suplementos)

#### Criar Restrição:
```json
POST /restricoes-alimentares/
{
  "nome": "Intolerância à Lactose"
}
```

#### Vincular Suplemento à Restrição:
```json
POST /restricoes-suplementos/
{
  "suplemento_alimentar_id": 1,
  "restricao_alimentar_id": 1,
  "severidade": "Moderada",
  "observacoes": "Pode causar desconforto intestinal"
}
```

### 9. **Consultas Úteis**

#### Consultar Estoque Atual:
- `GET /consulta-estoque/` - Lista todos os itens em estoque
- `GET /consulta-estoque/baixo-estoque` - Itens com estoque baixo
- `GET /consulta-estoque/vencimento-proximo` - Itens próximos ao vencimento

#### Relatórios:
- `GET /relatorios/vendas` - Relatório de vendas
- `GET /relatorios/estoque` - Relatório de estoque
- `GET /relatorios/movimentacoes` - Relatório de movimentações

### 📝 **Dicas Importantes:**

1. **Ordem de Cadastro**: Sempre cadastre na ordem apresentada, pois existem dependências entre as entidades
2. **IDs**: Anote os IDs retornados para usar nos próximos cadastros
3. **Validações**: Observe as validações específicas (ex: CPF deve ter 11 dígitos, CNPJ deve ser válido)
4. **Movimentações de Saída**: Sempre incluir CPF, nome do comprador e receita digital
5. **Data/Hora**: Use o formato ISO 8601 (`YYYY-MM-DDTHH:MM:SS`)

### 🔍 **Testando Cenários Completos:**

1. **Fluxo de Entrada**: Fornecedor → Produto → Item Estoque → Item Armazenado → Movimentação Entrada
2. **Fluxo de Venda**: Consultar Estoque → Movimentação Saída → Verificar Estoque Atualizado
3. **Alertas**: Cadastrar com quantidade mínima → Fazer várias saídas → Verificar alertas de estoque baixo

---

## Licença

MIT