      stack_set = CfnStackSet(self, 'MyStackSet',
                                stack_set_name='SetOfStacks',
                                capabilities=['CAPABILITY_NAMED_IAM', 'CAPABILITY_IAM'],
                                description='',
                                tags=[CfnTag(
                                    key="Name",
                                    value="Self-Managed stacksets"
                                )],
                                template_url=template_asset.http_url,
                                stack_instances_group=[CfnStackSet.StackInstancesProperty(
                                    deployment_targets=CfnStackSet.DeploymentTargetsProperty(
                                        accounts=[
                                            "xxxxxxxxxxx",  # Master
                                        ],
                                    ),
                                    regions=["eu-west-1"],
                                )],
                                permission_model='SELF_MANAGED',
                                )
