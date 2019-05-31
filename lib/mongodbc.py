# coding=utf-8
import time
from pymongo import MongoClient


class MongoDBC(object):
    def __init__(self):
        user_url153 = 'mongodb://xiao:xx123456@192.168.0.153/test'
        # user_url = 'mongodb://xiao:xiao@192.168.0.153/test'
        self.client153 = MongoClient(user_url153)
        self.db153 = self.client153['test']

        user_url161 = 'mongodb://xiao:xx123456@192.168.0.161/edition'
        # user_url = 'mongodb://xiao:xiao@192.168.0.153/test'
        self.client161 = MongoClient(user_url161)
        self.db161 = self.client161['edition']

    @classmethod
    def get_instance(cls):
        if hasattr(cls, 'instance'):
            return cls.instance
        else:
            cls.instance = cls()
            return cls.instance

    def find(self, table_name, condition_dict, projection_dict=None):
        if table_name == 'companies':
            table = self.db161[table_name]
        else:
            table = self.db153[table_name]
        # companies_table.find_one_and_update()
        return table.find(condition_dict, projection_dict)

    def find_one(self, table_name, condition_dict, projection_dict=None):
        if table_name == 'companies':
            table = self.db161[table_name]
        else:
            table = self.db153[table_name]
        # companies_table.find_one_and_update()
        return table.find_one(condition_dict, projection_dict)

    def remove(self):
        pass

    # 单条插入
    def insert_one(self, table_name, data_dict_param):
        data_dict = data_dict_param.copy()
        if table_name == 'companies':
            table = self.db161[table_name]
        else:
            table = self.db153[table_name]
        if table_name == 'companies':
            if data_dict.get('company_name') is None:
                return -1
            insert_dict = {
                'company_name': data_dict.get('company_name', ''),
                'region': data_dict.get('patent_list', ''),
                'patents_ref': data_dict.get('patent_list', []),
                'legal_person': data_dict.get('legal_person', ''),
                'mail': data_dict.get('mail', ''),
                'telephone': data_dict.get('telephone', ''),
                # 企业地址：    北京市丰台区西四环南路101号2018A室
                'address': data_dict.get('address', ''),
                # 注册资本：    131500万元人民币
                'registered_capital': data_dict.get('registered_capital', ''),
                # 实缴资本：
                'paidin_capital': data_dict.get('paidin_capital', ''),
                # 经营状态：    开业
                'business_status': data_dict.get('business_status', ''),
                # 成立日期：    2016 - 03 - 22
                'founded_date': data_dict.get('founded_date', ''),
                # 统一社会信用代码：    91110106MA00496U71
                'social_credit_code': data_dict.get('social_credit_code', ''),
                # 纳税人识别号：    91110106MA00496U71
                'taxpayer_identification_number': data_dict.get('taxpayer_identification_number', ''),
                # 注册号：    110106020872284
                'registration_number': data_dict.get('registration_number', ''),
                # 组织机构代码：    MA00496U - 7
                'organization_code': data_dict.get('organization_code', ''),
                # 公司类型：    有限责任公司(法人独资)
                'company_type': data_dict.get('company_type', ''),
                # 所属行业：    科学研究和技术服务业
                'industry': data_dict.get('industry', ''),
                # 核准日期：    2018 - 09 - 20
                'approval_date': data_dict.get('approval_date', ''),
                # 登记机关：    丰台分局
                'registration_authority': data_dict.get('registration_authority', ''),
                # 所属地区：    北京市
                'province': data_dict.get('province', ''),
                # 英文名：    -
                'english_name': data_dict.get('english_name', ''),
                # 曾用名中铁物轨道科技服务有限公司
                'used_name': data_dict.get('used_name', ''),
                # 参保人数 45
                'social_insurance_num': data_dict.get('social_insurance_num', ''),
                # 人员规模500 - 999
                'staff_size': data_dict.get('staff_size', ''),
                # 营业期限2016 - 03 - 22至无固定期限
                'business_term': data_dict.get('business_term', ''),
                # 经营范围：    销售金属材料、金属制品、矿产品、机械设备、电子产品
                'business_scope': data_dict.get('business_scope', '')
            }
            data_dict.update(insert_dict)
        if table_name == 'trademarks':
            if data_dict.get('apply_id') is None:
                return -1
            insert_dict = {
                'apply_id': '',
                'name': '',
                'category': '',
                'status': '',
                'applicant': '',
                'apply_date': '',
                # 初审公告日
                'investigate_date': '',
                # 注册公告日
                'register_date': '',
                # 专用期限
                'deadline': '',
                # 代理机构
                'agency': '',
                # 公告
                'announcement': '',
                # 商品/服务项目
                'service_items': '',
                # 商标动态
                'dynamics': '',
            }
            insert_dict.update(data_dict)
        if table_name == 'copyrights':
            if data_dict.get('register_no') is None:
                return -1
            insert_dict = {
                'register_no': '',
                'name': '',
                'category': '',
                # 创作完成日期
                'finish_time': '',
                # 登记日期
                'register_date': '',
                # 首次发布日期
                'release_time': ''
            }
            insert_dict.update(data_dict)

        data_dict['update_time'] = time.strftime('%Y-%m-%d')
        return table.insert_one(data_dict)

    def insert_many(self, table_name, data_dict_list):
        if table_name == 'companies':
            table = self.db161[table_name]
        else:
            table = self.db153[table_name]
        if table_name == 'companies':
            for data_dict in data_dict_list:
                if data_dict.get('company_name') is None:
                    return -1
                insert_dict = {
                    'company_name': data_dict.get('company_name', ''),
                    'region': data_dict.get('patent_list', ''),
                    'patents_ref': data_dict.get('patent_list', []),
                    'legal_person': data_dict.get('legal_person', ''),
                    'mail': data_dict.get('mail', ''),
                    'telephone': data_dict.get('telephone', ''),
                    # 企业地址：    北京市丰台区西四环南路101号2018A室
                    'address': data_dict.get('address', ''),
                    # 注册资本：    131500万元人民币
                    'registered_capital': data_dict.get('registered_capital', ''),
                    # 实缴资本：
                    'paidin_capital': data_dict.get('paidin_capital', ''),
                    # 经营状态：    开业
                    'business_status': data_dict.get('business_status', ''),
                    # 成立日期：    2016 - 03 - 22
                    'founded_date': data_dict.get('founded_date', ''),
                    # 统一社会信用代码：    91110106MA00496U71
                    'social_credit_code': data_dict.get('social_credit_code', ''),
                    # 纳税人识别号：    91110106MA00496U71
                    'taxpayer_identification_number': data_dict.get('taxpayer_identification_number', ''),
                    # 注册号：    110106020872284
                    'registration_number': data_dict.get('registration_number', ''),
                    # 组织机构代码：    MA00496U - 7
                    'organization_code': data_dict.get('organization_code', ''),
                    # 公司类型：    有限责任公司(法人独资)
                    'company_type': data_dict.get('company_type', ''),
                    # 所属行业：    科学研究和技术服务业
                    'industry': data_dict.get('industry', ''),
                    # 核准日期：    2018 - 09 - 20
                    'approval_date': data_dict.get('approval_date', ''),
                    # 登记机关：    丰台分局
                    'registration_authority': data_dict.get('registration_authority', ''),
                    # 所属地区：    北京市
                    'province': data_dict.get('province', ''),
                    # 英文名：    -
                    'english_name': data_dict.get('english_name', ''),
                    # 曾用名中铁物轨道科技服务有限公司
                    'used_name': data_dict.get('used_name', ''),
                    # 参保人数 45
                    'social_insurance_num': data_dict.get('social_insurance_num', ''),
                    # 人员规模500 - 999
                    'staff_size': data_dict.get('staff_size', ''),
                    # 营业期限2016 - 03 - 22至无固定期限
                    'business_term': data_dict.get('business_term', ''),
                    # 经营范围：    销售金属材料、金属制品、矿产品、机械设备、电子产品
                    'business_scope': data_dict.get('business_scope', '')
                }
                data_dict.update(insert_dict)
                data_dict['update_time'] = time.strftime('%Y-%m-%d')
        if table_name == 'trademarks':
            for data_dict in data_dict_list:
                if data_dict.get('apply_id') is None:
                    return -1
                insert_dict = {
                    'apply_id': '',
                    'name': '',
                    'image_fid': '',
                    'category': '',
                    'status': '',
                    'applicant': '',
                    'apply_date': '',
                    # 初审公告日
                    'investigate_date': '',
                    # 注册公告日
                    'register_date': '',
                    # 专用期限
                    'deadline': '',
                    # 代理机构
                    'agency': '',
                    # 公告
                    'announcement': '',
                    # 商品/服务项目
                    'service_items': '',
                    # 商标动态
                    'dynamics': '',
                }
                insert_dict.update(data_dict)
                data_dict['update_time'] = time.strftime('%Y-%m-%d')
        return table.insert_many(data_dict_list, ordered=False)

    def update_one(self, table_name, update_cond, update_dict, **kwargs):
        if table_name == 'companies':
            table = self.db161[table_name]
        else:
            table = self.db153[table_name]
        set_dict = update_dict.get('$set', {})
        set_dict.update({'update_time': time.strftime('%Y-%m-%d')})
        update_dict['$set'] = set_dict
        return table.update_one(update_cond, update_dict, **kwargs)

    def find_and_update_one(self, table_name, update_cond, update_dict, **kwargs):
        if table_name == 'companies':
            table = self.db161[table_name]
        else:
            table = self.db153[table_name]
        set_dict = update_dict.get('$set', {})
        set_dict.update({'update_time': time.strftime('%Y-%m-%d')})
        update_dict['$set'] = set_dict
        return table.find_one_and_update(update_cond, update_dict, **kwargs)
