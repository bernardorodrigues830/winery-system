import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class LogAuditoriaMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        inicio = time.time()
        response = await call_next(request)
        duracao = round((time.time() - inicio) * 1000, 2)
        
        # Tenta capturar o e-mail se injetado no header (opcional/customizado)
        usuario_email = request.headers.get("X-User-Email", "anonimo")
        
        print(
            f"[AUDITORIA] {request.method} {request.url.path} | "
            f"status={response.status_code} | "
            f"tempo={duracao}ms | usuario={usuario_email}"
        )
        return response