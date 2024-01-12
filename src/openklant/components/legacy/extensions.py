from drf_spectacular.extensions import OpenApiAuthenticationExtension

from .authorization import JWTDummyAuthentication


class PolymorphicSerializerExtension(OpenApiAuthenticationExtension):
    target_class = JWTDummyAuthentication
    name = "JWT-Claims"

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }

    def get_security_requirement(self, auto_schema):
        action = auto_schema._view.action
        scope = auto_schema._view.required_scopes[action]

        assert self.name, "name(s) must be specified"
        if isinstance(self.name, str):
            return {self.name: [scope.label]}
        else:
            return {name: [scope.label] for name in self.name}
