BEGIN;
DROP TABLE `records_record`;
DROP TABLE `records_userprofile`;
CREATE TABLE `records_userprofile` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `user_name` varchar(20) NOT NULL,
    `nick_name` varchar(60) NOT NULL,
    `school` varchar(60) NOT NULL,
    `college` varchar(60) NOT NULL,
    `graduation_year` varchar(20) NOT NULL
)
;
ALTER TABLE `records_userprofile` ADD CONSTRAINT `user_id_refs_id_5b7b4340` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `records_record` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `orig_record_id` integer NOT NULL,
    `companyname_cn` varchar(30),
    `companyname_en` varchar(40),
    `city` varchar(10),
    `post` varchar(20),
    `date_time` datetime,
    `location` varchar(60),
    `state` varchar(10),
    `remark` varchar(200),
    `timestamp` datetime NOT NULL
)
;
ALTER TABLE `records_record` ADD CONSTRAINT `user_id_refs_id_617e04b4` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE INDEX `records_userprofile_403f60f` ON `records_userprofile` (`user_id`);
CREATE INDEX `records_record_403f60f` ON `records_record` (`user_id`);
COMMIT;
