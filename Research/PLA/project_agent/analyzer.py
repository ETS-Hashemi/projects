import os

def analyze_repo(repo_path):
    summary = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py") and "project_agent" not in root:
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                        summary.append(f"\nFile: {path}\n{content[:1000]}")
                except:
                    continue
    return "\n".join(summary)
