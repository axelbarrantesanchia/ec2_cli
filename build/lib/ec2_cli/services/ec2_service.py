# ec2_service flow

from botocore.exceptions import ClientError
from aws_scripts.ec2_cli.services.ami_service import find_ami
from aws_scripts.ec2_cli.utils.validators import valid_tag_keys
from aws_scripts.ec2_cli.utils.validators import valid_tag_values
def create_instances(ec2, instance_name, environment):
    # Ask the user for an AMI ID or automatically find one
    ami_id = input("Enter the ID for the AMI of your instance: ") or find_ami(ec2)


    try:
        # Launch a new EC2 instance
        response = ec2.run_instances(
            ImageId=ami_id,
            InstanceType="t2.micro",
            MinCount=1,
            MaxCount=1,
            DryRun=False,  # Set to False to actually create the instance
            TagSpecifications=[
                {
                    "ResourceType": "instance",
                    "Tags": [
                        {"Key": "Name", "Value": instance_name},
                        {"Key": "Environment", "Value": environment}
                    ],
                }
            ],
        )

        # Retrieve the newly created instance ID
        instance_id = response["Instances"][0]["InstanceId"]
        print("Instance has been successfully created:", instance_id)

    except ClientError as e:
        # Handle errors during instance creation
        print("There has been an error creating the instance: " + str(e))


def list_instances_info(ec2_client):
    """
    Retrieve basic information about all EC2 instances in the current AWS region.

    This function calls the EC2 DescribeInstances API and extracts
    relevant attributes for each instance, such as networking details,
    state, availability zone, and tags.

    Args:
        ec2_client: Boto3 EC2 client used to interact with AWS EC2.

    Returns:
        list | None:
            - A list of dictionaries containing instance attributes.
            - None if an error occurs while retrieving or processing data.
    """
    response = ec2_client.describe_instances()
    instances_list = []
    try:
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                instance_attributes = {
                    "InstanceId": instance.get("InstanceId", "N/A"),
                    "VpcId": instance.get("VpcId", "No VPC"),
                    "SubnetId": instance.get("SubnetId", None),
                    "State": instance.get("State", {}).get("Name", "unknown"),
                    "AvailabilityZone": instance.get("Placement", {}).get("AvailabilityZone", "unknown"),
                    "Tags": instance.get("Tags", [])
                }
                instances_list.append(instance_attributes)

        return instances_list
    except ClientError as e:
        print("There has been an error while listing the instance"+ str(e))
        return None
    except KeyError as k:
        print("There has been an error while trying to access a key within the dictionary: "+ str(k))
        print(response)
        return None


def get_instances_by_id(instances_list):
    """
    Allow the user to select EC2 instances for deletion by providing
    their Instance IDs.

    Args:
        instances_list (list): List of available EC2 instances.

    Returns:
        list: Instances selected for deletion.

    """

    instances_to_delete = []
    while True:
        chosen_instance = input("Enter the ID of the instances you want to terminate: ")
        match = False

        for instance in instances_list:
            if chosen_instance == instance["InstanceId"]:
                instances_to_delete.append(instance)
                match = True

        if match:
            print("The instance has been added to the list")
        if not match:
            print("There is no instance with that Id")
            continue

        check = False
        if match:
            while True:
                confirm = input("Do you want to add another instance? Enter 'yes' or 'no':\n").lower()
                if confirm in ["yes", "no"]:
                    if confirm == 'yes':
                        check = True
                        break

                    elif confirm == 'no':
                        break
                else:
                    print("Invalid Option")

        if not check:
            break
        if check:
            continue
    return instances_to_delete




