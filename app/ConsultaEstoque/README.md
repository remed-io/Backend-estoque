# 📊 API de Consulta de Estoque - Documentação

## Endpoints Implementados

### 1. **GET /consulta-estoque/resumo**
Retorna resumo geral do estoque com estatísticas principais.

**Resposta:**
```json
{
  "total_itens": 150,
  "total_produtos_diferentes": 45,
  "produtos_vencidos": 5,
  "produtos_proximo_vencimento": 12,
  "produtos_estoque_baixo": 8,
  "produtos_estoque_critico": 3,
  "valor_total_estoque": 15750.50
}
```

---

### 2. **GET /consulta-estoque/**
Consulta estoque com filtros avançados.

**Parâmetros Query:**
- `produto_nome`: Busca parcial no nome do produto
- `codigo_barras`: Filtro por código de barras exato
- `tipo_produto`: medicamento, cuidado_pessoal, suplemento_alimentar
- `fornecedor_id`: ID do fornecedor
- `armazem_id`: ID do armazém
- `vencidos`: true/false para produtos vencidos
- `dias_vencimento`: Produtos que vencem em X dias
- `estoque_baixo`: true/false para estoque baixo
- `estoque_critico`: true/false para estoque crítico
- `quantidade_min`: Quantidade mínima
- `quantidade_max`: Quantidade máxima
- `skip`: Paginação - pular registros
- `limit`: Limitar resultados (máx 1000)

**Exemplo:**
```
GET /consulta-estoque/?produto_nome=Paracetamol&dias_vencimento=30&limit=50
```

---

### 3. **GET /consulta-estoque/detalhado**
Consulta detalhada com resumo + itens filtrados.

**Mesmos parâmetros do endpoint anterior**

**Resposta:**
```json
{
  "resumo": { /* resumo geral */ },
  "itens": [ /* lista de itens filtrados */ ]
}
```

---

### 4. **GET /consulta-estoque/vencidos**
Produtos vencidos ou próximos do vencimento.

**Parâmetros:**
- `dias_limite`: Dias para vencimento (0 = já vencidos)

---

### 5. **GET /consulta-estoque/critico**
Itens com estoque crítico ou baixo.

---

### 6. **GET /consulta-estoque/por-produto/{produto_id}**
Estoque de um produto específico em todos os armazéns.

---

### 7. **GET /consulta-estoque/por-armazem/{armazem_id}**
Todos os itens de um armazém específico.

---

## 🎯 Status dos Produtos

- **VENCIDO**: Data de validade passou
- **PROXIMO_VENCIMENTO**: Vence em ≤ 30 dias
- **ESTOQUE_CRITICO**: Quantidade = 0
- **ESTOQUE_BAIXO**: Quantidade ≤ quantidade_mínima
- **NORMAL**: Situação regular

---

## 🔐 Autenticação

**Todos os endpoints requerem autenticação JWT.**

**Header obrigatório:**
```
Authorization: Bearer <token_jwt>
```

---

## 📝 Exemplo de Resposta Completa

```json
{
  "item_estoque_id": 1,
  "produto_id": 15,
  "produto_nome": "Paracetamol 500mg",
  "tipo_produto": "medicamento",
  "codigo_barras": "7891234567890",
  "preco": 12.50,
  "data_validade": "2025-12-31",
  "lote": "LOT123",
  "fornecedor_id": 3,
  "fornecedor_nome": "Farmacêutica ABC",
  "armazem_id": 1,
  "armazem_local": "Estoque Central",
  "quantidade_atual": 50,
  "quantidade_minima": 10,
  "status": "normal",
  "dias_para_vencimento": 175
}
```
