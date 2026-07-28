import os

BASE_PATH = os.path.dirname(__file__)

def run(script):
    path = os.path.join(BASE_PATH, script)
    
    if os.path.exists(path):
        os.system(f"python {path}")
    else:
        print(f"❌ No existe: {path}")

print("\n=== TEST DOCENTE ===")
run("test_docente.py")

print("\n=== TEST HORARIOS ===")
run("test_horarios.py")

print("\n=== TEST CONSULTAS ===")
run("test_consultas.py")