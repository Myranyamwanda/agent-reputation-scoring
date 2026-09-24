python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
Write-Host "Setup complete. Edit .env with your real DATABASE_URL / AWS settings."
