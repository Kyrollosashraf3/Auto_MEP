
conda create -n mep python=3.11 -y


conda activate mep
pip install -r requirements.txt
uvicorn app.main:app --reload



