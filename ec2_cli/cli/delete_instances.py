# delete_instances flow
from ec2_cli.cli.list_instances import list_instances_info,run_list_flow
from ec2_cli.services.ec2_service import delete_instances
from ec2_cli.services.ec2_service import get_instances_by_id
from ec2_cli.services.ec2_service import get_instances_by_tag
from ec2_cli.utils.validators import filter_instances

def choose_delete_mode():
    """
    Display a menu that allows the user to choose how EC2 instances
    should be selected for deletion.

    Returns:
        str | None:
            - "id"  → delete instances by Instance ID
            - "tag" → delete instances by Tag
            - None  → exit the deletion flow
    """
    while True:
        menu = input(f"What option would you like to choose: \n"                   
                f"0) Close\n"
                f"1) Delete instance by Instance ID\n"
                f"2) Delete instance(s) by Tag\n")
        try:
            menu = int(menu)
            if menu in [1, 2]:
                if menu == 1:
                    return "id"
                elif menu == 2:
                    return "tag"
            elif menu == 0:
                break

            else:
                print("Invalid option")

        except Exception as e:
            print("Error, please enter a number")
        return None







def confirm_deletion(instances_to_delete):
    """
    Display a summary of all selected instances and ask the user
    for a strong confirmation before deletion.

    Args:
        instances_to_delete (list): Instances selected for deletion.

    Returns:
        bool: True if deletion is confirmed, False otherwise.
    """
    if not instances_to_delete:
        print("There are no instances selected to delete")
        return False

    for instance in instances_to_delete:
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


    while True:
        check = False
        confirm = input("Do you want delete all the instances? Enter 'CONFIRM' or 'CANCEL': \n").upper()
        if confirm in ["CONFIRM", "CANCEL"]:
            if confirm == 'CONFIRM':
                check = True
                break

            elif confirm == 'CANCEL':
                check = False
                break
        else:
            print("Invalid Option")


    if not check:
        return False

    return True





def print_deletion_summary(summary_deletion):
    """
    Print a summary of the deletion process.

    Args:
        summary_deletion (list): Deletion result summary.
    """
    if not summary_deletion:
        print("No instances were deleted")
        return None

    total_number_of_instances = len(summary_deletion)
    for instance in summary_deletion:
        print("Instance Id: "+instance["InstanceId"])
        print("Previous State: "+instance["PreviousState"])
        print("CurrentState: "+instance["CurrentState"])
    print("Total number of instances: " + str(total_number_of_instances))
    return None


def ask_dry_run_mode():
    """
    Ask the user whether to perform a DryRun or a real deletion.

    Returns:
        bool: True if DryRun is enabled, False otherwise.
    """
    dry_run = True
    while True:

        confirm = input("Do you want to use Dry Run for testing or to actually delete the instances.\n"
                        "Enter '1' for DryRun\n"
                        "Enter '2' to delete the instances\n")
        try:
            confirm = int(confirm)
            if confirm in [1, 2]:
                if confirm == 1:
                    dry_run = True
                    break

                elif confirm == 2:
                    dry_run = False
                    break
            else:
                print("Invalid Option")
        except ValueError:
            print("Invalid Option, please enter a number")
    if not dry_run:
        return False
    return True




def run_delete_flow(ec2_client):
    """
    Main workflow that controls the EC2 deletion process.
    """
    while True:
        try:
            instances_to_filter = list_instances_info(ec2_client)
            if not instances_to_filter:
                print("No instances found in the selected region.")
                break

            instances_list = filter_instances(instances_to_filter)
            if not instances_list:
                print("No deletable instances (all are terminated/shutting-down)")
                break
            menu = choose_delete_mode()
            if menu == "tag":
                run_list_flow(ec2_client)
                instances_to_delete = get_instances_by_tag(instances_list)
            elif menu == "id":
                run_list_flow(ec2_client)
                instances_to_delete = get_instances_by_id(instances_list)
            else:
                print("Closing...")
                break

            if not instances_to_delete:
                print("No instances were chosen, exiting...")
                break


            validate_deletion = confirm_deletion(instances_to_delete)
            if not validate_deletion:
                print("the deletion was canceled")
                break
            dry_run = ask_dry_run_mode()

            summary_deletion = delete_instances(ec2_client, instances_to_delete, dry_run)


            print_deletion_summary(summary_deletion)
            continue
        except Exception as e:
            print("Unexpected error: "+ str(e))



