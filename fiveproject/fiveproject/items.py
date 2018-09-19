# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy



#登录
class FiveCityLogin(scrapy.Item):
    # define the fields for your item here like:
    username = scrapy.Field()   #用户名
    password = scrapy.Field()   #密码
    jobWebSite = scrapy.Field()  #招聘网站
    name = scrapy.Field()       #真实姓名
    identityNo = scrapy.Field() #身份证号码
    cookie = scrapy.Field()   #cookie


#基本信息
class FiveCityBascInfo(scrapy.Item):
    name = scrapy.Field()     #真实姓名
    gender = scrapy.Field()     #性别
    birthday = scrapy.Field()     #生日
    height = scrapy.Field()     #身高
    mail = scrapy.Field()     #邮箱
    mobile = scrapy.Field()     #手机号
    address = scrapy.Field()     #居住地
    maritalStatus = scrapy.Field()     #婚姻状况
    workLife = scrapy.Field()     #工作年限
    workStatus = scrapy.Field()     #工作状态





#求职意向
class FiveCityJobIntension(scrapy.Item):
    expectedSalary = scrapy.Field()   #期望薪资
    workPlace = scrapy.Field()       #工作地点
    jobCategory = scrapy.Field()     #职能
    position = scrapy.Field()       #职位
    industry = scrapy.Field()       #行业
    personalLabel = scrapy.Field()       #个人标签
    selfEvaluation = scrapy.Field()       #自我评价
    onBoardDate = scrapy.Field()          #可到岗时间
    workNature = scrapy.Field()          #工作性质


#工作经历
class FiveCityWork(scrapy.Item):
    workStart = scrapy.Field()      #开始时间
    workEnd = scrapy.Field()        #结束时间
    company = scrapy.Field()        #公司
    position = scrapy.Field()        #职位
    industry = scrapy.Field()        #行业
    overview = scrapy.Field()        #公司概况
    workPlace = scrapy.Field()        #工作地点
    workDesc = scrapy.Field()        #工作描述
    workNature = scrapy.Field()        #工作性质


#项目经验
class FiveCityProject(scrapy.Item):
    company = scrapy.Field()        #公司
    projectStart = scrapy.Field()        #开始时间
    projectEnd = scrapy.Field()        #结束时间
    projectName = scrapy.Field()        #项目名称
    projectDesc = scrapy.Field()        #项目描述
    responsibility = scrapy.Field()        #职责描述

#教育经历
class FiveCityEducation(scrapy.Item):
    educationStart = scrapy.Field()     #开始时间
    educationEnd = scrapy.Field()     #结束时间
    school = scrapy.Field()     #学校
    arrangement = scrapy.Field()     #学历
    major = scrapy.Field()     #专业
    learningForm = scrapy.Field()     #学习形式
    majorDesc = scrapy.Field()     #专业描述
    overseaEducation = scrapy.Field()  #是否海外经历


#语言
class FiveCityLanguage(scrapy.Item):
    languageName = scrapy.Field()     #语言
    qualification = scrapy.Field()     #熟练程度

#证书
class FiveCityCertificate(scrapy.Item):
    certificateDate = scrapy.Field()       #证书获得时间
    certificateName = scrapy.Field()       #证书名称
    result = scrapy.Field()       #成绩

#培训经历
class FiveCityTrain(scrapy.Item):
    trainStart = scrapy.Field()     #培训开始时间
    trainEnd = scrapy.Field()     #培训结束时间
    trainOrg = scrapy.Field()     #培训机构
    trainCourse = scrapy.Field()     #培训课程
    trainPlace = scrapy.Field()     #培训地点
    trainDesc = scrapy.Field()     #培训描述




#ORM 映射
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

# 登录信息表
# 用户信息表
class JLLogin(Base):
    __tablename__ = 'jianliv1_jianlilogin'

    id = Column(Integer, primary_key=True)
    token = Column(String(64))
    username = Column(String(50))
    password = Column(String(20))
    jobWebSite = Column(String(20))
    name = Column(String(50))
    identityNo = Column(String(18))
    uid = Column(String(50))
    accessType = Column(String(50))
    loginType = Column(String(10))
    cookie = Column(String(255))
    crawl_status = Column(String(4), default=0)
    create_data = Column(String(4))
    targer_crawl = Column(String(4), default=1)
    msg_code = Column(String(20))
    msg_send_time = Column(Integer)  # 验证码发送时间
    msg_save_time = Column(Integer)  # 验证码输入时间
    add_time = Column(DateTime, default=datetime.datetime.now())


