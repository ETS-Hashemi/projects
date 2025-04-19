def write_report(content):
    with open("NEXT_STEPS.md", "w", encoding="utf-8") as f:
        f.write("# 🔄 Next Steps for This Project\n\n")
        f.write(content)
