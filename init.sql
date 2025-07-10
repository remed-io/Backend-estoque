-- Tabela armazem
CREATE TABLE armazem (
    id SERIAL PRIMARY KEY,
    local_armazem VARCHAR(100) NOT NULL UNIQUE,
    quantidade_minima INTEGER NOT NULL DEFAULT 0
);

-- Tabela subcategoria_cuidado_pessoal
CREATE TABLE subcategoria_cuidado_pessoal (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    descricao VARCHAR(255)
);

-- Tabela fornecedor
CREATE TABLE fornecedor (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cnpj VARCHAR(20) NOT NULL UNIQUE,
    contato VARCHAR(100)
);

-- Tabela funcionario
CREATE TABLE funcionario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    cargo VARCHAR(50) NOT NULL,
    data_contratacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabela restricao_alimentar
CREATE TABLE restricao_alimentar (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) UNIQUE NOT NULL
);

-- Tabela medicamento
CREATE TABLE medicamento (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(255),
    dosagem VARCHAR(50),
    principio_ativo VARCHAR(100),
    tarja VARCHAR(50),
    necessita_receita BOOLEAN NOT NULL DEFAULT FALSE,
    forma_farmaceutica VARCHAR(50),
    fabricante VARCHAR(100),
    registro_anvisa VARCHAR(50)
);

-- Tabela suplemento_alimentar
CREATE TABLE suplemento_alimentar (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(255),
    principio_ativo VARCHAR(100),
    sabor VARCHAR(50),
    peso_volume VARCHAR(20),
    fabricante VARCHAR(100),
    registro_anvisa VARCHAR(50)
);

-- Tabela cuidado_pessoal
CREATE TABLE cuidado_pessoal (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(255),
    subcategoria_id INT REFERENCES subcategoria_cuidado_pessoal(id),
    quantidade VARCHAR(20),
    volume VARCHAR(20),
    uso_recomendado VARCHAR(100),
    publico_alvo VARCHAR(50),
    fabricante VARCHAR(100)
);

-- Tabela item_estoque
CREATE TABLE item_estoque (
    id SERIAL PRIMARY KEY,
    codigo_barras VARCHAR(80) UNIQUE NOT NULL,
    fornecedor_id INT NOT NULL REFERENCES fornecedor(id),
    preco DECIMAL(10,2) NOT NULL,
    lote VARCHAR(50) NOT NULL,
    data_fabricacao DATE,
    data_validade DATE NOT NULL,
    produto_medicamento_id INT REFERENCES medicamento(id),
    produto_cuidado_pessoal_id INT REFERENCES cuidado_pessoal(id),
    produto_suplemento_alimentar_id INT REFERENCES suplemento_alimentar(id),
    tipo_produto VARCHAR(20) NOT NULL CHECK (tipo_produto IN ('medicamento', 'cuidado_pessoal', 'suplemento_alimentar')),
    produto_nome VARCHAR(100) NOT NULL,
    produto_id INT NOT NULL,

    CHECK (
        ((produto_medicamento_id IS NOT NULL)::int +
         (produto_cuidado_pessoal_id IS NOT NULL)::int +
         (produto_suplemento_alimentar_id IS NOT NULL)::int) = 1
    )
);

-- Tabela item_armazenado
CREATE TABLE item_armazenado (
    id SERIAL PRIMARY KEY,
    armazem_id INT NOT NULL REFERENCES armazem(id),
    item_estoque_id INT NOT NULL REFERENCES item_estoque(id),
    quantidade INT NOT NULL CHECK (quantidade >= 0),
    data_atualizacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (armazem_id, item_estoque_id)
);

-- Tabela movimentacao_estoque
CREATE TABLE movimentacao_estoque (
    id SERIAL PRIMARY KEY,
    item_estoque_id INT NOT NULL REFERENCES item_estoque(id),
    funcionario_id INT REFERENCES funcionario(id),
    data_movimentacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('entrada', 'saida')),
    quantidade INT NOT NULL CHECK (quantidade > 0),
    cpf_comprador VARCHAR(14),
    nome_comprador VARCHAR(100),
    receita_digital TEXT,
    armazem_id INT REFERENCES armazem(id)
);

