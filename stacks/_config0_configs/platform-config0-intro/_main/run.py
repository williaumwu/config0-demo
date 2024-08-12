def run(stackargs):

    '''
    this is platform example 
    '''

    # instantiate authoring stack
    stack = newStack(stackargs)

    # important to classify this stack
    # as a platform stack/configuration
    stack.set_platform()

    aws_default_region = "eu-west-1"
    billing_tag = "config0-intro-2024"

    general_labels = {
        "environment": "dev",
        "purpose": "config0-intro"
    }

    aws_settings = {
        "name":"aws_settings",
        "values": {
            "aws_default_region": aws_default_region
        }
    }

    # cloud_tags arguments are passed
    # as b64 string as cloud_tags_hash
    cloud_tags = {
        "name":"cloud_tags",
        "values": {
            "cloud_tags_hash": stack.b64_encode({
                **general_labels,
                "billing":billing_tag
            })
        }
    }

    # network related
    network_vars_set_labels_hash = {
        "name":"network_vars_set_labels_hash",
        "values": {
            "labels_hash": stack.b64_encode({
                **general_labels,
                "region": aws_default_region,
                "area": "network",
                "provider": "aws"
            })
        }
    }

    # labels for resources that are added
    general = {
        "name":"general",
        "values":general_labels
    }

    aws_cloud = {
        "name":"aws_cloud",
        "values":{
            "provider":"aws",
            "cloudprovider": "aws"
        }
    }

    # vars set stack specific
    # variable set
    # special selector base
    aws_base_network = {
        "name":"aws_base_network",
        "base":True,   # this indicates this is a base for other selectors
        "values":{
            "matchKeys":{
                "provider":"aws"
            },
            "matchLabels": {
                **general_labels,
                "area": "network"
            },
        }
    }

    network_vars = {
        "name": "network_vars",
        "values": {
            "matchLabels": {
                **general_labels,
                "area": "network",
                "region":aws_default_region,
                "provider":"aws"
            },
        }
    }

    eks_info = {
        "name": "eks_info",
        "values": {
            "matchLabels": {
                **general_labels
            },
            "matchKeys": {
                "provider":"aws",
                "region":aws_default_region
            },
            "matchParams": {
                "resource_type":"eks"
            }
        }
    }

    # vpc/network_vars_set for vpc setting
    stack.add_substack('config0-publish:::aws_vpc_simple',
                       arguments=[
                           cloud_tags,
                           aws_settings
                       ],
                       labels=[
                           general,
                           aws_cloud
                       ])

    # related to mostly vpc
    stack.add_substack('config0-publish:::network_vars_set',
                       arguments=[
                           cloud_tags,
                           network_vars_set_labels_hash
                       ],
                       labels=[
                           general,
                           aws_cloud
                       ],
                       selectors=[
                           aws_base_network
                       ])


    stack.add_substack('config0-publish:::aws_nat_inst_vpc',  # nat instance (instead of nat gw)
                       arguments=[
                           cloud_tags,
                           aws_settings
                       ],
                       labels=[
                           general,
                           aws_cloud
                       ],
                       selectors=[
                           network_vars
                       ])


    # aws stateful stacks
    stack.add_substack('config0-publish:::aws_rds',
                       arguments=[
                           cloud_tags,
                           aws_settings
                       ],
                       labels=[
                           general,
                           aws_cloud
                       ],
                       selectors=[
                           network_vars
                       ])


    # aws kubernetes
    stack.add_substack('config0-publish:::aws_eks',
                       arguments=[
                           cloud_tags,
                           aws_settings
                       ],
                       labels=[
                           general,
                           aws_cloud
                       ],
                       selectors=[
                           network_vars,
                           eks_info
                       ])


    # drift detection of resources
    stack.add_substack('config0-publish:::check_drift_resources',
                       arguments=[cloud_tags],
                       labels=[general])

    stack.init_substacks()

    return stack.get_results()

