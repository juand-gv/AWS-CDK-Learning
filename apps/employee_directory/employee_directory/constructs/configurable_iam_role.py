from __future__ import annotations

import aws_cdk.aws_iam as iam
from constructs import Construct

from employee_directory.models.iam_config import RoleConfig


class ConfigurableIamRole(Construct):
    def __init__(self, scope: Construct, construct_id: str, *, config: RoleConfig) -> None:
        super().__init__(scope, construct_id)

        self.role = iam.Role(
            self,
            "Role",
            role_name=config.role_name,
            assumed_by=iam.ServicePrincipal(config.assumed_by.service),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(name)
                for name in config.managed_policies
            ],
        )

        # Optional inline policies to avoid FullAccess
        for p in config.inline_policies:
            statements = []
            for s in p.statements:
                statements.append(
                    iam.PolicyStatement(
                        effect=iam.Effect.ALLOW if s.effect == "Allow" else iam.Effect.DENY,
                        actions=s.actions,
                        resources=s.resources,
                    )
                )

            iam.Policy(
                self,
                f"InlinePolicy-{p.name}",
                policy_name=p.name,
                statements=statements,
            ).attach_to_role(self.role)
