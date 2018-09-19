import scrapy
import time
from PIL import Image
import base64
from fiveproject.items import FiveCityLogin,FiveCityBascInfo,FiveCityJobIntension,FiveCityWork,FiveCityProject,FiveCityEducation,\
                                        FiveCityLanguage,FiveCityCertificate,FiveCityTrain




class ZhilianSpider(scrapy.Spider):
    name = "58tongcheng"
    allowed_domains = ["zhaopin.com"]

    header = {
        ''
    }

    img_header = {
        ':authority':'passport.58.com',
        ':method':'GET',
        # ':path':'/keepalive/qrcode/img?subject=lN53v4znDxpqxQtn-7ryVaRlu01kdd_1yxnF69yS1aSpR7QwG2lgdg&scene=3',
        ':scheme':'https',
        'accept':'image/webp,image/apng,image/*,*/*;q=0.8',
        'referer': 'https://passport.58.com/login/?path=http%3A//cn.58.com/&PGTID=0d100000-008d-2592-081a-40d9c729a3e9&ClickID=2',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }


    login_header = {
        ':authority':'my.58.com',
         ':method':'GET',
        ':path': '/index?r=0.6092444986312266',
        ':scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.8',
        'upgrade-insecure-requests': '1',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    def start_requests(self):
        url = 'https://passport.58.com/login/?path=http%3A//cn.58.com/&PGTID=0d100000-008d-2592-081a-40d9c729a3e9&ClickID=2'
        yield scrapy.Request(url=url,meta={'cookiejar':1},encoding='utf-8',callback=self.get_clientid,dont_filter=True)


    def get_clientid(self,response):
        tim = str(eval(str(time.time())) * 1000)[:13]
        url = 'https://passport.58.com/keepalive/clientid?callback=jQuery18305120724757644037_1532088021742&_={}'
        # url = 'https://passport.58.com/keepalive/qrcode/imgurl?callback=jQuery18305520856181923703_1532078467750&clientId=9YzG7C3BEPQbFY7FH451xdL90-1GWyiH&listenerId=3&scene=3&source=pc-login&_=%s'%tim
        yield scrapy.Request(url=url.format(tim),meta={'cookiejar': response.meta['cookiejar']},encoding='utf-8',headers=self.img_header,callback=self.get_subject,dont_filter=True)


    def get_subject(self,response):
        print(response.text)
        clientId = ''.join(response.text).split('clientId":"')[1].split('"')[0]
        # print(clientId)
        # print(type(response.text))
        url = 'https://passport.58.com/keepalive/qrcode/imgurl?callback=jQuery18305120724757644037_1532088021743&clientId={}&listenerId=3&scene=3&source=pc-login&_={}'
        tim = str(eval(str(time.time())) * 1000)[:13]
        yield scrapy.Request(url=url.format(clientId,tim),meta={'cookiejar': response.meta['cookiejar'],'clientId':clientId},encoding='utf-8',headers=self.img_header,callback=self.get_check_img,dont_filter=True)



    def get_check_img(self,response):
        print(response.text)
        subject = ''.join(response.text).split('subject=')[1].split('&')[0]
        clientId = response.meta['clientId']
        url = 'https://passport.58.com/keepalive/qrcode/img?subject={}&scene=3'
        yield scrapy.Request(url=url.format(subject), meta={'cookiejar': response.meta['cookiejar'],'clientId':clientId},encoding='utf-8',headers=self.img_header,callback=self.save_img,dont_filter=True)
        # url = 'https://passport.58.com/keepalive/qrcode/img?subject={}&scene=3'
        # yield scrapy.Request(url=url.format(img_url),meta={'cookiejar': response.meta['cookiejar']},headers=self.img_header,dont_filter=True)



    def save_img(self,response):
        with open('img.png', 'wb') as f:
            f.write(response.body)
        print('图片保存成功')
        with open('img.png', 'rb') as f:
            image_base64 = str(base64.b64encode(f.read()))[2:-1]  #这是图片编码后的字符串
        # print(image_base64)  #这是图片编码后的字符串
        img = Image.open('img.png')
        img.show()
        clientId = response.meta['clientId']
        tim = str(eval(str(time.time())) * 1000)[:13]
        url = 'https://passport.58.com/keepalive/connect?callback=jQuery18302607924775963246_1532140325499&clientId={}&_={}'
        time.sleep(20)
        yield scrapy.Request(url=url.format(clientId,tim), meta={'cookiejar': response.meta['cookiejar']}, encoding='utf-8',
                             headers=self.img_header, callback=self.get_token, dont_filter=True)


    #token认证，认证完之后自动转到个人主页（用户中心）
    def get_token(self,response):
        print(response.text)
        # if 'TIMEOUT' in response.text:
        #     print('扫码超时')
        # else:
        token = ''.join(response.text).split('tokenCode')[1].split(',')[0].replace('":"','').replace('"','')
        url = 'http://passport.58.com/thd/scanlogin/pc/passport?source=passport&token={}'
        yield scrapy.Request(url=url.format(token), meta={'cookiejar': response.meta['cookiejar']},
                             encoding='utf-8',
                             headers=self.img_header, callback=self.get_1, dont_filter=True)

    # 获取简历页面
    def get_1(self,response):
        # print(response.text)
        url = 'https://my.58.com/pro/myseekjob/11/'
        yield scrapy.Request(url=url,  meta={'cookiejar': response.meta['cookiejar']},encoding='utf-8',headers=self.login_header,callback=self.jianli_index,dont_filter=True)

    #简历主页
    def jianli_index(self,response):
        # print(response.text)
        url = 'http://jianli.58.com/resuelist/?u=1&r=0.1173711058818066687963574'
        yield scrapy.Request(url=url, meta={'cookiejar': response.meta['cookiejar']},encoding='utf-8',headers=self.login_header,callback=self.get_jianli_link,dont_filter=True )


    #获取到各个简历的链接，并且请求链接
    def get_jianli_link(self,response):
        # print('获取到各个简历的链接，并且请求链接',response.text)
        obj = response.xpath('/html/body/table')
        print(obj)
        jianli_url = ''
        for jianli_item in obj:
            print('4554646')
            jianli_url = jianli_item.xpath('tr[@class="bg1"]/td[@class="czav"]/div[@class="posrlt"]/a[@onclick=\"clickLog(\'from=mypreview\');\"]/@href').extract()
        print(jianli_url)
        if jianli_url:
            for url in jianli_url:
                yield scrapy.Request(url=url, meta={'cookiejar': response.meta['cookiejar']},encoding='utf-8',headers=self.login_header,callback=self.get_jianli_info,dont_filter=True)
        else:
            print('没有简历')


    # 正式获取简历详细信息
    def get_jianli_info(self,response):
        print(response.text)
        name = response.xpath('/html/body/div[3]/div/div/h1/span[@class="name"]/text()').extract()
        if name:
            name = ''.join(name).strip()  # 用户名
        else:
            name = ''
        sexAge = response.xpath('/html/body/div[3]/div/div/h1/span[@class="sexAge"]/text()').extract()
        if sexAge:
            gender = ''.join(sexAge).strip().replace('(', '').replace(')', '')  # 性别，年龄
        else:
            gender=''


        #基本情况div
        arrangement, workLife, now_address, jobItem = self.get_expectInfo(response)


        #工作经验div
        workItem = self.get_workInfo(response)


        # 教育经历
        eduItem = self.get_eduInfo(response)
        eduItem['arrangement'] = arrangement     #注意：：在训数据库的时候，所有的eduItem公用同一个学历，以最高学历为主


        #语言能力
        languageItem = self.get_languageInfo(response)

        #证书
        certifiItem = self.get_certificateInfo(response)

        #项目经验


        # print('个人信息',name,gender,workLife,now_address)
        print('求职意向',jobItem)
        print('工作经验',workItem)
        print('工作经验',workItem['workDesc'])


    # 基本情况div
    def get_expectInfo(self,response):
        jobItem = FiveCityJobIntension()
        expectInfo = response.xpath('/html/body/div[3]/div/div/div[@class="expectInfo"]')
        if expectInfo:
            for base_info in expectInfo:
                arrangement = base_info.xpath('div[@class="expectTitle"]/dl[1]/dd/ul/li[1]/text()').extract()
                arrangement = ''.join(arrangement).strip()  # 学历
                workLife = base_info.xpath('div[@class="expectTitle"]/dl[1]/dd/ul/li[3]/text()').extract()
                workLife = ''.join(workLife).strip()  # 工作年限
                now_address = base_info.xpath('div[@class="expectTitle"]/dl[1]/dd/ul/li[5]/text()').extract()
                now_address = ''.join(now_address).strip()  # 现居地址

                # 求职意向
                position = base_info.xpath('div[@class="expectTitle"]/dl[2]/dd/ul/li[1]/text()').extract()
                position = ''.join(position).strip()  # 职位
                workPlace = base_info.xpath('div[@class="expectTitle"]/dl[2]/dd/ul/li[3]/text()').extract()
                workPlace = ''.join(workPlace).strip()  # 工作地点
                expectedSalary = base_info.xpath('div[@class="expectTitle"]/dl[2]/dd/ul/li[5]/text()').extract()
                expectedSalary = ''.join(expectedSalary).strip()  # 期望薪资
                selfEvaluation = base_info.xpath('div[@class="intrCon"]/text()').extract()
                selfEvaluation = ''.join(selfEvaluation).strip()  # 自我描述
                personalLabel = base_info.xpath('ul[@class="cbright"]/li/div/span/text()').extract()
                personalLabel = ','.join(personalLabel).strip()  # 标签

                jobItem['expectedSalary'] = expectedSalary
                jobItem['workPlace'] = workPlace
                jobItem['jobCategory'] = ''
                jobItem['position'] = position
                jobItem['industry'] = ''
                jobItem['personalLabel'] = personalLabel
                jobItem['selfEvaluation'] = selfEvaluation
                jobItem['onBoardDate'] = ''
                jobItem['workNature'] = ''
        else:
            arrangement = ''
            workLife = ''
            now_address = ''
            jobItem['expectedSalary'] = ''
            jobItem['workPlace'] = ''
            jobItem['jobCategory'] = ''
            jobItem['position'] = ''
            jobItem['industry'] = ''
            jobItem['personalLabel'] = ''
            jobItem['selfEvaluation'] = ''
            jobItem['onBoardDate'] = ''
            jobItem['workNature'] = ''
        return arrangement,workLife,now_address,jobItem

    # 工作经验div
    def get_workInfo(self,response):
        workItem = FiveCityWork()
        workInfo = response.xpath('/html/body/div[3]/div/div/div[@class="addcont addexpe"]/div[contains(@class,"infoview")]')
        if workInfo:
            companys = []  # 公司
            workTimes = []  # 工作时间
            positions = []  # 职位
            workDescs = []  # 工作描述
            for work_info in workInfo:
                company = work_info.xpath('h4/text()').extract()
                company = ''.join(company).strip()  # 公司
                worktime = work_info.xpath('p[1]/span[2]/text()').extract()
                worktime = ''.join(worktime).strip()
                worktime = worktime.split('-')  # 工作时间，格式['2018.5,2018.6']
                position = work_info.xpath('p[3]/span[2]/text()').extract()
                position = ''.join(position).strip()  # 职位
                workDesc = work_info.xpath('p[4]/span[2]/text()').extract()
                workDesc = ''.join(workDesc).strip()  # 工作描述

                companys.append(company)
                workTimes.append(worktime)
                positions.append(position)
                workDescs.append(workDesc)

                workItem['workStart'] = workTimes
                workItem['company'] = companys
                workItem['position'] = positions
                workItem['industry'] = ''
                workItem['overview'] = ''
                workItem['workPlace'] = ''
                workItem['workDesc'] = workDescs
                workItem['workNature'] = ''

        else:
            workItem['workStart'] = ''
            workItem['company'] = ''
            workItem['position'] = ''
            workItem['industry'] = ''
            workItem['overview'] = ''
            workItem['workPlace'] = ''
            workItem['workDesc'] = ''
            workItem['workNature'] = ''

        return workItem

    # 教育经历
    def get_eduInfo(self,response):
        eduItem = FiveCityEducation()
        eduInfo = response.xpath('/html/body/div[3]/div/div/div[@class="addcont addeduc"]/div[contains(@class,"infoview")]')
        if eduInfo:
            educationEnds = []
            schools = []
            majors = []
            for edu_item in eduInfo:
                edu_endTime = edu_item.xpath('ul/li[1]/text()').extract()
                edu_endTime = ''.join(edu_endTime).strip()    #毕业时间
                school = edu_item.xpath('ul/li[2]/text()').extract()
                school = ''.join(school)     #学校
                major = edu_item.xpath('ul/li[3]/text()').extract()
                major = ''.join(major).strip()   #专业

                educationEnds.append(edu_endTime)
                schools.append(school)
                majors.append(major)

                eduItem['educationStart'] = ''
                eduItem['educationEnd'] = educationEnds
                eduItem['school'] = schools
                eduItem['major'] = majors
                eduItem['learningForm'] = ''
                eduItem['majorDesc'] = ''
                eduItem['overseaEducation'] = ''
        else:
            eduItem['educationStart'] = ''
            eduItem['educationEnd'] = ''
            eduItem['school'] = ''
            eduItem['major'] = ''
            eduItem['learningForm'] = ''
            eduItem['majorDesc'] = ''
            eduItem['overseaEducation'] = ''

        return eduItem

    #语言能力
    def get_languageInfo(self,response):
        languageItem = FiveCityLanguage()
        languageInfo = response.xpath('/html/body/div[3]/div/div/div[@class="addcont addlan"]/div[@class="infoview"]')
        if languageInfo:
            languageNames = []
            qualifications = []
            for language_item in languageInfo:
                languagename = language_item.xpath('p/span[1]/text()').extract()
                languagename = ''.join(languagename).strip()   #语言名称
                qualification = language_item.xpath('p/span[@class="std"]/span/text()').extract()
                qualification = ','.join(qualification).strip()    #熟练程度

                languageNames.append(languagename)
                qualifications.append(qualification)

                languageItem['languageName'] = languageNames
                languageItem['qualification'] = qualifications
        else:
            languageItem['languageName'] = ''
            languageItem['qualification'] = ''

        return languageItem

    # 证书
    def get_certificateInfo(self,response):
        certifiItem = FiveCityCertificate()
        certifi_info = response.xpath('/html/body/div[3]/div/div/div[@class="addcont addcert"]/div[@class="infoview"]')
        if certifi_info:
            certificateDates = []
            certificateNames = []
            results = []
            for certifi_item in certifi_info:
                certificateName = certifi_item.xpath('p/span[1]/text()').extract()
                certificateName = ''.join(certificateName).strip()    #证书名称
                certificateDate = certifi_item.xpath('p/span[2]/text()').extract()
                certificateDate = ''.join(certificateDate).strip()    #证书时间
                result = ''

                certificateDates.append(certificateDate)
                certificateNames.append(certificateName)
                results.append(result)

                certifiItem['certificateDate'] = certificateDates
                certifiItem['certificateName'] = certificateNames
                certifiItem['result'] = results
        else:
            certifiItem['certificateDate'] = ''
            certifiItem['certificateName'] = ''
            certifiItem['result'] = ''

        return certifiItem

    #项目经验
    def get_projectInfo(self,response):
        projectItem = FiveCityProject()
        project_Info = response.xpath('/html/body/div[3]/div/div/div[@class="addcont addproj"]/div[@class="infoview"]')
        if project_Info:
            companys = []
            projextTimes = []
            projectNames = []
            projectDescs = []
            responsibilitys = []
            for project_item in project_Info:
                projectName = project_item.xpath('h4/text()').extract()
                projectName = ''.join(projectName).strip()    #项目名称
                projectDesc = project_item.xpath('p[2]/span[2]/text()').extract()
                projectDesc = ''.join(projectDesc).strip()   #项目描述
                responsibility = project_item.xpath('p[3]/span[2]/text()').extract()
                responsibility = ''.join(responsibility).strip()  #职责和业绩
                projectTime = project_item.xpath('p[1]/span[2]/text()').extract()
                projectTime = ''.join(projectTime).strip().split('-')  #开始,结束，时间
                company = ''

                companys.append(company)
                projextTimes.append(projectTime)
                projectNames.append(projectName)
                projectDescs.append(projectDesc)
                responsibilitys.append(responsibility)



        else:
            pass
















