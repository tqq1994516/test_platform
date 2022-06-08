-- upgrade --
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `t_users` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'id 主键',
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `c_time` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `u_time` DATETIME(6)   COMMENT '最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `username` VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    `password` VARCHAR(50) NOT NULL  COMMENT '密码',
    `first_name` VARCHAR(50)   COMMENT '姓',
    `last_name` VARCHAR(50)   COMMENT '名',
    `mobile` VARCHAR(11)  UNIQUE COMMENT '手机号',
    `email` VARCHAR(50)   COMMENT '邮箱',
    `gender` SMALLINT NOT NULL  COMMENT '性别' DEFAULT 1,
    `is_active` BOOL NOT NULL  COMMENT '是否激活' DEFAULT 1,
    `is_online` BOOL NOT NULL  COMMENT '是否在线' DEFAULT 0,
    `is_super_master` BOOL NOT NULL  COMMENT '是否超管' DEFAULT 0,
    `is_system_master` BOOL NOT NULL  COMMENT '是否管理员' DEFAULT 0,
    `owner_id` BIGINT COMMENT '创建者',
    CONSTRAINT `fk_t_users_t_users_dbdb52ca` FOREIGN KEY (`owner_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='用户信息表';
CREATE TABLE IF NOT EXISTS `t_project_info` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'id 主键',
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `c_time` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `u_time` DATETIME(6)   COMMENT '最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `name` VARCHAR(50) NOT NULL UNIQUE COMMENT '项目名称',
    `description` LONGTEXT   COMMENT '项目描述',
    `owner_id` BIGINT COMMENT '创建者',
    CONSTRAINT `fk_t_projec_t_users_6090e3ba` FOREIGN KEY (`owner_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='项目信息表';
CREATE TABLE IF NOT EXISTS `t_envs` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'id 主键',
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `c_time` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `u_time` DATETIME(6)   COMMENT '最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `name` VARCHAR(50) NOT NULL  COMMENT '环境名称',
    `description` LONGTEXT   COMMENT '环境描述',
    `domain` VARCHAR(150) NOT NULL UNIQUE COMMENT '环境域名',
    `owner_id` BIGINT COMMENT '创建者',
    `project_id` BIGINT COMMENT '所属项目',
    CONSTRAINT `fk_t_envs_t_users_7bfc4d5e` FOREIGN KEY (`owner_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_t_envs_t_projec_0db4f5b7` FOREIGN KEY (`project_id`) REFERENCES `t_project_info` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='运行环境表';
CREATE TABLE IF NOT EXISTS `t_versions` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'id 主键',
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `c_time` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `u_time` DATETIME(6)   COMMENT '最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `version_num` VARCHAR(50) NOT NULL  COMMENT '版本号',
    `start_time` DATETIME(6)   COMMENT '开始时间',
    `end_time` DATETIME(6)   COMMENT '结束时间',
    `is_activate` BOOL NOT NULL  COMMENT '是否激活' DEFAULT 1,
    `is_newest` BOOL NOT NULL  COMMENT '是否最新' DEFAULT 1,
    `owner_id` BIGINT COMMENT '创建者',
    `project_id` BIGINT COMMENT '所属项目',
    CONSTRAINT `fk_t_versio_t_users_8a222a2f` FOREIGN KEY (`owner_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_t_versio_t_envs_0da62359` FOREIGN KEY (`project_id`) REFERENCES `t_envs` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='软件版本表';
CREATE TABLE IF NOT EXISTS `t_apps` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'id 主键',
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `c_time` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `u_time` DATETIME(6)   COMMENT '最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `name` VARCHAR(50) NOT NULL UNIQUE COMMENT '应用名称',
    `description` VARCHAR(150)   COMMENT '应用描述' DEFAULT '',
    `owner_id` BIGINT COMMENT '创建者',
    CONSTRAINT `fk_t_apps_t_users_a3f010c5` FOREIGN KEY (`owner_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='应用信息表';
CREATE TABLE IF NOT EXISTS `t_groups` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'id 主键',
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `c_time` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `u_time` DATETIME(6)   COMMENT '最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `name` VARCHAR(50) NOT NULL UNIQUE COMMENT '用户组名称',
    `description` VARCHAR(150)   COMMENT '用户组描述' DEFAULT '',
    `owner_id` BIGINT COMMENT '创建者',
    CONSTRAINT `fk_t_groups_t_users_54c5145e` FOREIGN KEY (`owner_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='用户组表';
CREATE TABLE IF NOT EXISTS `t_models` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'id 主键',
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `c_time` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `u_time` DATETIME(6)   COMMENT '最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `name` VARCHAR(50) NOT NULL UNIQUE COMMENT '模块名称',
    `description` VARCHAR(150)   COMMENT '模块描述' DEFAULT '',
    `owner_id` BIGINT COMMENT '创建者',
    CONSTRAINT `fk_t_models_t_users_f8163271` FOREIGN KEY (`owner_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='模块信息表';
CREATE TABLE IF NOT EXISTS `t_permissions` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'id 主键',
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `c_time` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `u_time` DATETIME(6)   COMMENT '最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `name` VARCHAR(50) NOT NULL  COMMENT '权限名称',
    `description` VARCHAR(150)   COMMENT '权限描述' DEFAULT '',
    `models_id` BIGINT COMMENT '所属模块',
    `owner_id` BIGINT COMMENT '创建者',
    CONSTRAINT `fk_t_permis_t_models_ffba397b` FOREIGN KEY (`models_id`) REFERENCES `t_models` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_t_permis_t_users_56d66a21` FOREIGN KEY (`owner_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='权限表';
CREATE TABLE IF NOT EXISTS `t_roles` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'id 主键',
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `c_time` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `u_time` DATETIME(6)   COMMENT '最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `name` VARCHAR(50) NOT NULL UNIQUE COMMENT '角色名称',
    `description` VARCHAR(150)   COMMENT '角色描述' DEFAULT '',
    `owner_id` BIGINT COMMENT '创建者',
    CONSTRAINT `fk_t_roles_t_users_18d6ad79` FOREIGN KEY (`owner_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='角色表';
CREATE TABLE IF NOT EXISTS `t_tags` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'id 主键',
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `c_time` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `u_time` DATETIME(6)   COMMENT '最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `name` VARCHAR(50) NOT NULL UNIQUE COMMENT '标签名称',
    `tag_type` SMALLINT NOT NULL  COMMENT '标签类型',
    `description` VARCHAR(150)   COMMENT '标签描述' DEFAULT '',
    `owner_id` BIGINT COMMENT '创建者',
    CONSTRAINT `fk_t_tags_t_users_6098ab92` FOREIGN KEY (`owner_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='标签表';
CREATE TABLE IF NOT EXISTS `t_testcase_sites` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'id 主键',
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `c_time` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `u_time` DATETIME(6)   COMMENT '最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `name` VARCHAR(50) NOT NULL UNIQUE COMMENT '用例集名称',
    `description` VARCHAR(150)   COMMENT '用例集描述' DEFAULT '',
    `priority` SMALLINT NOT NULL  COMMENT '优先级' DEFAULT 2,
    `owner_id` BIGINT COMMENT '创建者',
    `project_id` BIGINT COMMENT '所属项目',
    CONSTRAINT `fk_t_testca_t_users_80cef72b` FOREIGN KEY (`owner_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_t_testca_t_projec_a06e71bf` FOREIGN KEY (`project_id`) REFERENCES `t_project_info` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='用例集信息表';
CREATE TABLE IF NOT EXISTS `t_testcases` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'id 主键',
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `c_time` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `u_time` DATETIME(6)   COMMENT '最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `name` VARCHAR(50) NOT NULL  COMMENT '用例名称',
    `testcase_type` SMALLINT NOT NULL  COMMENT '用例类型',
    `priority` SMALLINT NOT NULL  COMMENT '优先级' DEFAULT 2,
    `review` SMALLINT NOT NULL  COMMENT '评审状态' DEFAULT 2,
    `result` SMALLINT NOT NULL  COMMENT '执行状态' DEFAULT 1,
    `level` SMALLINT NOT NULL  COMMENT '用例级别' DEFAULT 0,
    `owner_id` BIGINT COMMENT '创建者',
    `testcase_site_id` BIGINT COMMENT '所属用例集',
    CONSTRAINT `fk_t_testca_t_users_a1a48704` FOREIGN KEY (`owner_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_t_testca_t_testca_12730f6b` FOREIGN KEY (`testcase_site_id`) REFERENCES `t_testcase_sites` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='用例信息表';
CREATE TABLE IF NOT EXISTS `t_testcase_change_logs` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'id 主键',
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `c_time` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `u_time` DATETIME(6)   COMMENT '最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `change_field` VARCHAR(50) NOT NULL  COMMENT '修改字段',
    `before` LONGTEXT NOT NULL  COMMENT '修改前',
    `after` LONGTEXT NOT NULL  COMMENT '修改后',
    `owner_id` BIGINT COMMENT '创建者',
    `testcase_id` BIGINT COMMENT '关联用例',
    CONSTRAINT `fk_t_testca_t_users_e93f5e87` FOREIGN KEY (`owner_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_t_testca_t_testca_cb59a410` FOREIGN KEY (`testcase_id`) REFERENCES `t_testcases` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='用例变更历史表';
CREATE TABLE IF NOT EXISTS `t_testcase_comments` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'id 主键',
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `c_time` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `u_time` DATETIME(6)   COMMENT '最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `comment` LONGTEXT NOT NULL  COMMENT '备注',
    `owner_id` BIGINT COMMENT '创建者',
    `testcase_id` BIGINT COMMENT '关联用例',
    CONSTRAINT `fk_t_testca_t_users_15410986` FOREIGN KEY (`owner_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_t_testca_t_testca_a8b4ddf9` FOREIGN KEY (`testcase_id`) REFERENCES `t_testcases` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='用例备注表';
CREATE TABLE IF NOT EXISTS `t_testcase_dependence` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'id 主键',
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `c_time` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `u_time` DATETIME(6)   COMMENT '最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `is_front` BOOL NOT NULL  COMMENT '是否前置' DEFAULT 1,
    `is_back` BOOL NOT NULL  COMMENT '是否后置' DEFAULT 0,
    `sort` INT NOT NULL  COMMENT '排序' DEFAULT 0,
    `owner_id` BIGINT COMMENT '创建者',
    `testcase_id` BIGINT COMMENT '关联用例',
    CONSTRAINT `fk_t_testca_t_users_a90287bb` FOREIGN KEY (`owner_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_t_testca_t_testca_b6004b8f` FOREIGN KEY (`testcase_id`) REFERENCES `t_testcases` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='用例关系表';
CREATE TABLE IF NOT EXISTS `t_testcase_detail` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'id 主键',
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `c_time` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `u_time` DATETIME(6)   COMMENT '最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `precondition` LONGTEXT   COMMENT '前置条件',
    `operation_steps_type` SMALLINT NOT NULL  COMMENT '操作步骤类型',
    `operation_steps` LONGTEXT NOT NULL  COMMENT '文本操作步骤',
    `owner_id` BIGINT COMMENT '创建者',
    `testcase_id` BIGINT COMMENT '关联用例',
    CONSTRAINT `fk_t_testca_t_users_300504b7` FOREIGN KEY (`owner_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_t_testca_t_testca_6ae6047e` FOREIGN KEY (`testcase_id`) REFERENCES `t_testcases` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='用例详情表';
CREATE TABLE IF NOT EXISTS `t_testcase_execute_records` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'id 主键',
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `c_time` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `u_time` DATETIME(6)   COMMENT '最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `execute_time` DATETIME(6)   COMMENT '执行时间',
    `execute_result` VARCHAR(50) NOT NULL  COMMENT '执行结果',
    `execute_type` SMALLINT NOT NULL  COMMENT '执行类型',
    `owner_id` BIGINT COMMENT '创建者',
    `testcase_id` BIGINT COMMENT '关联用例',
    CONSTRAINT `fk_t_testca_t_users_a88e6d74` FOREIGN KEY (`owner_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_t_testca_t_testca_8e5c7c56` FOREIGN KEY (`testcase_id`) REFERENCES `t_testcases` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='用例执行记录表';
CREATE TABLE IF NOT EXISTS `t_testcase_execute_logs` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'id 主键',
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `c_time` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `u_time` DATETIME(6)   COMMENT '最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `log_path` LONGTEXT NOT NULL  COMMENT '日志存储地址',
    `execute_record_id` BIGINT COMMENT '关联运行记录',
    `owner_id` BIGINT COMMENT '创建者',
    `testcase_id` BIGINT COMMENT '关联用例',
    CONSTRAINT `fk_t_testca_t_testca_e155c3ee` FOREIGN KEY (`execute_record_id`) REFERENCES `t_testcase_execute_records` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_t_testca_t_users_bf22402e` FOREIGN KEY (`owner_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_t_testca_t_testca_e4aee0d1` FOREIGN KEY (`testcase_id`) REFERENCES `t_testcases` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='用例执行日志表';
CREATE TABLE IF NOT EXISTS `t_testcase_files` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'id 主键',
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `c_time` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `u_time` DATETIME(6)   COMMENT '最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `file_path` VARCHAR(200) NOT NULL  COMMENT '文件地址',
    `owner_id` BIGINT COMMENT '创建者',
    `testcase_id` BIGINT COMMENT '关联用例',
    CONSTRAINT `fk_t_testca_t_users_684acb7a` FOREIGN KEY (`owner_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_t_testca_t_testca_e009a49c` FOREIGN KEY (`testcase_id`) REFERENCES `t_testcases` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='用例附件表';
CREATE TABLE IF NOT EXISTS `t_testcase_operation_steps` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'id 主键',
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `c_time` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `u_time` DATETIME(6)   COMMENT '最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `operation_steps` LONGTEXT NOT NULL  COMMENT '分步操作步骤',
    `sort` INT NOT NULL  COMMENT '排序' DEFAULT 0,
    `owner_id` BIGINT COMMENT '创建者',
    `testcase_id` BIGINT COMMENT '关联用例',
    CONSTRAINT `fk_t_testca_t_users_f0069b23` FOREIGN KEY (`owner_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_t_testca_t_testca_8cff396b` FOREIGN KEY (`testcase_id`) REFERENCES `t_testcases` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='用例操作步骤表';
CREATE TABLE IF NOT EXISTS `t_bugs` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'id 主键',
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `c_time` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `u_time` DATETIME(6)   COMMENT '最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `name` VARCHAR(50) NOT NULL  COMMENT '缺陷名称',
    `related_id` BIGINT NOT NULL  COMMENT '关联id',
    `owner_id` BIGINT COMMENT '创建者',
    CONSTRAINT `fk_t_bugs_t_users_9a8c752b` FOREIGN KEY (`owner_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='缺陷信息表';
CREATE TABLE IF NOT EXISTS `t_tasks` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'id 主键',
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `c_time` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `u_time` DATETIME(6)   COMMENT '最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `name` VARCHAR(50) NOT NULL  COMMENT '需求名称',
    `related_id` BIGINT NOT NULL  COMMENT '关联id',
    `owner_id` BIGINT COMMENT '创建者',
    CONSTRAINT `fk_t_tasks_t_users_585078c3` FOREIGN KEY (`owner_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='需求信息表';
CREATE TABLE IF NOT EXISTS `t_users_apps` (
    `t_users_id` BIGINT NOT NULL,
    `apps_id` BIGINT NOT NULL,
    FOREIGN KEY (`t_users_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`apps_id`) REFERENCES `t_apps` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='开通应用';
CREATE TABLE IF NOT EXISTS `t_users_groups` (
    `t_users_id` BIGINT NOT NULL,
    `groups_id` BIGINT NOT NULL,
    FOREIGN KEY (`t_users_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`groups_id`) REFERENCES `t_groups` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='用户组';
CREATE TABLE IF NOT EXISTS `t_users_models` (
    `t_users_id` BIGINT NOT NULL,
    `models_id` BIGINT NOT NULL,
    FOREIGN KEY (`t_users_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`models_id`) REFERENCES `t_models` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='开通模块';
CREATE TABLE IF NOT EXISTS `t_project_masters` (
    `t_project_info_id` BIGINT NOT NULL,
    `users_id` BIGINT NOT NULL,
    FOREIGN KEY (`t_project_info_id`) REFERENCES `t_project_info` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`users_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='管理员';
CREATE TABLE IF NOT EXISTS `t_project_members` (
    `t_project_info_id` BIGINT NOT NULL,
    `users_id` BIGINT NOT NULL,
    FOREIGN KEY (`t_project_info_id`) REFERENCES `t_project_info` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`users_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='项目成员';
CREATE TABLE IF NOT EXISTS `t_groups_t_roles` (
    `t_groups_id` BIGINT NOT NULL,
    `roles_id` BIGINT NOT NULL,
    FOREIGN KEY (`t_groups_id`) REFERENCES `t_groups` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`roles_id`) REFERENCES `t_roles` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='角色';
CREATE TABLE IF NOT EXISTS `t_roles_t_permissions` (
    `t_roles_id` BIGINT NOT NULL,
    `permissions_id` BIGINT NOT NULL,
    FOREIGN KEY (`t_roles_id`) REFERENCES `t_roles` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`permissions_id`) REFERENCES `t_permissions` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='权限';
CREATE TABLE IF NOT EXISTS `t_testcase_sites_t_tags` (
    `t_testcase_sites_id` BIGINT NOT NULL,
    `tags_id` BIGINT NOT NULL,
    FOREIGN KEY (`t_testcase_sites_id`) REFERENCES `t_testcase_sites` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`tags_id`) REFERENCES `t_tags` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='标签';
CREATE TABLE IF NOT EXISTS `t_testcase_executors` (
    `t_testcases_id` BIGINT NOT NULL,
    `users_id` BIGINT NOT NULL,
    FOREIGN KEY (`t_testcases_id`) REFERENCES `t_testcases` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`users_id`) REFERENCES `t_users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='执行人';
CREATE TABLE IF NOT EXISTS `t_testcases_t_tags` (
    `t_testcases_id` BIGINT NOT NULL,
    `tags_id` BIGINT NOT NULL,
    FOREIGN KEY (`t_testcases_id`) REFERENCES `t_testcases` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`tags_id`) REFERENCES `t_tags` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='标签';
CREATE TABLE IF NOT EXISTS `t_testcase_detail_testcases` (
    `t_testcase_detail_id` BIGINT NOT NULL,
    `testcases_id` BIGINT NOT NULL,
    FOREIGN KEY (`t_testcase_detail_id`) REFERENCES `t_testcase_detail` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`testcases_id`) REFERENCES `t_testcases` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='关联用例';
CREATE TABLE IF NOT EXISTS `t_testcase_detail_tasks` (
    `t_testcase_detail_id` BIGINT NOT NULL,
    `tasks_id` BIGINT NOT NULL,
    FOREIGN KEY (`t_testcase_detail_id`) REFERENCES `t_testcase_detail` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`tasks_id`) REFERENCES `t_tasks` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='关联需求';
CREATE TABLE IF NOT EXISTS `t_testcase_detail_bugs` (
    `t_testcase_detail_id` BIGINT NOT NULL,
    `bugs_id` BIGINT NOT NULL,
    FOREIGN KEY (`t_testcase_detail_id`) REFERENCES `t_testcase_detail` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`bugs_id`) REFERENCES `t_bugs` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='关联缺陷';