-- Tabela restricao_suplemento
CREATE TABLE restricao_suplemento (
    suplemento_alimentar_id INT NOT NULL REFERENCES suplemento_alimentar(id),
    restricao_alimentar_id INT NOT NULL REFERENCES restricao_alimentar(id),
    severidade VARCHAR(20) CHECK (severidade IN ('leve', 'moderada', 'grave')),
    observacoes TEXT,
    PRIMARY KEY (suplemento_alimentar_id, restricao_alimentar_id)
);

-- Tabelas para Sistema de Alertas (H9)
CREATE TABLE IF NOT EXISTS alerta_estoque (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('estoque_critico', 'estoque_baixo', 'produto_vencido', 'proximo_vencimento', 'falta_produto')),
    prioridade VARCHAR(20) NOT NULL CHECK (prioridade IN ('baixa', 'media', 'alta', 'critica')),
    titulo VARCHAR(200) NOT NULL,
    descricao TEXT NOT NULL,
    item_estoque_id INTEGER NOT NULL REFERENCES item_estoque(id) ON DELETE CASCADE,
    armazem_id INTEGER NOT NULL REFERENCES armazem(id) ON DELETE CASCADE,
    quantidade_atual INTEGER NOT NULL DEFAULT 0,
    quantidade_minima INTEGER NOT NULL DEFAULT 0,
    valor_unitario DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    valor_total_impactado DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    dias_para_vencimento INTEGER,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_resolucao TIMESTAMP,
    resolvido BOOLEAN NOT NULL DEFAULT FALSE,
    observacoes TEXT,
    
    CONSTRAINT check_alerta_valores_positivos CHECK (
        quantidade_atual >= 0 AND 
        quantidade_minima >= 0 AND 
        valor_unitario >= 0 AND 
        valor_total_impactado >= 0
    )
);

CREATE TABLE IF NOT EXISTS notificacao_alerta (
    id SERIAL PRIMARY KEY,
    alerta_id INTEGER NOT NULL REFERENCES alerta_estoque(id) ON DELETE CASCADE,
    funcionario_id INTEGER REFERENCES funcionario(id) ON DELETE SET NULL,
    tipo_notificacao VARCHAR(20) NOT NULL CHECK (tipo_notificacao IN ('email', 'push', 'sms')),
    enviado BOOLEAN NOT NULL DEFAULT FALSE,
    data_envio TIMESTAMP,
    tentativas_envio INTEGER NOT NULL DEFAULT 0,
    erro_envio TEXT,
    
    CONSTRAINT check_tentativas_positivas CHECK (tentativas_envio >= 0)
);

CREATE TABLE IF NOT EXISTS configuracao_alertas (
    id SERIAL PRIMARY KEY,
    chave VARCHAR(100) NOT NULL UNIQUE,
    valor VARCHAR(500) NOT NULL,
    descricao TEXT,
    data_atualizacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Índices para performance dos alertas
CREATE INDEX IF NOT EXISTS idx_alerta_tipo_prioridade ON alerta_estoque(tipo, prioridade);
CREATE INDEX IF NOT EXISTS idx_alerta_resolvido ON alerta_estoque(resolvido);
CREATE INDEX IF NOT EXISTS idx_alerta_item_armazem ON alerta_estoque(item_estoque_id, armazem_id);
CREATE INDEX IF NOT EXISTS idx_alerta_data_criacao ON alerta_estoque(data_criacao DESC);
CREATE INDEX IF NOT EXISTS idx_alerta_dias_vencimento ON alerta_estoque(dias_para_vencimento) WHERE dias_para_vencimento IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_notificacao_alerta_id ON notificacao_alerta(alerta_id);
CREATE INDEX IF NOT EXISTS idx_notificacao_funcionario ON notificacao_alerta(funcionario_id);
CREATE INDEX IF NOT EXISTS idx_notificacao_enviado ON notificacao_alerta(enviado);

CREATE INDEX IF NOT EXISTS idx_config_chave ON configuracao_alertas(chave);

-- Configurações padrão do sistema de alertas
INSERT INTO configuracao_alertas (chave, valor, descricao) VALUES
('dias_vencimento_critico', '3', 'Dias para alerta crítico de vencimento'),
('dias_vencimento_atencao', '7', 'Dias para alerta de atenção sobre vencimento'),
('dias_vencimento_aviso', '30', 'Dias para aviso de vencimento próximo'),
('ativar_alertas_email', 'false', 'Enviar alertas por email'),
('ativar_alertas_push', 'true', 'Exibir alertas no sistema')
ON CONFLICT (chave) DO NOTHING;