# 基本信息
class JLBasicInfo(Base):
    __tablename__ = 'jianliv1_jianlibasicinfo'
    id = Column(Integer, primary_key=True)
    token = Column(String(64))
    name = Column(String(50))
    gender = Column(String(10))
    birthday = Column(String(20))
    height = Column(String(3))
    mail = Column(String(50))
    mobile = Column(String(50))
    address = Column(String(255))
    maritalStatus = Column(String(10))
    workLife = Column(String(255))
    workStatus = Column(String(100))
    add_time = Column(DateTime, default=datetime.datetime.now())


# 求职意向
class JLJobIntension(Base):
    __tablename__ = 'jianliv1_jianlijobintension'
    id = Column(Integer, primary_key=True)
    token = Column(String(64))
    expectedSalary = Column(String(255))
    workPlace = Column(String(255))
    jobCategory = Column(String(255))
    position = Column(String(255))
    industry = Column(String(255))
    personalLabel = Column(String(255))
    selfEvaluation = Column(String(255))
    onBoardDate = Column(String(255))
    workNature = Column(String(255))
    add_time = Column(DateTime, default=datetime.datetime.now())


# 工作经历
class JLWork(Base):
    __tablename__ = "jianliv1_jianliwork"

    id = Column(Integer, primary_key=True)
    token = Column(String(64))
    workStart = Column(String(20))
    workEnd = Column(String(20))
    company = Column(String(255))
    position = Column(String(255))
    industry = Column(String(255))
    overview = Column(Text)
    workPlace = Column(String(255))
    workDesc = Column(String(255))
    workNature = Column(String(255))
    add_time = Column(DateTime, default=datetime.datetime.now())


# 项目经验
class JLProject(Base):
    __tablename__ = "jianliv1_jianliproject"

    id = Column(Integer, primary_key=True)
    token = Column(String(64))
    company = Column(String(255))
    projectStart = Column(String(50))
    projectEnd = Column(String(50))
    projectName = Column(String(255))
    projectDesc = Column(Text)
    responsibility = Column(String(255))
    add_time = Column(DateTime, default=datetime.datetime.now())


# 教育经历
class JLEducation(Base):
    __tablename__ = "jianliv1_jianlieducation"

    id = Column(Integer, primary_key=True)
    token = Column(String(64))
    educationStart = Column(String(20))
    educationEnd = Column(String(20))
    school = Column(String(255))
    arrangement = Column(String(255))
    major = Column(String(255))
    learningForm = Column(String(255))
    majorDesc = Column(String(255))
    overseaEducation = Column(String(255))
    add_time = Column(DateTime, default=datetime.datetime.now())


# 技能特长  三表
class JLLanguages(Base):
    __tablename__ = "jianliv1_jianlilanguages"

    id = Column(Integer, primary_key=True)
    languageName = Column(String(255))
    qualification = Column(String(255))
    add_time = Column(DateTime, default=datetime.datetime.now())
    tokenid_id = Column(Integer,ForeignKey('jianliv1_jianliskill.token'))
    skill = relationship('JLSkill',back_populates="languages")

class JLCertificates(Base):
    __tablename__ = "jianliv1_jianlicertificates"

    id = Column(Integer, primary_key=True)
    certificateDate = Column(String(20))
    certificateName = Column(String(255))
    result = Column(String(20))
    add_time = Column(DateTime, default=datetime.datetime.now())
    tokenid_id = Column(Integer, ForeignKey('jianliv1_jianliskill.token'))
    skill = relationship('JLSkill',back_populates="certificates")

class JLTrain(Base):
    __tablename__ = "jianliv1_jianlitrain"

    id = Column(Integer, primary_key=True)
    trainStart = Column(String(20))
    trainEnd = Column(String(20))
    trainOrg = Column(String(255))
    trainCourse = Column(String(255))
    trainPlace = Column(String(255))
    trainDesc = Column(String(255))
    add_time = Column(DateTime, default=datetime.datetime.now())
    tokenid_id = Column(Integer, ForeignKey('jianliv1_jianliskill.token'))
    skill = relationship('JLSkill',back_populates="trains")


#技能特长
class JLSkill(Base):
    __tablename__ = "jianliv1_jianliskill"

    token = Column(String(64), primary_key=True)
    add_time = Column(DateTime, default=datetime.datetime.now())
    languages = relationship("JLLanguages",order_by=JLLanguages.id,back_populates="skill")
    certificates = relationship("JLCertificates",order_by=JLCertificates.id,back_populates="skill")
    trains = relationship("JLTrain",order_by=JLTrain.id,back_populates="skill")
