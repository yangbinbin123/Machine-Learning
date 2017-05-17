DROP DATABASE IF EXISTS `isonUKDB`;
CREATE DATABASE `isonUKDB`;
USE `isonUKDB`;
DROP TABLE IF EXISTS `ukey`;
CREATE TABLE `ukey`(   -- Ukey基本信息表
  `ukid`           INT(64),     -- uk编码
  `jycode`         INT(10),     -- JY 证券代码  InnerCode int 聚源数据库码
  `windcode`       VARCHAR(40), -- wind证券代码 s_info_windcode 'A14630.SZ' wind是字符类型
  `markid`         INT(12),     -- 证券市场ID编码 4096种了
  `exchangeid`     INT(10),     -- 交易所编码
  `secutype1`      INT(4),      -- 证券类型编码,大类型
  `secutype2`      INT(4),      -- 证券类型编码,小类型
  `ccy`            INT(8),      -- 货币类型 8位=256种货币
  `expiremonth`    INT(12),     -- 到期月 12为编码, 按1900.01月为1, 每月增加1,能表示到2241年.如果品种有到期月份,如没有,则为0.
--  详细信息了(uk后32位的分解)        --- 
  `codeid`            INT(16),  -- 证券编码  uk方案的扩展信息中的一种,20位够100万种了,若是股票,基金,国债,则下面字段不会有数据
  `futurespriceid`    INT(12),  -- 期货专用,12位价格码
  `futurestypeid`     INT(12),  -- 期货专用,期货标的编码12位
  `spmonthdiff`       INT(6) ,  -- spread专用, 月份差6位
  `sptypea`           INT(12),  -- spread专用,A品种代码
  `sptypeb`           INT(12),  -- spread专用,B品种代码
  `stockfu_priceid`   INT(12),  -- 个股期权专用,价格码
  `stockfu_typeid`    INT(16),  -- 个股期权专用,标的编码12位
  `exchangerate_ccya` INT(8),   -- 汇率报价A(转出)货币编码
  `exchangerate_ccyb` INT(8),   -- 汇率报价B(转入)货币编码
  `exchangerate_ccy`  INT(8),   -- 汇率报价货币编码(可能是A,B,其他等) 
  `exchratefu_ccya`   INT(8),   -- 汇率期货A(转出)货币编码
  `exchratefu_ccyb`   INT(8),   -- 汇率期货B(转入)货币编码
  `exchratefu_ccy`    INT(8),   -- 汇率期货货币编码(可能是A,B,其他等) 
  PRIMARY KEY (`ukid`)
);

DROP TABLE IF EXISTS `futures_information`;

CREATE TABLE `futures_information`( -- 期货-基本信息表
  `futuresid`        INT(32),       -- 与ukey表的codeid关联
  `markid`           INT(12),       -- 证券市场ID编码 4096种了
  `exchangeid`       INT(10),       -- 交易所编码
  `jycode`           INT(10),       -- JY 证券代码  InnerCode int 聚源数据库码 
  `windcode`         VARCHAR(40),   -- wind证券代码 s_info_windcode '600373.SH' wind是字符类型
  `futypeid2`        INT(4),        -- 期货类型编码,小类型与ukey表的codeid关联
  `contoptionid`     VARCHAR(32),   -- 交易标的编码  大豆 /铜 ..  au
  `contmutil`        VARCHAR(50),   -- 交易单位/合约乘数 
  `priunit`          VARCHAR(50),   -- 报价单位  元/吨 -- 期货才有用
  `ticksize`         VARCHAR(50),   -- 最小变动价位   -- A股 0.01
  `dailychgrange`    VARCHAR(200),  -- 每日涨跌幅度
  `contmonth`        VARCHAR(100),  -- 期货合约月份 --期货才用
  `trdate`           VARCHAR(200),  -- 交易时间 --- 期货使用
  `lasttrdate`       VARCHAR(100),  -- 最后交易日,期货使用
  `lasttrtime`       VARCHAR(100),  -- 最后交易日交易时间 ,期货使用
  `deliverydate`     VARCHAR(100),  -- 交割日期 ,期货使用
  `lastdeliverydate` VARCHAR(100),  -- 最后交割日期 ,期货使用
  `deliverygrade`    INT(10),       -- 交割等级 期货使用
  `deliverymethod`   INT(10),       -- 交割方式 期货使用
  `settpricecode`    INT(10),       -- 期货结算价计算方式分类代码
  `Settpricedesc`    VARCHAR(128),  -- 期货结算价计算方式
  `deliseprice`      DECIMAL(17,2), -- 期货交割结算价
  `conttrrate`       DECIMAL(18,8), -- 合约交易保证金率 期货使用
  `conttrfee`        DECIMAL(17,2), -- 合约交易手续费 期货使用
  `condeliveryfee`   DECIMAL(17,2), -- 合约交割手续费 期货使用
    PRIMARY KEY (`markid`,`futuresid`)
);

