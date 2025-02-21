from connexion import RestyResolver
from inflection import underscore


class CamelCaseRestyResolver(RestyResolver):
    def resolve_operation_id(self, operation):
        """
        operationId resolver, convert camelCase[.method] operationId to snake_case
        :type operation: connexion.operations.AbstractOperation
        """

        # getting operationId and converting to snake_case
        operation_id_parts = operation.operation_id.split(".", 1)
        if len(operation_id_parts) == 1:
            operation_id = underscore(operation.operation_id)
        else:
            operation_id = f"{underscore(operation_id_parts[0])}_{operation_id_parts[1]}"

        router_controller = operation_id.split("_", 1)[0]

        # eg: bach_api.applications.auth.controller.login
        return "api.applications.{}.controller.{}".format(router_controller, operation_id)
