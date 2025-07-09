# H8 - Relatório de Movimentações de Estoque

## Implementação Completa

Esta documentação descreve a implementação da História de Usuário H8 - **Relatório de Movimentações de Estoque**.

### Arquivos Criados/Modificados

#### 1. Schema (`schema_relatorio_movimentacao.py`)
- **FiltroRelatorioMovimentacao**: Filtros avançados para o relatório
- **MovimentacaoResumo**: Dados consolidados de cada movimentação
- **EstatisticasMovimentacao**: Estatísticas agregadas do período
- **RelatorioMovimentacao**: Schema principal do relatório
- **ExportConfig**: Configurações de exportação

#### 2. Service (`service_relatorio_movimentacao.py`)
- **gerar_relatorio()**: Geração completa do relatório com filtros
- **_aplicar_filtros()**: Aplicação de filtros na query
- **_converter_para_resumo()**: Conversão de modelo para schema
- **_calcular_estatisticas()**: Cálculo de estatísticas agregadas
- **exportar_csv()**: Exportação para formato CSV
- **obter_resumo_periodo()**: Resumo rápido para dashboards

#### 3. Routes (`routes_relatorio_movimentacao.py`)
- **GET /relatorios/movimentacoes/**: Relatório completo com filtros
- **GET /relatorios/movimentacoes/estatisticas**: Apenas estatísticas
- **GET /relatorios/movimentacoes/export/csv**: Exportação CSV
- **GET /relatorios/movimentacoes/por-produto/{produto_nome}**: Por produto
- **GET /relatorios/movimentacoes/por-armazem/{armazem_id}**: Por armazém
- **GET /relatorios/movimentacoes/por-funcionario/{funcionario_id}**: Por funcionário

#### 4. Main App (`main.py`)
- Adicionado import e registro do router de relatório de movimentações

### Funcionalidades Implementadas

#### Filtros Disponíveis
- **Período**: data_inicio e data_fim
- **Tipo**: entrada ou saida
- **Produto**: busca por nome (em todas as categorias)
- **Armazém**: filtro por ID do armazém
- **Funcionário**: filtro por responsável
- **Item**: filtro por item específico de estoque

#### Dados Retornados
- **ID da movimentação**
- **Data e hora**
- **Tipo** (entrada/saida)
- **Quantidade movimentada**
- **Dados do produto**: nome, lote, vencimento, preço
- **Dados do armazém**: ID e nome
- **Dados do funcionário**: ID e nome
- **Dados específicos de saída**: CPF comprador, nome comprador, receita digital

#### Estatísticas Calculadas
- Total de movimentações no período
- Quantidade de entradas vs saídas
- Quantidade total movimentada (entrada/saída)
- Valor total movimentado (entrada/saída)
- Período analisado

#### Exportação CSV
- Formato compatível com Excel/LibreOffice
- Inclui todas as movimentações detalhadas
- Adiciona estatísticas consolidadas no final
- Nome de arquivo baseado no período

### Endpoints de API

#### 1. Relatório Completo
```
GET /relatorios/movimentacoes/
```
**Parâmetros Query:**
- `data_inicio` (opcional): Data inicial (YYYY-MM-DD)
- `data_fim` (opcional): Data final (YYYY-MM-DD)
- `tipo` (opcional): entrada | saida
- `produto_nome` (opcional): Nome do produto (busca parcial)
- `armazem_id` (opcional): ID do armazém
- `funcionario_id` (opcional): ID do funcionário
- `item_id` (opcional): ID do item de estoque

#### 2. Estatísticas Resumidas
```
GET /relatorios/movimentacoes/estatisticas
```
**Parâmetros Query:**
- `data_inicio` (opcional): Data inicial
- `data_fim` (opcional): Data final

#### 3. Exportação CSV
```
GET /relatorios/movimentacoes/export/csv
```
**Parâmetros Query:** (mesmos do relatório completo)

#### 4. Relatórios Específicos
```
GET /relatorios/movimentacoes/por-produto/{produto_nome}
GET /relatorios/movimentacoes/por-armazem/{armazem_id}
GET /relatorios/movimentacoes/por-funcionario/{funcionario_id}
```

### Segurança
- **Autenticação obrigatória**: Todos os endpoints requerem JWT válido
- **Autorização**: Apenas funcionários autenticados podem acessar
- **Validação**: Filtros validados via Pydantic schemas

### Integração com Banco de Dados
- **Joins otimizados**: Uso de `joinedload` para evitar N+1 queries
- **Filtros eficientes**: Queries otimizadas com índices apropriados
- **Busca em múltiplas tabelas**: Produto pode estar em Medicamento, CuidadoPessoal ou SuplementoAlimentar

### Casos de Uso

#### 1. Auditoria Operacional
```python
# Movimentações de hoje
GET /relatorios/movimentacoes/?data_inicio=2024-01-15&data_fim=2024-01-15
```

#### 2. Análise por Funcionário
```python
# Performance de um funcionário
GET /relatorios/movimentacoes/por-funcionario/5?data_inicio=2024-01-01
```

#### 3. Controle de Armazém
```python
# Atividade do estoque central
GET /relatorios/movimentacoes/por-armazem/1?data_inicio=2024-01-01&data_fim=2024-01-31
```

#### 4. Rastreamento de Produto
```python
# Histórico de um medicamento
GET /relatorios/movimentacoes/por-produto/Paracetamol
```

#### 5. Relatório Gerencial
```python
# Exportar tudo do mês para Excel
GET /relatorios/movimentacoes/export/csv?data_inicio=2024-01-01&data_fim=2024-01-31
```

### Performance
- **Paginação**: Implementar se necessário para grandes volumes
- **Cache**: Considerar cache Redis para consultas frequentes
- **Índices**: Garantir índices em data, tipo, armazem_id, responsavel_id

### Status
✅ **História H8 - IMPLEMENTADA COMPLETAMENTE**

**Critérios de aceitação atendidos:**
- ✅ Relatório inclui data, tipo, quantidade, item de estoque e armazém
- ✅ Dados do produto (nome, lote) incluídos
- ✅ Dados do funcionário responsável incluídos
- ✅ Filtros avançados por período, tipo, produto, etc.
- ✅ Exportação CSV para análise externa
- ✅ Estatísticas consolidadas
- ✅ Autenticação obrigatória
