# validators flow

def filter_instances(instances_to_filter):
    """
    Filter EC2 instances that are in a state where termination is allowed.

    Args:
        instances_to_filter (list): List of EC2 instance dictionaries.

    Returns:
        list: Instances that are in permitted states.
    """
    instances_list = []
    forbidden_states = ['shutting-down', 'terminated', 'Unknown']

    for instance in instances_to_filter:
        state = instance.get("State")
        if instance.get(state) not in forbidden_states:
            instances_list.append(instance)
    return instances_list

def valid_tag_keys(tag_key, instances_list):
    keys = set()
    for instance in instances_list:
        tags = instance.get("Tags",[])
        if tags:
            for tag in tags:
                key = tag.get("Key")
                keys.add(key)
    if tag_key in keys:
        return True
    else:
        return False

def valid_tag_values(tag_key, tag_value, instances_list):
    values = set()
    for instance in instances_list:
        tags = instance.get("Tags",[])
        if tags:
            for tag in tags:
                key = tag.get("Key")
                if tag_key == key:
                    value = tag.get("Value", "Undefined")
                    values.add(value)
    if tag_value in values:
        return True
    else:
        return False
