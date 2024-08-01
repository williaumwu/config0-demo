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
        # config0-publish:::config0_core::empty_stack
        self.stack.add_substack("config0-publish:::empty_stack")
        self.stack.add_substack("config0-publish:::aws_rds")
        self.stack.add_substack("config0-publish:::aws_eks")

        self.stack.init_substacks()

    def _set_vars(self):

        self.stack.init_variables()
        self.stack.verify_variables()

        self.stack.set_variable("rds_name",
                                rds_name = f'{self.stack.env_name}-rds')

        self.stack.set_variable("eks_cluster",
                                eks_cluster = f'{self.stack.env_name}-eks')

    def run_start_sched(self):

        self.stack.init_variables()

        description="start job for schedule",

        inputargs = {
            "arguments": {"description":description},
            "automation_phase": "infrastructure",
            "human_description": 'start of sched jobs'
        }

        return self.stack.empty_stack.insert(display=True,
                                             **inputargs)

    def run_rds(self):

        self._set_names()

        arguments = {
            "aws_default_region": self.stack.aws_default_region,
            "sg_id": self.stack.db_sg_id,
            "subnet_ids": self.stack.private_subnet_ids,
            "allocated_storage": self.stack.db_allocated_storage,
            "engine": self.stack.db_engine,
            "engine_version": self.stack.db_engine_version,
            "instance_class": self.stack.db_instance_class,
            "storage_type": self.stack.db_storage_type,
            "publicly_accessible":False,
            "storage_encrypted":True,
            "cloud_tags_hash": self.stack.cloud_tags_hash,
            "rds_name": self.stack.rds_name,
        }
        if self.stack.db_multi_az:
            arguments["multi_az"] = self.stack.db_multi_az

        if self.stack.db_master_username:
            arguments["master_username"] = self.stack.db_master_username

        if self.stack.db_master_password:
            arguments["master_password"] = self.stack.db_master_password

        inputargs = {
            "arguments": arguments,
            "automation_phase": "infrastructure",
            "human_description": f'create rds "{self.stack.rds_name}"'
        }

        return self.stack.aws_rds.insert(display=True,
                                         **inputargs)

    def run_eks(self):

        self._set_names()

        arguments = {
            "aws_default_region": self.stack.aws_default_region,
            "vpc_id": self.stack.vpc_id,
            "eks_cluster_version": self.stack.eks_cluster_version,
            "eks_cluster_subnet_ids": self.stack.public_subnet_ids,
            "eks_node_group_subnet_ids": self.stack.private_subnet_ids,
            "eks_node_role_arn": self.stack.eks_node_role_arn,
            "eks_node_max_capacity": self.stack.eks_node_max_capacity,
            "eks_node_min_capacity": self.stack.eks_node_min_capacity,
            "eks_node_desired_capacity": self.stack.eks_node_desired_capacity,
            "eks_node_disksize": self.stack.eks_node_disksize,
            "eks_node_instance_types": self.stack.eks_node_instance_types,
            "eks_node_ami_type": self.stack.eks_node_ami_type,
            "cloud_tags_hash": self.stack.cloud_tags_hash,
            "eks_cluster": self.stack.eks_cluster,
        }

        if self.stack.eks_cluster_sg_id:
            arguments["eks_cluster_sg_id"] = self.stack.eks_cluster_sg_id


        inputargs = {
            "arguments": arguments,
            "automation_phase": "infrastructure",
            "human_description": f'create eks cluster "{self.stack.eks_cluster}"'
        }

        return self.stack.aws_eks.insert(display=True,
                                         **inputargs)

    def run(self):

        self.stack.unset_parallel(sched_init=True)
        self.add_job("start_sched")
        self.add_job("rds")
        self.add_job("eks")

        return self.finalize_jobs()

    def schedule(self):

        sched = self.new_schedule()
        sched.job = "start_sched"
        sched.archive.timeout = 600
        sched.archive.timewait = 60
        sched.automation_phase = "infrastructure"
        sched.human_description = "starts schedule"
        sched.conditions.retries = 1
        sched.on_success = ["rds","eks"]
        self.add_schedule()

        sched = self.new_schedule()
        sched.job = "rds"
        sched.archive.timeout = 1800
        sched.archive.timewait = 120
        sched.automation_phase = "infrastructure"
        sched.human_description = f'create rds "{self.stack.rds_name}"'
        self.add_schedule()

        sched = self.new_schedule()
        sched.job = "eks"
        sched.archive.timeout = 2700
        sched.archive.timewait = 120
        sched.automation_phase = "infrastructure"
        sched.human_description = f'create eks cluster "{self.stack.eks_cluster}"'
        self.add_schedule()

        return self.get_schedules()
