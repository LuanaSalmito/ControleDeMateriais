
from enum import Enum


class StatusManutencao(str, Enum):

    ABERTO = "aberto"
    FINALIZADO = "finalizado"
    
    @classmethod
    def is_finalizado(cls, status: str) -> bool:
        """
        Verifica se um status indica que a manutenção está finalizada.
        
        Args:
            status: Status a ser verificado
            
        Returns:
            True se o status indica finalização
        """
        if isinstance(status, cls):
            return status == cls.FINALIZADO
        return status.lower() in ["finalizado", "finalizada", "fechada", "concluida", "concluída"]
