from pathlib import Path

def save_uploaded_file(uploaded_file):
    upload_dir = Path("data/resumes")
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / uploaded_file.name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return str(file_path)