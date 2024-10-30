import boto3
import json

# Initialize Boto3 clients
appconfig = boto3.client('appconfig')
appconfig_data = boto3.client('appconfigdata')

def list_appconfig_feature_flags():
    # List all applications
    applications = appconfig.list_applications()

    for app in applications['Items']:
        app_id = app['Id']
        print(f"Application: {app['Name']} (ID: {app_id})")

        # List configuration profiles for each application
        profiles = appconfig.list_configuration_profiles(ApplicationId=app_id)

        for profile in profiles['Items']:
            if profile['Type'] == 'AWS.AppConfig.FeatureFlags':
                profile_id = profile['Id']
                print(f"  Feature Flag Profile: {profile['Name']} (ID: {profile_id})")

                # List environments for the application
                environments = appconfig.list_environments(ApplicationId=app_id)

                for env in environments['Items']:
                    env_id = env['Id']
                    print(f"    Environment: {env['Name']} (ID: {env_id})")

                    # Get the latest configuration
                    session = appconfig_data.start_configuration_session(
                        ApplicationIdentifier=app_id,
                        EnvironmentIdentifier=env_id,
                        ConfigurationProfileIdentifier=profile_id
                    )

                    # Parse the configuration content
                    if config['Configuration']:
                        content = json.loads(config['Configuration'].read())
                        print(f"      Feature Flags:")
                        for flag, details in content.get('flags', {}).items():
                            enabled = content['values'][flag]['enabled']
                            print(f"        - {flag}: {'Enabled' if enabled else 'Disabled'}")
                    else:
                        print("      No configuration data available.")

    print("\nDone listing all AppConfig feature flags.")

if __name__ == "__main__":
    list_appconfig_feature_flags()
