
conda create -n mep python=3.11 -y


conda activate mep
pip install -r requirements.txt
uvicorn app.main:app --reload





TASKS:
✅ Register JWT
✅ Login
✅ Create Project
✅ Get My Projects

✅ Upload Files
✅ Get Project files by name or ID
✅ Delete Project

Analyze Uploaded File : 
المهندس يرفع Excel.
بعدها يدوس Analyze 

تجيب ملفات المشروع من Database.
تقرأ أول Excel موجود باستخدام:
{
  "file_name": "BOQ.xlsx",
  "rows": 10,
  "columns": 10,
  "column_names": [
    "Room",
    "Area",
    "Load"
  ]
}