def get_instances_by_tag(instances_list):
    """
      Allow the user to select EC2 instances for deletion by filtering
      based on a specific tag key and value.

      Args:
          instances_list (list): List of available EC2 instances.

      Returns:
          list: Instances selected for deletion.
      """

    while True:
        tag_key = input("Which key do you want to search: "
                        "\nIf you do not specify the key, 'Environment' will be used by default\n")

        if tag_key == '':
            tag_key = 'Environment'
            option = input("Choose from what environment you want to delete the instance: \n"
                               "\n1) Dev"
                               "\n2) Stage"
                               "\n3) Test \n")

            try:
                option = int(option)
                if option == 1:
                    tag_value = "Dev"
                    break
                elif option == 2:
                    tag_value = "Stage"
                    break
                elif option == 3:
                    tag_value = "Test"
                    break
                else:
                    print("Invalid Option")
                    continue
            except ValueError:
                print("Please enter a number between 1 and 3")
        else:
            validating_tag_key = valid_tag_keys(tag_key,instances_list)
            if validating_tag_key:
                tag_value = input(f"Enter the value of the tag that you provided: {tag_key}\n ")
                validating_tag_value = valid_tag_values(tag_key,tag_value,instances_list)
                if validating_tag_value:
                    break
                else:
                    print("You have entered an invalid tag value")
            print("You have entered an invalid tag key")
            continue



    instances_filter= []
    instances_to_delete = []


    for instance in instances_list:
        for tag in instance["Tags"]:
            if tag["Key"] == tag_key and tag["Value"] == tag_value:
                instances_filter.append(instance)

    for instance_number, instance in enumerate(instances_filter,start=1):
        print("----------------------------------")
        print(str(instance_number)+")" + f" Instance ID: {instance.get('InstanceId', 'N/A')}")
        print("----------------------------------")
        print(f"VPC ID: {instance.get('VpcId', 'N/A')}")

        print(f"State: {instance.get('State', 'Unknown')}")

        print(f"Subnet ID: {instance.get('SubnetId', 'N/A')}")
        print(f"AZ: {instance.get('AvailabilityZone', 'N/A')}")

        tags = instance.get("Tags", [])
        if tags:
            print("--- Tags ---")
            for tag in tags:

                key = tag.get("Key", "Undefined")
                value = tag.get("Value", "Undefined")
                print(f"  Tag: {key} | Value: {value}")
        print("----------------------------------")
    if not instances_filter:
        print("There is no instance with that tag")

    if instances_filter:
        while True:
            match = False
            chosen_instance = input("Choose an instance based on its index: \n")
            try:
                chosen_instance = int(chosen_instance)
                chosen_instance = chosen_instance - 1
                if 0 <= chosen_instance < len(instances_filter):
                    instances_to_delete.append(instances_filter[chosen_instance])
                    match = True
            except:
                print("Invalid Option")
                continue



            if match:
                print("The instance has been added to the list")
            if not match:
                print("The index is invalid")
                continue

            check = False
            if match:
                while True:
                    confirm = input("Do you want to add another instance? Enter 'yes' or 'no'\n").lower()
                    if confirm in ["yes", "no"]:
                        if confirm == 'yes':
                            check = True
                            break

                        elif confirm == 'no':
                            break
                    else:
                        print("Invalid Option")

            if not check:
                break
            if check:
                continue
    return instances_to_delete


def delete_instances(ec2_client, instances_to_delete, dry_run_flag):
    """
    Terminate EC2 instances using their Instance IDs.

    Args:
        ec2_client: Boto3 EC2 client.
        instances_to_delete (list): Instances selected for deletion.
        dry_run_flag (bool): If True, perform a DryRun.

    Returns:
        list | None: Summary of terminated instances.
    """
    instances_ids = []
    for instance in instances_to_delete:
        instances_ids.append(instance["InstanceId"])

    if not instances_ids:
        print("There are no instances IDs")
        return None

    summary_deletion = []
    try:
        response = ec2_client.terminate_instances(InstanceIds=instances_ids, DryRun=dry_run_flag)
        for instance in response["TerminatingInstances"]:
            instances_deleted = {
            'InstanceId': instance["InstanceId"],
            'PreviousState': instance["PreviousState"]["Name"],
            'CurrentState': instance["CurrentState"]["Name"]
            }
            summary_deletion.append(instances_deleted)
    except ClientError as c:
        if 'DryRunOperation' not in str(c):
            print("There has been an error: " + str(c))
            return None
        else:
            print("The request would have succeded -> DryRunTrue")

    return summary_deletion

