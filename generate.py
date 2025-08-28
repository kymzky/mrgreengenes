import yaml
from jinja2 import Environment, FileSystemLoader
import os
import shutil

THEME_FILE = "theme.yaml"
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "output"

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
with open(THEME_FILE) as f:
    theme = yaml.safe_load(f)

name = theme["name"]
style = theme.get("style", {})
colors = style.get("colors", {})
enabled_for = theme.get("enabled_for", [])

print(f"Generating theme '{name}' for: {enabled_for}")

for app in enabled_for:
    template_app_dir = os.path.join(TEMPLATE_DIR, app)
    if not os.path.exists(template_app_dir):
        print(f"Warning: no templates for {app}")
        continue

    output_app_dir = os.path.join(OUTPUT_DIR, app, name)
    os.makedirs(output_app_dir, exist_ok=True)

    for root, dirs, files in os.walk(template_app_dir):
        for file_name in files:
            src_path = os.path.join(root, file_name)
            rel_path = os.path.relpath(src_path, template_app_dir)
            dst_path = os.path.join(
                output_app_dir, rel_path.replace(".j2", ""))

            os.makedirs(os.path.dirname(dst_path), exist_ok=True)

            if file_name.endswith(".j2"):
                template = env.get_template(
                    os.path.join(app, rel_path).replace("\\", "/"))
                render_vars = {"theme_name": name, **style, **colors }
                output_text = template.render(**render_vars)
                with open(dst_path, "w") as f:
                    f.write(output_text)
                print(f"Generated {dst_path}")
            else:
                shutil.copy2(src_path, dst_path)
                print(f"Copied {dst_path}")
