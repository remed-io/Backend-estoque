"""
Testes para o sistema de alertas de estoque crítico (H9).
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from decimal import Decimal

from app.main import app
from app.security import create_access_token
from app.Alertas.service_alertas import AlertaService

client = TestClient(app)

# Token de teste para autenticação
test_token = create_access_token(data={"sub": "test@example.com"})
headers = {"Authorization": f"Bearer {test_token}"}


class TestAlertasEndpoints:
    """Testes para endpoints de alertas."""
    
    def test_get_dashboard_alertas(self):
        """Testa o endpoint de dashboard de alertas."""
        response = client.get("/alertas/dashboard", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert "resumo" in data
        assert "alertas_ativos" in data
        assert "grafico_prioridades" in data
        
        # Verifica estrutura do resumo
        resumo = data["resumo"]
        assert "total_alertas" in resumo
        assert "alertas_criticos" in resumo
        assert "alertas_altos" in resumo
        assert "produtos_em_falta" in resumo
        
    def test_get_alertas_ativos(self):
        """Testa listagem de alertas ativos."""
        response = client.get("/alertas/ativos", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        
    def test_get_alertas_resolvidos(self):
        """Testa listagem de alertas resolvidos."""
        response = client.get("/alertas/resolvidos", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        
    def test_get_configuracoes_alertas(self):
        """Testa obtenção de configurações de alertas."""
        response = client.get("/alertas/configuracoes", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
        
    def test_update_configuracoes_alertas(self):
        """Testa atualização de configurações de alertas."""
        config_data = {
            "dias_vencimento_critico": "5",
            "dias_vencimento_atencao": "10",
            "ativar_alertas_email": "true"
        }
        
        response = client.put(
            "/alertas/configuracoes",
            json=config_data,
            headers=headers
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "Configurações atualizadas com sucesso"
        
    def test_verificar_alertas_criticos(self):
        """Testa verificação manual de alertas críticos."""
        response = client.post("/alertas/verificar-criticos", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert "alertas_criados" in data
        assert "alertas_atualizados" in data
        
    def test_resolver_alerta(self):
        """Testa resolução de um alerta."""
        # Primeiro cria alertas para ter algo para resolver
        client.post("/alertas/verificar-criticos", headers=headers)
        
        # Pega o primeiro alerta ativo
        response = client.get("/alertas/ativos", headers=headers)
        alertas = response.json()
        
        if alertas:
            alerta_id = alertas[0]["id"]
            
            resolve_data = {
                "observacoes": "Alerta resolvido manualmente nos testes"
            }
            
            response = client.put(
                f"/alertas/{alerta_id}/resolver",
                json=resolve_data,
                headers=headers
            )
            assert response.status_code == 200
            
            data = response.json()
            assert data["message"] == "Alerta resolvido com sucesso"
            
    def test_filtros_alertas(self):
        """Testa filtros nos endpoints de alertas."""
        # Teste com filtro de tipo
        response = client.get(
            "/alertas/ativos?tipo=estoque_critico",
            headers=headers
        )
        assert response.status_code == 200
        
        # Teste com filtro de prioridade
        response = client.get(
            "/alertas/ativos?prioridade=critica",
            headers=headers
        )
        assert response.status_code == 200
        
        # Teste com filtro de armazém
        response = client.get(
            "/alertas/ativos?armazem_id=1",
            headers=headers
        )
        assert response.status_code == 200
        
    def test_relatorio_alertas(self):
        """Testa geração de relatório de alertas."""
        response = client.get("/alertas/relatorio", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert "periodo" in data
        assert "estatisticas" in data
        assert "historico_alertas" in data
        
    def test_unauthorized_access(self):
        """Testa acesso sem autenticação."""
        response = client.get("/alertas/dashboard")
        assert response.status_code == 401


class TestAlertaService:
    """Testes para o serviço de alertas."""
    
    def test_detectar_alertas_estoque_critico(self):
        """Testa detecção de alertas de estoque crítico."""
        service = AlertaService()
        
        # Mock de dados para teste
        item_mock = {
            'id': 1,
            'quantidade': 5,
            'quantidade_minima': 20,
            'preco_venda': Decimal('10.50'),
            'armazem_id': 1,
            'nome_produto': 'Produto Teste',
            'data_validade': datetime.now() + timedelta(days=30)
        }
        
        alertas = service._detectar_alertas_item(item_mock)
        
        # Deve detectar alerta de estoque baixo
        assert len(alertas) > 0
        assert any(a['tipo'] == 'estoque_baixo' for a in alertas)
        
    def test_detectar_alertas_produto_vencido(self):
        """Testa detecção de produtos vencidos."""
        service = AlertaService()
        
        # Mock de produto vencido
        item_mock = {
            'id': 1,
            'quantidade': 10,
            'quantidade_minima': 5,
            'preco_venda': Decimal('15.00'),
            'armazem_id': 1,
            'nome_produto': 'Produto Vencido',
            'data_validade': datetime.now() - timedelta(days=1)
        }
        
        alertas = service._detectar_alertas_item(item_mock)
        
        # Deve detectar alerta de produto vencido
        assert len(alertas) > 0
        assert any(a['tipo'] == 'produto_vencido' for a in alertas)
        assert any(a['prioridade'] == 'critica' for a in alertas)
        
    def test_detectar_alertas_proximo_vencimento(self):
        """Testa detecção de produtos próximos do vencimento."""
        service = AlertaService()
        
        # Mock de produto que vence em 2 dias
        item_mock = {
            'id': 1,
            'quantidade': 10,
            'quantidade_minima': 5,
            'preco_venda': Decimal('20.00'),
            'armazem_id': 1,
            'nome_produto': 'Produto Próximo Vencimento',
            'data_validade': datetime.now() + timedelta(days=2)
        }
        
        alertas = service._detectar_alertas_item(item_mock)
        
        # Deve detectar alerta de próximo vencimento
        assert len(alertas) > 0
        assert any(a['tipo'] == 'proximo_vencimento' for a in alertas)
        
    def test_calcular_prioridade_alerta(self):
        """Testa cálculo de prioridade dos alertas."""
        service = AlertaService()
        
        # Testa diferentes cenários de prioridade
        assert service._calcular_prioridade_estoque(0, 10) == 'critica'  # Sem estoque
        assert service._calcular_prioridade_estoque(2, 10) == 'alta'     # Muito baixo
        assert service._calcular_prioridade_estoque(5, 10) == 'alta'     # 50% do mínimo
        assert service._calcular_prioridade_estoque(8, 10) == 'media'    # Baixo
        
        # Prioridade por vencimento
        assert service._calcular_prioridade_vencimento(1) == 'critica'   # 1 dia
        assert service._calcular_prioridade_vencimento(3) == 'critica'   # 3 dias
        assert service._calcular_prioridade_vencimento(5) == 'alta'      # 5 dias
        assert service._calcular_prioridade_vencimento(15) == 'media'    # 15 dias
        assert service._calcular_prioridade_vencimento(25) == 'baixa'    # 25 dias


def test_integration_alertas_workflow():
    """Teste de integração do fluxo completo de alertas."""
    
    # 1. Verificar alertas críticos
    response = client.post("/alertas/verificar-criticos", headers=headers)
    assert response.status_code == 200
    
    # 2. Consultar dashboard
    response = client.get("/alertas/dashboard", headers=headers)
    assert response.status_code == 200
    dashboard = response.json()
    
    # 3. Listar alertas ativos
    response = client.get("/alertas/ativos", headers=headers)
    assert response.status_code == 200
    alertas = response.json()
    
    # 4. Se há alertas, resolver um
    if alertas:
        alerta_id = alertas[0]["id"]
        response = client.put(
            f"/alertas/{alerta_id}/resolver",
            json={"observacoes": "Resolvido no teste de integração"},
            headers=headers
        )
        assert response.status_code == 200
        
    # 5. Verificar alertas resolvidos
    response = client.get("/alertas/resolvidos", headers=headers)
    assert response.status_code == 200
    
    # 6. Gerar relatório
    response = client.get("/alertas/relatorio", headers=headers)
    assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
