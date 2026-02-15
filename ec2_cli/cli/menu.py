# Menu flow
from ec2_cli.cli.create_instances import run_create_flow
from ec2_cli.cli.list_instances import run_list_flow
from ec2_cli.cli.delete_instances import run_delete_flow
from ec2_cli.aws.session import rebuild_ec2_config_for_region
from ec2_cli.aws.session import get_client

def show_menu(client, session):
    """
     Display the main interactive menu and handle user actions.

     This function acts as the central dispatcher of the application,
     allowing the user to:
         - Create EC2 instances
         - List EC2 instances
         - Delete EC2 instances
         - Change the active AWS region

     Args:
         client: Active EC2 client.
         session: Active boto3 session.

     Returns:
         None
     """
    while True:

        menu = input(f"What option would you like to choose: \n"
                     f"0) Exit\n"
                     f"1) Create an instance\n"
                     f"2) List instances\n"
                     f"3) Delete instance(s) by Id/Tag\n"
                     f"4) Change Region\n")
        try:
            menu = int(menu)
            if menu in [1, 2, 3, 4]:
                if menu == 1:
                    run_create_flow(client)
                elif menu == 2:
                    run_list_flow(client)
                elif menu == 3:
                    run_delete_flow(client)
                elif menu == 4:
                    aws_config, selected_region = rebuild_ec2_config_for_region(session)
                    if not aws_config:
                        continue
                    client = get_client(session, aws_config)
                    print("Your region has changed to: " + selected_region)
                    continue


            elif menu == 0:
                break

            else:
                print("Invalid option")

        except ValueError:
            print("Error, please enter a number")
    return None