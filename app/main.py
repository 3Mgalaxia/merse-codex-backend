from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.routes import (
    analyse,
    beautify,
    componentize,
    convert_react,
    convert_tailwind,
    edit,
    execute,
    fix_errors,
    minify,
    refactor,
    refactor_ui,
    repair,
    seo,
    to_nextjs,
    to_tailwind,
    upgrade,
)

app = FastAPI(
    title="Merse Codex API",
    description=(
        "Merse Codex — cérebro de edição e criação de código da Merse. "
        "Edita HTML, analisa, refatora, converte para React e muito mais."
    ),
    version="1.0.0",
)

# CORS – depois você restringe só para o domínio da Merse em produção
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # em produção: ["https://merse.app", ...]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Healthcheck
@app.get("/health")
async def health():
    return {"status": "ok", "service": "merse-codex", "version": "1.0.0"}


# Homepage
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
    <head>
        <title>Merse Codex</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                background: radial-gradient(circle at center, #1a0033, #000000);
                font-family: Arial, sans-serif;
                color: white;
                text-align: center;
            }
            h1 {
                margin-top: 120px;
                font-size: 4em;
                color: #39ff14;
                text-shadow: 0 0 15px #39ff14, 0 0 25px #39ff14;
            }
            p {
                font-size: 1.3em;
                opacity: 0.8;
            }
            .container {
                margin-top: 40px;
                display: flex;
                justify-content: center;
                gap: 20px;
            }
            .card {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255,255,255,0.1);
                padding: 25px;
                width: 280px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
                box-shadow: 0 0 15px rgba(0,0,0,0.4);
            }
            .card h3 {
                color: #39ff14;
            }
            .card p {
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <h1>Merse Codex</h1>
        <p>A inteligência que edita, analisa e transforma websites no estilo MERSE.</p>

        <div class="container">
            <div class="card">
                <h3>Edit-Site</h3>
                <p>Edita HTML usando comandos naturais.</p>
            </div>

            <div class="card">
                <h3>Analyse-Site</h3>
                <p>Analisa e dá nota no seu HTML/CSS.</p>
            </div>

            <div class="card">
                <h3>Convert React</h3>
                <p>Transforma HTML em componentes React modernos.</p>
            </div>
        </div>
    </body>
    </html>
    """

# Registrar rotas
app.include_router(edit.router, prefix="/codex", tags=["edit"])
app.include_router(analyse.router, prefix="/codex", tags=["analyse"])
app.include_router(execute.router, prefix="/codex", tags=["execute"])
app.include_router(refactor.router, prefix="/codex", tags=["refactor"])
app.include_router(beautify.router, prefix="/codex", tags=["beautify"])
app.include_router(seo.router, prefix="/codex", tags=["seo"])
app.include_router(convert_react.router, prefix="/codex", tags=["convert-react"])
app.include_router(convert_tailwind.router, prefix="/codex", tags=["convert-tailwind"])
app.include_router(componentize.router, prefix="/codex", tags=["componentize"])
app.include_router(repair.router, prefix="/codex", tags=["repair"])
app.include_router(minify.router, prefix="/codex", tags=["minify"])
app.include_router(refactor_ui.router, prefix="/codex", tags=["refactor-ui"])
app.include_router(to_tailwind.router, prefix="/codex", tags=["to-tailwind"])
app.include_router(to_nextjs.router, prefix="/codex", tags=["to-nextjs"])
app.include_router(fix_errors.router, prefix="/codex", tags=["fix-errors"])
app.include_router(upgrade.router, prefix="/codex", tags=["upgrade"])
