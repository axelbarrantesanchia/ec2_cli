import re
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError, NoRegionError, NoCredentialsError


def ask_for_profile():
    """
    Prompt the user to select an AWS CLI profile.

    If no profiles are found, the default credential chain is used.
    The user can select a profile by index or press Enter to use
    the default profile.

    Returns:
        boto3.Session: A boto3 session configured with the selected profile.
    """
    session = boto3.Session()
    profiles = session.available_profiles
    if not profiles:
        print("No profiles found → using default chain")
        return session

    for num, profile in enumerate(profiles, start=1):
        print(f"{num}) {profile}")
    print(f"---")
    print(f"Default -> Press Enter")

    while True:
        chosen_profile = input("Select an AWS profile by number (press Enter or 0 to use the default profile): ")
        if not chosen_profile:
            return session
        try:
            chosen_profile = int(chosen_profile)
            if chosen_profile == 0:
                return session
            chosen_profile = chosen_profile - 1
            if 0 <= chosen_profile < len(profiles):
                break
            else:
                print("Invalid profile selection. Choose a number from the list.")
        except ValueError:
            print("Profile number out of range. Please select one of the listed profiles.")
    session = boto3.Session(profile_name=profiles[chosen_profile])
    return session


def available_regions(session, bootstrap_region: str = "us-east-1"):
    """
    Returns a sorted list of AWS region names using a bootstrap EC2 client.
    Uses the SAME session the user selected (profile/default chain).
    If it fails, returns None (so MAIN can fallback to manual region input).
    """
    try:

        ec2 = session.client(
            "ec2",
            region_name=bootstrap_region,
            config=Config(retries={"max_attempts": 5, "mode": "standard"})
        )
        resp = ec2.describe_regions(AllRegions=False)
        regions = sorted(r["RegionName"] for r in resp.get("Regions", []) if r.get("RegionName"))
        return regions or None

    except (NoRegionError, NoCredentialsError) as e:
        print("AWS configuration error:")
        print(" - No region or credentials were found.")
        print(f" - Details: {e}")
        return None

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        error_message = e.response.get("Error", {}).get("Message", "No message provided")
        print("AWS API error:")
        print(f" - Error Code: {error_code}")
        print(f" - Message: {error_message}")
        return None


    except Exception as e:
        print("Unexpected error occurred while communicating with AWS.")
        print(f" - Details: {e}")
        return None


def choose_region(list_of_regions):
    """
    Allow the user to select an AWS region.

    If regions cannot be retrieved automatically, the user is asked
    to manually input a region name that matches the AWS region format.

    Args:
        list_of_regions (list): List of available AWS regions.

    Returns:
        str: Selected AWS region.
    """
    pattern = r"^[a-z]{2}-[a-z0-9-]+-\d+$"

    if not list_of_regions:
        while True:
            raw = input(
                "I was unable to obtain regions automatically. Please enter a region manually (example: us-west-1): "
            )

            chosen_region = raw.strip().lower()

            if not chosen_region:
                print("Invalid region: it cannot be empty.")
                continue

            if re.fullmatch(pattern, chosen_region):
                return chosen_region

            print("Invalid region format. Expected something like: 'us-west-1' ")

    region_number = len(list_of_regions)
    for num,region in enumerate(list_of_regions, start=1):
        print(f"{str(num)}) Available Regions: " + region)
    print(f"Found {str(region_number)} Regions")
    while True:
        chosen_region = input("Choose a region based on its index: ")
        try:
            chosen_region = int(chosen_region)
            chosen_region = chosen_region - 1
            if 0 <= chosen_region < len(list_of_regions):
                break
            else:
                print("Invalid number, the number must be between 1 and "+ str(len(list_of_regions)))
        except ValueError:
            print("Invalid Option, use a valid number")
            continue

    return list_of_regions[chosen_region]

def client_config(region):
    """
    Create a botocore Config object for a specific AWS region.

    Args:
        region (str): AWS region name.

    Returns:
        botocore.config.Config | None: Configured AWS client configuration.
    """
    if not region:
        print("You did not choose a region")
        return None

    aws_config = Config(
        region_name=region,
        retries={"max_attempts": 5,
                 "mode": "standard"
                 },
    )
    return aws_config

def rebuild_ec2_config_for_region(session):
    """
    Rebuild the EC2 client configuration after selecting a new region.

    Args:
        session (boto3.Session): Active boto3 session.

    Returns:
        tuple:
            - botocore.config.Config
            - str (selected region)
    """
    regions = available_regions(session)
    selected_region = choose_region(regions)
    aws_config = client_config(selected_region)
    return aws_config, selected_region

def get_client(session, aws_config):
    """
    Create an EC2 client using the provided session and configuration.

    Args:
        session (boto3.Session): Active boto3 session.
        aws_config (botocore.config.Config): AWS client configuration.

    Returns:
        boto3.client: EC2 client.
    """
    client = session.client("ec2", config=aws_config)
    return client

def run_client_flow():
    """
    Main workflow for building an EC2 client.

    This function:
        1. Selects an AWS profile
        2. Selects an AWS region
        3. Builds the EC2 client

    Returns:
        tuple:
            - boto3.client (EC2 client)
            - boto3.Session (active session)
    """
    session = ask_for_profile()
    regions = available_regions(session)
    region = choose_region(regions)
    aws_config = client_config(region)
    client = get_client(session,aws_config)
    return client, session