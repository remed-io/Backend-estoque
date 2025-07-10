from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional

from app.settings import get_db
from app.security import get_current_user
from app.Funcionario.model_funcionario import Funcionario

from .schema_alertas import (
    AlertaEstoque,
    AlertaCritico,
    ResumoAlertas,
    FiltroAlertas,
    RelatorioAlertas,
    TipoAlerta,
    PrioridadeAlerta
)
from .service_alertas import service_alertas

router = APIRouter(
    prefix="/alertas",
    tags=["Alertas de Estoque"]
)

@router.get("/verificar", response_model=List[AlertaEstoque])
def verificar_alertas(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    usuario: Funcionario = Depends(get_current_user)
):
    """
    Verifica e gera todos os alertas do sistema.
    
    Esta operação pode ser executada em background para não bloquear a interface.
    """
    # Executar verificação em background para performance
    background_tasks.add_task(service_alertas.verificar_todos_alertas, db)
    
    # Retornar alertas existentes imediatamente
    filtros = FiltroAlertas(apenas_nao_resolvidos=True)
    return service_alertas.obter_alertas(db, filtros)

@router.get("/resumo", response_model=ResumoAlertas)
def obter_resumo_alertas(
    db: Session = Depends(get_db),
    usuario: Funcionario = Depends(get_current_user)
):
    """
    Obtém resumo estatístico dos alertas do sistema.
    
    Ideal para dashboards e visões gerais.
    """
    return service_alertas.gerar_resumo_alertas(db)

@router.get("/criticos", response_model=List[AlertaCritico])
def obter_alertas_criticos(
    limite: int = Query(10, description="Número máximo de alertas críticos", ge=1, le=50),
    db: Session = Depends(get_db),
    usuario: Funcionario = Depends(get_current_user)
):
    """
    Obtém os alertas mais críticos do sistema.
    
    Retorna alertas que requerem ação imediata.
    """
    return service_alertas.obter_alertas_criticos(db, limite)

@router.get("/", response_model=List[AlertaEstoque])
def listar_alertas(
    tipo: Optional[TipoAlerta] = Query(None, description="Filtrar por tipo de alerta"),
    prioridade: Optional[PrioridadeAlerta] = Query(None, description="Filtrar por prioridade"),
    armazem_id: Optional[int] = Query(None, description="Filtrar por armazém"),
    apenas_nao_resolvidos: bool = Query(True, description="Apenas alertas não resolvidos"),
    dias_vencimento_max: Optional[int] = Query(None, description="Máximo de dias para vencimento"),
    db: Session = Depends(get_db),
    usuario: Funcionario = Depends(get_current_user)
):
    """
    Lista alertas com filtros opcionais.
    
    Permite busca detalhada e filtrada dos alertas.
    """
    filtros = FiltroAlertas(
        tipo=tipo,
        prioridade=prioridade,
        armazem_id=armazem_id,
        apenas_nao_resolvidos=apenas_nao_resolvidos,
        dias_vencimento_max=dias_vencimento_max
    )
    
    return service_alertas.obter_alertas(db, filtros)

@router.get("/relatorio", response_model=RelatorioAlertas)
def gerar_relatorio_completo(
    tipo: Optional[TipoAlerta] = Query(None, description="Filtrar por tipo de alerta"),
    prioridade: Optional[PrioridadeAlerta] = Query(None, description="Filtrar por prioridade"),
    armazem_id: Optional[int] = Query(None, description="Filtrar por armazém"),
    apenas_nao_resolvidos: bool = Query(True, description="Apenas alertas não resolvidos"),
    db: Session = Depends(get_db),
    usuario: Funcionario = Depends(get_current_user)
):
    """
    Gera relatório completo de alertas.
    
    Inclui resumo estatístico, alertas críticos e lista completa filtrada.
    """
    filtros = FiltroAlertas(
        tipo=tipo,
        prioridade=prioridade,
        armazem_id=armazem_id,
        apenas_nao_resolvidos=apenas_nao_resolvidos
    )
    
    resumo = service_alertas.gerar_resumo_alertas(db)
    alertas_criticos = service_alertas.obter_alertas_criticos(db, 20)
    alertas_completos = service_alertas.obter_alertas(db, filtros)
    
    return RelatorioAlertas(
        resumo=resumo,
        alertas_criticos=alertas_criticos,
        alertas_completos=alertas_completos,
        filtros_aplicados=filtros
    )

@router.put("/{alerta_id}/resolver")
def resolver_alerta(
    alerta_id: int,
    observacoes: Optional[str] = Query(None, description="Observações sobre a resolução"),
    db: Session = Depends(get_db),
    usuario: Funcionario = Depends(get_current_user)
):
    """
    Marca um alerta como resolvido.
    
    Adiciona data de resolução e observações opcionais.
    """
    sucesso = service_alertas.resolver_alerta(db, alerta_id, observacoes)
    
    if not sucesso:
        raise HTTPException(status_code=404, detail="Alerta não encontrado")
    
    return {"message": "Alerta marcado como resolvido", "alerta_id": alerta_id}

@router.post("/atualizar-todos")
def atualizar_todos_alertas(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    usuario: Funcionario = Depends(get_current_user)
):
    """
    Força atualização completa de todos os alertas do sistema.
    
    Operação executada em background para não bloquear a interface.
    Útil para executar verificações manuais ou em schedules.
    """
    background_tasks.add_task(service_alertas.verificar_todos_alertas, db)
    
    return {
        "message": "Verificação de alertas iniciada em background",
        "status": "processando"
    }

@router.get("/dashboard", response_model=dict)
def obter_dados_dashboard(
    db: Session = Depends(get_db),
    usuario: Funcionario = Depends(get_current_user)
):
    """
    Obtém dados consolidados para dashboard de alertas.
    
    Combina resumo + alertas críticos em uma única resposta otimizada.
    """
    resumo = service_alertas.gerar_resumo_alertas(db)
    alertas_criticos = service_alertas.obter_alertas_criticos(db, 5)
    
    return {
        "resumo": resumo,
        "alertas_criticos": alertas_criticos,
        "timestamp": resumo.ultima_atualizacao
    }

@router.get("/por-tipo/{tipo}", response_model=List[AlertaEstoque])
def obter_alertas_por_tipo(
    tipo: TipoAlerta,
    armazem_id: Optional[int] = Query(None, description="Filtrar por armazém"),
    db: Session = Depends(get_db),
    usuario: Funcionario = Depends(get_current_user)
):
    """
    Obtém alertas de um tipo específico.
    
    Útil para views especializadas (ex: só produtos vencidos).
    """
    filtros = FiltroAlertas(
        tipo=tipo,
        armazem_id=armazem_id,
        apenas_nao_resolvidos=True
    )
    
    return service_alertas.obter_alertas(db, filtros)

@router.get("/por-armazem/{armazem_id}", response_model=List[AlertaEstoque])
def obter_alertas_por_armazem(
    armazem_id: int,
    tipo: Optional[TipoAlerta] = Query(None, description="Filtrar por tipo de alerta"),
    prioridade: Optional[PrioridadeAlerta] = Query(None, description="Filtrar por prioridade"),
    db: Session = Depends(get_db),
    usuario: Funcionario = Depends(get_current_user)
):
    """
    Obtém alertas de um armazém específico.
    
    Útil para gestão localizada de estoque.
    """
    filtros = FiltroAlertas(
        tipo=tipo,
        prioridade=prioridade,
        armazem_id=armazem_id,
        apenas_nao_resolvidos=True
    )
    
    return service_alertas.obter_alertas(db, filtros)
