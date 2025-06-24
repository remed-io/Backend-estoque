-- Tabela Armazem
CREATE TABLE Armazem (
    id SERIAL PRIMARY KEY,
    local_armazem VARCHAR(100) NOT NULL
);

-- Tabela SubcategoriaCuidadoPessoal
CREATE TABLE SubcategoriaCuidadoPessoal (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    descricao VARCHAR(255)
);

-- Tabela Fornecedor
CREATE TABLE Fornecedor (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cnpj VARCHAR(20) NOT NULL UNIQUE,
    contato VARCHAR(100)
);

-- Tabela Funcionario
CREATE TABLE Funcionario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    cargo VARCHAR(50) NOT NULL,
    data_contratacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabela Restricao
CREATE TABLE Restricao (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) UNIQUE NOT NULL
);

-- Tabela Medicamento
CREATE TABLE Medicamento (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(255),
    principio_ativo VARCHAR(100),
    tarja VARCHAR(50),
    restricoes TEXT,
    fabricante VARCHAR(100),
    registro_anvisa VARCHAR(50)
);

-- Tabela SuplementoAlimentar
CREATE TABLE SuplementoAlimentar (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(255),
    principio_ativo VARCHAR(100),
    restricoes TEXT,
    fabricante VARCHAR(100),
    registro_anvisa VARCHAR(50)
);

-- Tabela CuidadoPessoal
CREATE TABLE CuidadoPessoal (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(255),
    subcategoria_id INT REFERENCES SubcategoriaCuidadoPessoal(id),
    forma VARCHAR(50),
    quantidade VARCHAR(20),
    volume VARCHAR(20),
    uso_recomendado VARCHAR(100),
    publico_alvo VARCHAR(50),
    fabricante VARCHAR(100)
);

-- Tabela ItemEstoque
CREATE TABLE ItemEstoque (
    id SERIAL PRIMARY KEY,
    codigo_barras VARCHAR(80) UNIQUE NOT NULL,
    fornecedor_id INT NOT NULL REFERENCES Fornecedor(id),
    medicamento_id INT REFERENCES Medicamento(id),
    cuidado_pessoal_id INT REFERENCES CuidadoPessoal(id),
    suplemento_alimentar_id INT REFERENCES SuplementoAlimentar(id),
    preco DECIMAL(10,2) NOT NULL,
    validade DATE NOT NULL,
    lote VARCHAR(50) NOT NULL,
    data_fabricacao DATE,
    CHECK (
        ((medicamento_id IS NOT NULL)::int +
         (cuidado_pessoal_id IS NOT NULL)::int +
         (suplemento_alimentar_id IS NOT NULL)::int) = 1
    )
);

-- Tabela ItemArmazenado
CREATE TABLE ItemArmazenado (
    id SERIAL PRIMARY KEY,
    armazem_id INT NOT NULL REFERENCES Armazem(id),
    item_estoque_id INT NOT NULL REFERENCES ItemEstoque(id),
    quantidade INT NOT NULL CHECK (quantidade >= 0),
    data_atualizacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (armazem_id, item_estoque_id)
);

-- Tabela MovimentacaoEstoque
CREATE TABLE MovimentacaoEstoque (
    id SERIAL PRIMARY KEY,
    item_estoque_id INT NOT NULL REFERENCES ItemEstoque(id),
    funcionario_id INT REFERENCES Funcionario(id),
    data TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('entrada', 'saida')),
    quantidade INT NOT NULL CHECK (quantidade > 0),
    cpf_comprador VARCHAR(14),
    nome_comprador VARCHAR(100),
    receita_digital TEXT,
    observacoes TEXT
);

-- Tabela RestricaoSuplemento
CREATE TABLE RestricaoSuplemento (
    suplemento_alimentar_id INT NOT NULL REFERENCES SuplementoAlimentar(id),
    restricao_id INT NOT NULL REFERENCES Restricao(id),
    severidade VARCHAR(20) CHECK (severidade IN ('leve', 'moderada', 'grave')),
    observacoes TEXT,
    PRIMARY KEY (suplemento_alimentar_id, restricao_id)
);

-- Índices para performance
CREATE INDEX idx_item_armazenado ON ItemArmazenado(armazem_id, item_estoque_id);
CREATE INDEX idx_item_estoque_produto ON ItemEstoque(medicamento_id, cuidado_pessoal_id, suplemento_alimentar_id);
CREATE INDEX idx_movimentacao_estoque ON MovimentacaoEstoque(item_estoque_id, data);
CREATE INDEX idx_restricao_suplemento ON RestricaoSuplemento(suplemento_alimentar_id);
