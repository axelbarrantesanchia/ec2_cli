# Create_instances flow
from botocore.exceptions import ClientError
from ec2_cli.cli import create_instances


def valid_instance(ec2):
    # This function checks if an EC2 instance with the provided Name tag
    # already exists in the AWS account.
    response = ec2.describe_instances()
    all_instance_tags = []
    # Ask the user for the desired instance name
    instance_name = input("Enter the name of your instance: ")
    try:
        # Iterate through all reservations and instances
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                # Extract the value of the "Name" tag if it exists
                name = next((t["Value"] for t in instance.get("Tags", []) if t["Key"] == "Name"), None)
                all_instance_tags.append(name)
                print(all_instance_tags)

    except ClientError as e:
        # Handle AWS API errors
        print("It can't get the instances due to: "+ str(e))
        return None
    # Check if the entered name already exists
    if instance_name in all_instance_tags:
        print("There is already an instance with that name: " + instance_name)
        return None
    else:
        return instance_name

def choose_environment():
    # This function allows the user to choose an environment tag
    # for the EC2 instance (Dev, Stage, Test, or Prod).
    while True:
        try:
            while True:
                environment = input("Choose one environment for your instances\n"
                                "1) Dev\n"
                                "2) Stage\n"
                                "3) Test\n"
                                "4) Prod *To create an instance using Prod tag you need permission*\n"
                                    "If you do not choose an option, the default environment will be 'Dev': \n" )
                # Default environment is Dev if no input is provided
                if not environment:
                    environment = 1
                environment = int(environment)
                # Validate option range
                if environment >= 1 and environment <= 4:
                    break

        except ValueError as v:
            # Handle invalid numeric input
            print("You did not write a valid number "+str(v))
            continue
        # Map numeric option to environment name
        if environment == 1:
            environment = "Dev"
            return environment
        elif environment == 2:
            environment = "Stage"
            return environment
        elif environment == 3:
            environment = "Test"
            return environment
        elif environment == 4:
            # Additional confirmation is required for Prod
            environment = "Prod"
            while True:
                confirmation = input("Are you sure you want to assign this tag? Enter 'Confirm'")
                if not confirmation :
                    print("You did not enter anything")
                    continue
                if confirmation == "Confirm":
                    return environment
                else:
                    print("Invalid Option")
                    continue



def run_create_flow(ec2_client):
    # This function orchestrates the complete flow:
    # 1. Choose environment
    # 2. Validate instance name
    # 3. Create the EC2 instance
    env = choose_environment()
    instance_name = valid_instance(ec2_client)

    if instance_name is not None:
        create_instances(ec2_client, instance_name, env)



