FinanControl - Railway Ready

Análise automática:
- Backend: /mnt/data/FinanControl_RailwayWork/backend
- Frontend: /mnt/data/FinanControl_RailwayWork/frontend
- Framework detectado: fastapi
- Arquivos gerados: Procfile (root) and backend/requirements.txt (if missing).

Deploy recomendado (2 serviços no Railway):

1) Frontend (Static Site)
- Em Railway: New Project -> New Static Site
- Upload: extraia e envie o conteúdo da pasta: /mnt/data/FinanControl_RailwayWork/frontend
- O site ficará disponível em https://<your-frontend>.up.railway.app

2) Backend (Web Service)
- Em Railway: New Project -> New Service -> Deploy Manual (Upload ZIP) ou conectar GitHub
- Se for upload ZIP, envie este pacote completo.
- Build Command: pip install -r backend/requirements.txt
- Start Command: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
- O serviço ficará disponível em https://<your-backend>.up.railway.app

Integração:
- Atualize o frontend para apontar as chamadas API para a URL do backend acima.
- Se preferir, eu posso automatizar a substituição dessas URLs no frontend antes do deploy.

Observações:
- Não modifiquei seus arquivos de código além de gerar requirements.txt se necessário.
- Este pacote está pronto para upload no Railway.