INSTRUCCIONES - DEPLOY EN RENDER

1. Crear cuenta en https://render.com
2. Subir este proyecto a GitHub
3. En Render → New → Web Service
4. Conectar repo
5. Configurar:
   Build Command: pip install -r requirements.txt
   Start Command: streamlit run app.py --server.port=10000 --server.address=0.0.0.0

IMPORTANTE:
- Agregar tu archivo template_brief.docx en esta carpeta antes de subir
- Los archivos generados se descargan desde la app (no se guardan en servidor)

RESULTADO:
Tendrás una URL pública con tu app
