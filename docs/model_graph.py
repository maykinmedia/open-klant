import os

from vng_api_common.diagrams.generate_graphs import generate_model_graphs


def build_graph(sphinx_app):
    components_dir = os.path.abspath(
        os.path.join(sphinx_app.srcdir, "..", "src", "openklant", "components")
    )

    generate_model_graphs(
        sphinx_app,
        excluded_models=[
            "token",
            "utils",
            "AdresMixin",
            "ContactnaamMixin",
            "CorrespondentieadresMixin",
            "BezoekadresMixin",
        ],
        components_dir=components_dir,
    )


def setup(app):
    app.connect("builder-inited", build_graph)
