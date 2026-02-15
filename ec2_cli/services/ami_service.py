# ami_service flow
def find_ami(ec2):
    # This function searches for the most recent Amazon Linux 2023 AMI (2024 version)
    # using predefined filters such as owner, name pattern, and architecture.
    amis = ec2.describe_images(
    Owners=["amazon"],
    Filters=[
        {"Name": "name", "Values": ["al2023-ami-*2024*"]},
        {"Name": "architecture", "Values": ["x86_64"]},
    ]
)
    # Retrieve the list of images from the response
    images = amis.get("Images", [])
    # If no AMIs are found, raise an exception
    if not images:
        raise RuntimeError("No AMIs found for filter al2023-ami-*2024*")
    # Sort images by creation date (newest first)
    images_sorted = sorted(amis["Images"], key=lambda x: x["CreationDate"], reverse=True)

    # Select the most recent AMI
    image = images_sorted[0]
    print("Using default AMI:", image["ImageId"], image["Name"])
    # Return the AMI ID
    return image["ImageId"]
