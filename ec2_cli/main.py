#!/usr/bin/env python3
# main flow
from ec2_cli.aws.session import run_client_flow
from ec2_cli.cli.menu import show_menu


def print_aws_tool():
    """
    Print the banner for the AWS EC2 management tool.

    This function is purely cosmetic and helps identify the tool
    when it is executed from the terminal.
    """
    print("=" * 40)
    print(" AWS CLI TOOL — EC2 Management - By Axel Barrantes ")
    print(" Built for learning. Designed like production.")
    print("=" * 40)



def main():
    """
    Entry point for the AWS EC2 management tool.

    This function:
        1. Prints the application banner
        2. Initializes the AWS client and session
        3. Launches the main interactive menu

    All initialization errors are caught to prevent
    unexpected crashes at startup.
    """
    try:
        print_aws_tool()
        client, session = run_client_flow()
        show_menu(client,session)
    except Exception as e:
        print("The tool could not be initialized. Verify your AWS credentials and try again " + str(e))

if __name__ == "__main__":
    main()