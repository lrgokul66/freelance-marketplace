import os
import importlib.util

spec = importlib.util.spec_from_file_location("root_app", "app.py")
root_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(root_app)
create_app = root_app.create_app

app = create_app()
with app.app_context():
    from database import execute_query
    res = execute_query("SELECT id, title, category, status FROM projects", fetch='all')
    for r in res:
        print(r)
