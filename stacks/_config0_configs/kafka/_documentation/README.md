**Description**

  - This stack creates a Kafka cluster on AWS using EC2 instances.

**Gotchas**
  - Please note that there is an option to utilize spot instances, which can be more cost-effective. However, it is important to be aware that there is a slight possibility of failure if the spot price is exceptionally low or if there is an interruption in spot capacity.

**Infrastructure**

  - If vpc_id and security group IDs are not explicitly provided, users have the option to use "selectors".
    - NOTE: Using selectors depends on the VPC information being available in the Config0 resources database.

**Required**

| argument      | description                            | var type | default      |
| ------------- | -------------------------------------- | -------- | ------------ |
| kafka_cluster   | the name of the kafka cluster       | string   | None         |
| num_of_zookeeper   | the num of zookeepers for the kafka cluster       | string   | 1         |
| num_of_broker   | the num of brokers for the kafka cluster       | string   | 1         |
| num_of_schema_registry   | the num of schema registries for the kafka cluster       | string   | 1         |
| num_of_connect   | the num of connect nodes for kafka cluster       | string   | 1         |
| num_of_rest   | the num of rest nodes for the kafka cluster       | string   | 1         |
| num_of_ksql   | the num of ksql nodes for the  kafka cluster       | string   | 1         |
| num_of_control_center   | the num of controls centers for the kafka cluster       | string   | 1         |
| vpc_id | the vpc id | string   | None       |
| subnet_ids   | a subnet for the VMs is selected from a list of the provided subnet_ids  | string in csv   | None         |
| sg_id   | the security group id for the VMs       | string   | None         |
| bastion_subnet_ids   | a subnet for the Bastion VM is selected from a list of the provided subnet_ids  | string in csv   | None         |
| bastion_sg_id   | the security group id for the bastion host       | string   | None         |

**Optional**

| argument           | description                            | var type |  default      |
| ------------- | -------------------------------------- | -------- | ------------ |
| spot   | the option to use spot intances. (buyer be aware)    | boolean   | None        |
| ami   | the ami image used for kafka instances      | string   | None        |
| ami_filter   | the ami filter used to search for an image as a base for kafka instances      | string   | None        |
| ami_owner   | the ami owner used to search for an image as a base for kafka instances      | string   | None        |
| bastion_ami   | the ami image used for the bastion config host      | string   | None          |
| bastion_ami_filter   | the ami filter used to search for an image as a base for the bastion host     | string   | None        |
| bastion_ami_owner   | the ami owner used to search for an image as a base for the bastion host      | string   | None        |
| aws_default_region   | the aws region                | string   | us-east-1         |
| instance_type | the instance_type for the VMs | string   | t3.micro       |
| disksize | the disksize for the VM | string   | None       |
| tags | the tags for the kafka cluster in the Config0 resources database | string   | None       |
| labels | the labels for the kafka cluster in the Config0 resources database | string   | None       |
