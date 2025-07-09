# 📊 Relatórios de Vencimento - H7

## ✅ **H7 — Relatório de Produtos Vencidos e Próximos do Vencimento COMPLETO**

### 🎯 Endpoints Implementados

#### 1. **GET /relatorios/vencimento/**
Relatório completo com filtros avançados.

**Parâmetros:**
- `dias_limite`: Dias para análise (0-365, padrão: 30)
- `incluir_vencidos`: Incluir já vencidos (padrão: true)
- `armazem_id`: Filtrar por armazém
- `fornecedor_id`: Filtrar por fornecedor  
- `tipo_produto`: medicamento, cuidado_pessoal, suplemento_alimentar
- `valor_minimo`: Valor mínimo para incluir
- `apenas_com_estoque`: Apenas itens com estoque > 0

---

#### 2. **GET /relatorios/vencimento/csv**
Exportação em CSV (download direto).

**Mesmos parâmetros do endpoint anterior**

**Resposta:** Arquivo CSV para download

---

#### 3. **GET /relatorios/vencimento/vencidos-hoje**
Produtos que vencem hoje (para alertas).

---

#### 4. **GET /relatorios/vencimento/criticos**
Produtos críticos (vencimento muito próximo).

**Parâmetros:**
- `dias_limite`: Dias para considerar crítico (0-7, padrão: 3)

---

#### 5. **GET /relatorios/vencimento/resumo-rapido**
Resumo para dashboard - próximos 7 dias.

---

#### 6. **GET /relatorios/vencimento/por-armazem/{armazem_id}**
Relatório específico de um armazém.

---

#### 7. **GET /relatorios/vencimento/por-fornecedor/{fornecedor_id}**
Relatório específico de um fornecedor.

---

## 📊 **Status de Vencimento**

- **VENCIDO**: Produto já passou da validade
- **CRITICO**: Vence em até 3 dias 🚨
- **ATENCAO**: Vence em até 15 dias ⚠️
- **NORMAL**: Vence em mais de 15 dias ✅

---

## 📈 **Resumo Detalhado**

Cada relatório inclui:

```json
{
  "resumo": {
    "total_itens_analisados": 150,
    "produtos_vencidos": 5,
    "produtos_vence_hoje": 2,
    "produtos_vence_amanha": 1,
    "produtos_vence_3_dias": 4,
    "produtos_vence_7_dias": 8,
    "produtos_vence_15_dias": 12,
    "produtos_vence_30_dias": 25,
    "valor_total_vencidos": 1250.50,
    "valor_total_criticos": 890.30,
    "valor_total_atencao": 2340.80
  }
}
```

---

## 🔐 **Segurança**
Todos os endpoints protegidos com JWT.

---

## 📝 **Exemplo de Item**

```json
{
  "item_estoque_id": 1,
  "produto_nome": "Paracetamol 500mg",
  "codigo_barras": "7891234567890",
  "lote": "LOT123",
  "data_validade": "2025-07-15",
  "dias_para_vencimento": 6,
  "status_vencimento": "critico",
  "quantidade_atual": 50,
  "valor_unitario": 12.50,
  "valor_total": 625.00,
  "fornecedor_nome": "Farmacêutica ABC",
  "armazem_nome": "Estoque Central"
}
```

---

## ✅ **Critérios de Aceitação Atendidos**

✅ Listagem de produtos com validade expirada  
✅ Produtos prestes a vencer em até X dias (configurável)  
✅ Parâmetro configurável para dias  
✅ Exportação em formato CSV  
✅ Filtros por armazém, fornecedor, tipo  
✅ Valores financeiros comprometidos  
✅ Status visual de criticidade

**❌ Nenhuma alteração no banco necessária** - usa dados existentes.
