# list_instances flow
from ec2_cli.services.ec2_service import list_instances_info
from ec2_cli.utils.validators import filter_instances


def print_instances_info(instances_list):
    if not instances_list:
        print("You do not have any instance")
        return

    for instance in instances_list:

        print("----------------------------------")
        print(f"Instance ID: {instance.get('InstanceId', 'N/A')}")
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

def run_list_flow(ec2_client):
    """
    Main execution flow for listing EC2 instances.

    This function retrieves instance information and prints it
    in a human-readable format.
    """
    listing_instances = list_instances_info(ec2_client)

    # Error real (None)
    if listing_instances is None:
        print("There was an error retrieving instances.")
        return

    # No instances at all
    if len(listing_instances) == 0:
        print("There are no instances in this region.")
        return

    # Apply filter
    filtered_instances = filter_instances(listing_instances)

    # No instances after filtering
    if len(filtered_instances) == 0:
        print("There are no instances in allowed states.")
        return

    print_instances_info(filtered_instances)