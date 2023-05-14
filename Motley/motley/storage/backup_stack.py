from aws_cdk import (
    # Duration,
    Stack,
    aws_backup as backup, CfnOutput, RemovalPolicy, )
from constructs import Construct


class BackupStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vault = backup.BackupVault(self, "Vault",
                                   removal_policy=RemovalPolicy.DESTROY,
                                   )

        # Daily, weekly and monthly with 5 year retention
        plan = backup.BackupPlan.daily_weekly_monthly5_year_retention(self, "Plan", backup_vault=vault, )

        CfnOutput(self, 'BackupPlanArn',
                  description='The ARN of the backup plan.',
                  value=plan.backup_plan_arn
                  )
        CfnOutput(self, 'BackupPlanId',
                  description='The identifier of the backup plan.',
                  value=plan.backup_plan_id
                  )
        CfnOutput(self, 'BackupPlanVaultArn',
                  description='The ARN of the backup vault.',
                  value=plan.backup_vault.backup_vault_arn
                  )
        CfnOutput(self, 'BackupPlanVaultName',
                  description='The name of the backup vault.',
                  value=plan.backup_vault.backup_vault_name
                  )
        CfnOutput(self, 'BackupVersionId',
                  description='Backup version.',
                  value=plan.version_id
                  )

        my_cool_construct = Construct(self, "MyCoolConstruct")

        selection = plan.add_selection("Selection",
                                       resources=[
                                           # All resources that are tagged stage=prod in the region/account
                                           backup.BackupResource.from_construct(my_cool_construct),

                                           # All resources that are tagged stage=prod in the region/account
                                           backup.BackupResource.from_tag("stage", "prod"),
                                       ]
                                       )
        CfnOutput(self, 'BackupSelectionId',
                  description='The identifier of the backup selection.',
                  value=selection.selection_id
                  )