DROP TABLE IF EXISTS `shares_information`;

CREATE TABLE `shares_information`(   -- 股票-基本信息表
  `sharesid`    INT(20),      -- 股票编码  与ukey表codeid关联
  `markid`      INT(12),      -- 证券市场ID编码 4096种了
  `exchangeid`  INT(10),      -- 交易所编码
  `jycode`      INT(10),      -- JY 证券代码  InnerCode int 聚源数据库码 
  `windcode`    VARCHAR(40),  -- wind证券代码 s_info_windcode '600373.SH' wind是字符类型
  `chiname`     VARCHAR(200), -- 证券中文名称
  `chinameabbr` VARCHAR(100), -- 证券中文名称缩写
  `engname`     VARCHAR(200), -- 证券英文名称
  `engnameabbr` VARCHAR(50),  -- 证券英文名称缩写
  `secuabbr`    VARCHAR(100), -- 证券简称
  `chispell`    VARCHAR(50),  -- 证券中文拼写
  `listplate`   INT(12),      -- 上市板块
  `Liststate`   INT(12),      -- 上市状态
  `listdate`    CHAR(8),      -- 上市时间
  `delistdate`  CHAR(8),      -- 退市时间
  `updatetime`  DATETIME,     -- 表最近更新时间
  PRIMARY KEY (`markid`,`sharesid`)
);


DROP TABLE IF EXISTS `references_data`;

CREATE TABLE `references_data`( -- 交易相关表 ,交易系统需要的数据   referensdata
  `ukid`           INT(64),       -- 
  `codeid`         INT(20),       -- 证券编码/合约代码
  `compcodeid`     INT(100),      -- 公司代码
  `markid`         INT(12),       -- 证券市场ID
  `exchangeid`     INT(12),       -- 交易所
  `secutype`       INT(4),        -- 证券/期货合约 的类型
  `ccy`            INT(8),        -- 货币种类
  `volume`         DECIMAL(20,0), -- 成交数量 
  `amt`            DECIMAL(20,0), -- 成交金额
  `position`       DECIMAL(17,2), -- 期货持仓,期货才有用
  `positionchange` DECIMAL(17,2), -- 期货持仓变化量,期货才有用
  `preclear`       DECIMAL(17,2), -- 昨日结算价
  `preclose`       DECIMAL(17,2), -- 昨日收盘价
  `open`           DECIMAL(17,2), -- 开盘价
  `high`           DECIMAL(17,2), -- 高点
  `low`            DECIMAL(17,2), -- 低点
  `last`           DECIMAL(17,2), -- 最新价
  `close`          DECIMAL(17,2), -- 收盘价
  `handnums`       INT(11),       -- 每手股数
  `netasset`       DECIMAL(17,2), -- 每股净资产值
  `totalvolume`    DECIMAL(17,2), -- 证券全部股数
  `tradevolume`    DECIMAL(17,2), -- 证券全部流通股数
  `stat`           INT(6),        -- 状态,是否可交易 1正常,2停牌,3其他
  `suspendtime`    DATETIME,      -- 停牌时间
  `suspendflg`     INT(6),        -- 1-一小时    2-一天    3-半天    5-开盘后临时   7-待人工跟踪    9-其他
  `desc`           VARCHAR(200),  -- 描述
  `updatetime`     DATETIME,      -- 表最近更新时间
  PRIMARY KEY (`ukid`)
);



DROP TABLE IF EXISTS `tradmarket_information`;

