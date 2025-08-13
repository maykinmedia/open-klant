import os

from django.core.management import call_command


def generate_model_graphs(app):
    output_dir = os.path.join(app.srcdir, "_static", "uml")
    os.makedirs(output_dir, exist_ok=True)

    project_root = os.path.abspath(os.path.join(app.srcdir, ".."))
    components_dir = os.path.join(project_root, "src", "openklant", "components")

    excluded_components = ["token", "utils"]

    apps_in_components = [
        d
        for d in os.listdir(components_dir)
        if os.path.isdir(os.path.join(components_dir, d))
        and os.path.isfile(os.path.join(components_dir, d, "__init__.py"))
        and d not in excluded_components
    ]

    # Generate diagrams for each allowed component
    for comp in apps_in_components:
        png_path = os.path.join(output_dir, f"{comp}.png")
        try:
            call_command(
                "graph_models",
                comp,
                output=png_path,
                rankdir="LR",
                hide_edge_labels=True,
            )
        except Exception as exc:
            print(f"Failed to generate PNG for {comp}: {exc}")
