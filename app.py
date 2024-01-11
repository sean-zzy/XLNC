import uvicorn
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "dev":
            uvicorn.run(
                "xlnc.main:app",
                host="",
                port=8000,
                reload=True,
                reload_dirs=[],
                reload_includes=["*.py", "*.html", "*.js", "*.css"],
            )
    else:
        uvicorn.run("xlnc.main:app", host="0.0.0.0", port=8000)
