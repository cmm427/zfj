# -*- coding: utf-8 -*-

import requests
from requests.auth import HTTPBasicAuth
import json
import uuid
import logging
import time

module_logger = logging.getLogger(__name__)
SLEEPTIME = 0.5


class JiraService:
    def __init__(self, user='admin', password='admin', host='http://192.168.1.17:8080'):
        self.__user = user
        self.__password = password
        self.__host = host
        self.headers = {"Accept": "application/json", "Content-Type": "application/json"}
        self.logger = logging.getLogger("JiraService")

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user):
        self.__user = user

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, host):
        self.__host = host

    def get_base_url(self):
        return self.host + '/rest'

    def gen_auth(self):
        # 生成 basic auth
        return HTTPBasicAuth(self.user, self.password)

    def is_login(self):
        # 判断用户是否登录
        url = self.get_base_url() + '/api/latest/project'
        resp = requests.get(url, headers=self.headers, auth=self.gen_auth())
        self.logger.warning("is_login status code: {0}".format(resp.status_code))
        return resp.status_code

    def get_projects(self):
        # 获取所有项目列表
        url = self.get_base_url() + '/api/latest/project'
        response = requests.get(url, headers = self.headers, auth = self.gen_auth())
        time.sleep(SLEEPTIME)
        data = response.json()
        projects = [{"name": project["name"], "id":project["id"]} for project in data]
        # self.logger.info(projects)
        return projects

    def get_project_id(self, project_name):
        # 根据项目名获取项目ID
        for item in self.get_projects():
            if item['name'] == project_name:
                return item['id']

    def get_project_versions_by_id(self, project_id):
        url = self.get_base_url() + "/api/latest/project/%s/versions" % project_id
        response = requests.get(url, headers=self.headers, auth=self.gen_auth())
        time.sleep(SLEEPTIME)
        self.logger.info("Project: {0} versions: {1}".format(project_id, response.json()))
        return response.json()

    def get_create_issue_metadata(self):
        url = self.get_base_url() + "/api/latest/issue/createmeta"
        response = requests.get(url, headers=self.headers, auth=self.gen_auth())
        time.sleep(SLEEPTIME)
        self.logger.info("Create issue metadata: {0}".format(response.json()))
        return response.json()

    def get_all_issue_type(self):
        url = self.get_base_url() + "/api/latest/issuetype"
        response = requests.get(url, headers=self.headers, auth=self.gen_auth())
        time.sleep(SLEEPTIME)
        self.logger.info("All issue type: {0}".format(response.json()))
        return response.json()

    def get_user_account_id(self):
        url = self.get_base_url() + "/api/latest/user"
        payload = {'username': self.user}
        response = requests.get(url, headers = self.headers, auth = self.gen_auth(), params=payload)
        time.sleep(SLEEPTIME)
        self.logger.warning(response.json())

    def generate_issue_payload(self, summary, project_id="10301"):
        fields = dict()
        fields["project"] = {"id": project_id}
        fields["summary"] = summary
        fields["issuetype"] = {"id": "10005"}

        reporter = dict()
        reporter["username"] = self.user

        payload = dict()
        payload["fields"] = fields
        payload["reporter"] = reporter

        return payload

    def create_issue(self, issue):
        # 新增问题，并返回该问题的ID
        url = self.get_base_url() + "/api/latest/issue"
        response = requests.post(url, data=json.dumps(issue), headers=self.headers, auth=self.gen_auth())
        time.sleep(SLEEPTIME)
        self.logger.warning("Create issue: {0}".format(response.json()))
        return eval(response.text)["id"]

    def add_test_step(self, issueid, step):
        # 添加测试步骤
        url = self.get_base_url() + "/zephyr/latest/teststep/%s" % issueid
        headers = self.headers
        headers["User-Agent"] = "ZFJImporter"
        headers["AO-7DEABF"] = str(uuid.uuid4())
        response = requests.post(url, data=json.dumps(step), headers=headers, auth=self.gen_auth())
        time.sleep(SLEEPTIME)
        self.logger.warning("Add test step: {0}".format(response.json()))

    def get_issue_by_id(self, issueid):
        url = self.get_base_url() + "/api/latest/issue/%s" % issueid
        response = requests.get(url, headers = self.headers, auth = self.gen_auth())
        time.sleep(SLEEPTIME)
        self.logger.info("issue info: {0}".format(response.json()))
        return response.json()


if __name__ == '__main__':
    js = JiraService('cuimingming','cuimingming')
    js.get_user_account_id()
