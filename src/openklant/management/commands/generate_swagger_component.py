from django.conf import settings
from django.urls import set_script_prefix

from vng_api_common.management.commands import generate_swagger
from vng_api_common.schema import OpenAPISchemaGenerator

SCHEMA_MAPPING = {
    "info": "openklant.components.{}.api.schema.info",
    "urlconf": "openklant.components.{}.api.urls",
}


class Command(generate_swagger.Command):
    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument(
            "--component",
            dest="component",
            default=None,
            help="The component name to define urlconf, base_path and schema info",
        )

    # Workaround since vng-api-common 1.5.x does not pass the urlconf to its
    # schema_generator_class
    def get_schema_generator(
        self, generator_class_name, info, api_version, api_url
    ):
        return OpenAPISchemaGenerator(info=info, url=api_url, urlconf=self.urlconf)

    def handle(
        self,
        output_file,
        overwrite,
        format,
        api_url,
        mock,
        api_version,
        user,
        private,
        info,
        urlconf,
        component=None,
        *args,
        **options,
    ):
        _version = getattr(settings, f"{component.upper()}_API_VERSION")

        # Setting must exist for vng-api-common, so monkeypatch it in
        settings.API_VERSION = _version
        api_version = _version.split('.')[0]

        if settings.SUBPATH:
            set_script_prefix(settings.SUBPATH)

        if not component:
            super().handle(
                output_file,
                overwrite,
                format,
                api_url,
                mock,
                api_version,
                user,
                private,
                info=info,
                urlconf=urlconf,
                *args,
                **options,
            )

        # rewrite command arguments based on the component
        info = SCHEMA_MAPPING["info"].format(component)
        urlconf = SCHEMA_MAPPING["urlconf"].format(component)

        self.urlconf = urlconf

        # generate schema
        super().handle(
            output_file,
            overwrite,
            format,
            api_url,
            mock,
            api_version,
            user,
            private,
            info=info,
            urlconf=urlconf,
            *args,
            **options,
        )
