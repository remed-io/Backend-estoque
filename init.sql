-- Tabela armazem
CREATE TABLE armazem (
    id SERIAL PRIMARY KEY,
    local_armazem VARCHAR(100) NOT NULL UNIQUE
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
    observacoes TEXT
);

-- Tabela restricao_suplemento
CREATE TABLE restricao_suplemento (
    suplemento_alimentar_id INT NOT NULL REFERENCES suplemento_alimentar(id),
    restricao_alimentar_id INT NOT NULL REFERENCES restricao_alimentar(id),
    severidade VARCHAR(20) CHECK (severidade IN ('leve', 'moderada', 'grave')),
    observacoes TEXT,
    PRIMARY KEY (suplemento_alimentar_id, restricao_alimentar_id)
);

-- Índices para performance
CREATE INDEX idx_item_armazenado ON item_armazenado(armazem_id, item_estoque_id);
CREATE INDEX idx_item_estoque_produto ON item_estoque(produto_medicamento_id, produto_cuidado_pessoal_id, produto_suplemento_alimentar_id);
CREATE INDEX idx_movimentacao_estoque ON movimentacao_estoque(item_estoque_id, data_movimentacao);
CREATE INDEX idx_restricao_suplemento ON restricao_suplemento(suplemento_alimentar_id);