CREATE TABLE `tradmarket_information`( -- 交易市场信息表
  `markid`   INT(12),      -- 市场ID
  `enname`   VARCHAR(128), -- 英文名称
  `chname`   VARCHAR(128), -- 中文名称
  `country`  VARCHAR(32),  -- 国家
  `markstat` CHAR(1),      -- 交易所状态
  PRIMARY KEY (`markid`)
);

--  交易所品种 --
DROP TABLE IF EXISTS `exchange_information`;

CREATE TABLE `exchange_information`( -- 交易所品种信息表
  `exchangeid`   INT(12),      -- 交易所ID
  `exchangetype` INT,          -- 交易所品种 1.股票,2.期货,3.国债,4.基金,
                               --            5.期权,6.spread,7.个股期权,8.汇率报价,9.汇率期货   
  `enname`       VARCHAR(128), -- 品种英文名称
  `chname`       VARCHAR(128), -- 品种中文名称
  `markstat` CHAR(1),          -- 交易所状态
  PRIMARY KEY (`exchangeid`,`exchangetype`)
);


DROP TABLE IF EXISTS `shares_quotations`;

CREATE TABLE `shares_quotations`(  -- 股票交易行情表 ()
  `trday`          CHAR(8),       -- 交易日
  `ukid`           INT(64),       -- uk编码 -
  `codeid`         INT(20),       -- 证券编码
  `markid`         INT(12),       -- 证券市场ID编码 4096种了
  `exchangeid`     INT(10),       -- 交易所编码
  `highlimit`      DECIMAL(17,2), -- 涨停价
  `lowlimit`       DECIMAL(17,2), -- 跌停价
  `preclear`       DECIMAL(17,2), -- 昨日结算价
  `preclose`       DECIMAL(17,2), -- 昨日收盘价
  `open`           DECIMAL(17,2), -- 开盘价
  `high`           DECIMAL(17,2), -- 高点
  `low`            DECIMAL(17,2), -- 低点
  `last`           DECIMAL(17,2), -- 最新价
  `close`          DECIMAL(17,2), -- 收盘价
  `volume`         DECIMAL(20,0), -- 成交数量 
  `amt`            DECIMAL(20,0), -- 成交金额
  `clear`          DECIMAL(17,2), -- 结算价
  `stat`           CHAR(1),       -- 股票可交易状态
  `updatetime`     DATETIME,      -- 表更新时间
  PRIMARY KEY (`trday`,`ukid`)
);

DROP TABLE IF EXISTS `futures_quotations`;

CREATE TABLE `futures_quotations`( -- 期货交易行情表 
  `trday`          CHAR(8),       -- 交易日
  `ukid`           INT(64),       -- uk编码 -
  `codeid`         INT(20),       -- 证券编码
  `markid`         INT(12),       -- 证券市场ID编码 4096种了
  `exchangeid`     INT(10),       -- 交易所编码
  `contoptionid`   INT(12),       -- 交易标的 大豆/铜 编码 .. 期货使用
  `highlimit`      DECIMAL(17,2), -- 涨停价
  `lowlimit`       DECIMAL(17,2), -- 跌停价
  `preclear`       DECIMAL(17,2), -- 昨日结算价
  `preclose`       DECIMAL(17,2), -- 昨日收盘价
  `open`           DECIMAL(17,2), -- 开盘价
  `high`           DECIMAL(17,2), -- 高点
  `low`            DECIMAL(17,2), -- 低点
  `last`           DECIMAL(17,2), -- 最新价
  `close`          DECIMAL(17,2), -- 收盘价
  `volume`         DECIMAL(20,0), -- 成交数量 
  `amt`            DECIMAL(20,0), -- 成交金额
  `clear`          DECIMAL(17,2), -- 结算价
  `deliverydate`   CHAR(8),       -- 交割日期 ,期货使用
  `position`       DECIMAL(20,0), -- 期货持仓,期货才有用
  `positionchange` DECIMAL(20,0), -- 期货持仓变化量,期货才有用
  `stat`           CHAR(1),       -- 股票可交易状态
  `updatetime`     DATETIME,      -- 表更新时间
  PRIMARY KEY (`trday`,`ukid`)
);
