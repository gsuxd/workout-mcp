COPY --chown=appuser:appuser . .
 
USER appuser
 
# Puerto SSE / streamable-http (fastmcp default: 8000)
EXPOSE 8001
 
# Variables de entorno — sobreescribir en runtime con --env o .env
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MCP_HOST=0.0.0.0 \
    MCP_PORT=8001 \
    # Hevy API key — REQUERIDA en runtime
 
# Healthcheck básico (ajustar ruta según transport elegido)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${MCP_PORT}/')" || exit 1
 
# Entrypoint: corre el servidor MCP en modo SSE (HTTP) en lugar de stdio
# Si tu main.py ya acepta --transport, ajusta aquí.
# Si no, usa el wrapper de abajo (ver README en el Dockerfile).
CMD ["python", "main.py"]
