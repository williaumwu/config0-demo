class Main(newSchedStack):

    def __init__(self,stackargs):

        newSchedStack.__init__(self,stackargs)

        # general
        self.parse.add_optional(key="aws_default_region",
                                 default="eu-west-1",
                                 types="str")

        self.parse.add_required(key="env_name",
                                 types="str")

        self.parse.add_optional(key="cloud_tags_hash",
                                 types="str")

        self.parse.add_optional(key="public_subnet_ids",
                                 default="null",
                                 types="str")

        self.parse.add_optional(key="private_subnet_ids",
                                 default="null",
                                 types="str")

        # variable set
        self.parse.add_optional(key="vars_set_labels_hash",
                                default='null',
                                types="str")

        self.parse.add_optional(key="vars_set_arguments_hash",
                                default='null',
                                types="str")

        # nat instance vars
        self.parse.add_optional(key="private_route_table_id",
                                default="null",
                                types="str")

        # sensible defaults
        self.parse.add_optional(key="nat_instance_types",
                                types="str",
                                default="t3.nano,t3a.nano")

        self.parse.add_optional(key="nat_cidr_ingress_accept",
                                types="str",
                                default="0.0.0.0/0")

        # rds
        self.parse.add_required(key="db_sg_id",
                                 types="str")

        self.parse.add_optional(key="db_allocated_storage",
                                 default=30,
                                 types="int")

        self.parse.add_optional(key="db_engine",
                                 default="MySQL",
                                 types="str")

        self.parse.add_optional(key="db_engine_version",
                                 default="8.0.35",
                                 types="float")

        self.parse.add_optional(key="db_instance_class",
                                 default="db.t3.micro",
                                 types="str")

        self.parse.add_optional(key="db_multi_az",
                                 default="false",
                                 types="bool")

        self.parse.add_optional(key="db_storage_type",
                                 default="gp2",
                                 types="str")

        self.parse.add_optional(key="db_master_username",
                                 default=None,
                                 types="str")

        self.parse.add_optional(key="db_master_password",
                                 default=None,
                                 types="str")

        # eks
        self.parse.add_required(key="vpc_id",
                                 types="str")

        self.parse.add_optional(key="eks_cluster_version",
                                 types="str",
                                 default="1.29")

        self.parse.add_optional(key="eks_cluster_sg_id",
                                 default="null",
                                 types="str")

        self.parse.add_optional(key="eks_node_role_arn",
                                 default="null",
                                 types="str")

        self.parse.add_optional(key="eks_node_max_capacity",
                                 default=1,
                                 types="int")

        self.parse.add_optional(key="eks_node_min_capacity",
                                 default=1,
                                 types="int")

        self.parse.add_optional(key="eks_node_desired_capacity",
                                 default=1,
                                 types="int")

        self.parse.add_optional(key="eks_node_disksize",
                                 default=25,
                                 types="int")

        self.parse.add_optional(key="eks_node_instance_types",
                                 default=["t3.medium","t3.large"],
                                 types="list")

        self.parse.add_optional(key="eks_node_ami_type",
                                 default="AL2_x86_64",
                                 types="str")

        # add substack
        self.stack.add_substack("williaumwu:::network")
        self.stack.add_substack("williaumwu:::rds_eks")

        self.stack.init_substacks()


    def _set_vars(self):

        self.stack.set_variable("eks_cluster",
                                f'{self.stack.env_name}-eks')

    def run_network(self):

        self.stack.init_variables()
        self.stack.verify_variables()
        self._set_vars()

        arguments = {
            "env_name": self.stack.env_name,
            "eks_cluster": self.stack.eks_cluster,
            "aws_default_region": self.stack.aws_default_region,
            "vpc_id": self.stack.vpc_id,
            "public_subnet_ids": self.stack.public_subnet_ids,
            "private_route_table_id": self.stack.private_route_table_id,
            "nat_instance_types": self.stack.nat_instance_types,
            "nat_cidr_ingress_accept": self.stack.nat_cidr_ingress_accept,
            "vars_set_labels_hash": self.stack.vars_set_labels_hash,
            "vars_set_arguments_hash": self.stack.vars_set_arguments_hash,
            "cloud_tags_hash": self.stack.cloud_tags_hash
            }

        inputargs = {
            "arguments": arguments,
            "automation_phase": "infrastructure",
            "human_description": "create network"
        }

        return self.stack.network.insert(display=True,
                                         **inputargs)

    def run_rds_eks(self):

        self.stack.init_variables()
        self.stack.verify_variables()
        self._set_vars()

        arguments = {
            "env_name": self.stack.env_name,
            "eks_cluster": self.stack.eks_cluster,
            "vpc_id": self.stack.vpc_id,
            "public_subnet_ids": self.stack.public_subnet_ids,
            "private_subnet_ids": self.stack.private_subnet_ids,
            "private_route_table_id": self.stack.private_route_table_id,
            "db_sg_id": self.stack.db_sg_id,
            "db_engine": self.stack.db_engine,
            "db_engine_version": self.stack.db_engine_version,
            "db_allocated_storage": self.stack.db_allocated_storage,
            "db_instance_class": self.stack.db_instance_class,
            "eks_cluster_sg_id": self.stack.eks_cluster_sg_id,
            "eks_node_role_arn": self.stack.eks_node_role_arn,
            "cloud_tags_hash": self.stack.cloud_tags_hash,
        }

        if self.stack.db_master_username:
            arguments["master_username"] = self.stack.db_master_username

        if self.stack.db_master_password:
            arguments["master_password"] = self.stack.db_master_password

        if self.stack.eks_cluster_sg_id:
            arguments["eks_cluster_sg_id"] = self.stack.eks_cluster_sg_id

        inputargs = {
            "arguments": arguments,
            "automation_phase": "infrastructure",
            "human_description": "create rds/eks"
        }

        return self.stack.rds_eks.insert(display=True,
                                         **inputargs)

    def run(self):

        self.stack.unset_parallel(sched_init=True)
        self.add_job("network")
        self.add_job("rds_eks")

        return self.finalize_jobs()

    def schedule(self):

        sched = self.new_schedule()
        sched.job = "network"
        sched.archive.timeout = 2700
        sched.archive.timewait = 180
        sched.conditions.retries = 1
        sched.automation_phase = "infrastructure"
        sched.human_description = "creates network"
        sched.on_success = [ "rds_eks" ]
        self.add_schedule()

        sched = self.new_schedule()
        sched.job = "rds_eks"
        sched.archive.timeout = 2700
        sched.archive.timewait = 180
        sched.automation_phase = "infrastructure"
        sched.human_description = 'create rds/eks'
        self.add_schedule()

        return self.get_schedules()