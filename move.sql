/*
Navicat MySQL Data Transfer

Source Server         : 106.13.206.82（我的）
Source Server Version : 50726
Source Host           : 106.13.206.82:3306
Source Database       : move

Target Server Type    : MYSQL
Target Server Version : 50726
File Encoding         : 65001

Date: 2019-12-04 10:42:45
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for move_class
-- ----------------------------
DROP TABLE IF EXISTS `move_class`;
CREATE TABLE `move_class` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL COMMENT '类型名(电影，综艺等等)',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='资源大类';

-- ----------------------------
-- Table structure for move_district
-- ----------------------------
DROP TABLE IF EXISTS `move_district`;
CREATE TABLE `move_district` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL COMMENT '地区名(美国，韩国等等)',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='资源地区';

-- ----------------------------
-- Table structure for move_error
-- ----------------------------
DROP TABLE IF EXISTS `move_error`;
CREATE TABLE `move_error` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(500) DEFAULT NULL,
  `platform` varchar(255) DEFAULT NULL COMMENT '平台ID',
  `error` longtext,
  `line` varchar(50) DEFAULT NULL,
  `file` varchar(255) DEFAULT NULL,
  `url` varchar(500) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10545 DEFAULT CHARSET=utf8 COMMENT='异常记录表';

-- ----------------------------
-- Table structure for move_follow
-- ----------------------------
DROP TABLE IF EXISTS `move_follow`;
CREATE TABLE `move_follow` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `openid` varchar(300) DEFAULT NULL,
  `move_id` int(11) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8 COMMENT='关注表';

-- ----------------------------
-- Table structure for move_location
-- ----------------------------
DROP TABLE IF EXISTS `move_location`;
CREATE TABLE `move_location` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `openid` varchar(300) DEFAULT NULL,
  `longitude` varchar(300) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `latitude` varchar(300) DEFAULT NULL,
  `data` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8 COMMENT='位置记录表';

-- ----------------------------
-- Table structure for move_meijutt
-- ----------------------------
DROP TABLE IF EXISTS `move_meijutt`;
CREATE TABLE `move_meijutt` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(500) DEFAULT NULL,
  `href` varchar(500) DEFAULT NULL,
  `img` varchar(500) DEFAULT NULL,
  `video` varchar(500) DEFAULT NULL,
  `content` text,
  `create_time` datetime DEFAULT NULL,
  `year` varchar(500) DEFAULT NULL COMMENT '年份',
  `director` varchar(500) DEFAULT NULL COMMENT '导演',
  `actor` varchar(500) DEFAULT NULL COMMENT '演员',
  `score` double(3,1) DEFAULT NULL COMMENT '评分',
  `type` varchar(255) DEFAULT NULL COMMENT '类型',
  `result` longtext COMMENT 'js路径',
  `is_update` tinyint(4) DEFAULT '0' COMMENT '0:不更新，1:还更新',
  `platform` tinyint(4) DEFAULT NULL COMMENT '平台1:美剧天堂',
  `update_title` varchar(500) DEFAULT NULL COMMENT '更新至标题',
  `update_time` datetime DEFAULT NULL,
  `hot` tinyint(3) DEFAULT NULL COMMENT '推荐标识',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`,`href`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=7720 DEFAULT CHARSET=utf8 COMMENT='美剧吧';

-- ----------------------------
-- Table structure for move_move
-- ----------------------------
DROP TABLE IF EXISTS `move_move`;
CREATE TABLE `move_move` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL COMMENT '电影名',
  `number` int(5) DEFAULT NULL COMMENT '第几集',
  `douban_grade` char(5) DEFAULT NULL COMMENT '豆瓣评分',
  `year` int(4) DEFAULT NULL COMMENT '年份',
  `class` tinyint(3) DEFAULT NULL COMMENT '剧类型（大类）',
  `type` tinyint(3) DEFAULT NULL COMMENT '剧类型（小类）',
  `district` tinyint(3) DEFAULT NULL COMMENT '地区类型',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='资源';

-- ----------------------------
-- Table structure for move_move_video
-- ----------------------------
DROP TABLE IF EXISTS `move_move_video`;
CREATE TABLE `move_move_video` (
  `move_id` int(10) DEFAULT NULL,
  `name` varchar(500) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL COMMENT '视频资源',
  `number` int(11) DEFAULT NULL COMMENT '排序',
  `create_time` datetime DEFAULT NULL,
  `title` varchar(500) DEFAULT NULL COMMENT '视频资源标题(例如1080高清中字)',
  `password` varchar(255) DEFAULT NULL COMMENT '百度网盘：密码',
  `type` tinyint(3) DEFAULT NULL COMMENT '1：云播，2:云播2,3百度云盘'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='资源地址';

-- ----------------------------
-- Table structure for move_search
-- ----------------------------
DROP TABLE IF EXISTS `move_search`;
CREATE TABLE `move_search` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `openid` varchar(300) DEFAULT NULL,
  `name` varchar(300) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8 COMMENT='查询记录表';

-- ----------------------------
-- Table structure for move_type
-- ----------------------------
DROP TABLE IF EXISTS `move_type`;
CREATE TABLE `move_type` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL COMMENT '小类型名(动作，爱情等等)',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='资源小类';

-- ----------------------------
-- Table structure for move_user
-- ----------------------------
DROP TABLE IF EXISTS `move_user`;
CREATE TABLE `move_user` (
  `openid` varchar(300) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `last_login_time` datetime DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `language` varchar(255) DEFAULT NULL,
  `gender` varchar(255) DEFAULT NULL,
  `province` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户表';

-- ----------------------------
-- Table structure for move_wacth
-- ----------------------------
DROP TABLE IF EXISTS `move_wacth`;
CREATE TABLE `move_wacth` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `openid` varchar(300) DEFAULT NULL,
  `move_id` int(11) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8 COMMENT='观看表';
