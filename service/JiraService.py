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
    def __init__(self, user='admin', password='admin'):
        self.user = user
        self.password = password
        self.url_base = 'http://192.168.1.17:8080/rest'
        self.headers = {"Accept": "application/json", "Content-Type": "application/json"}
        self.auth = HTTPBasicAuth(self.user, self.password)
        self.logger = logging.getLogger("JiraService")

    def get_projects(self):
        url = self.url_base + '/api/latest/project'
        response = requests.get(url, headers = self.headers, auth = self.auth)
        time.sleep(SLEEPTIME)
        data = response.json()
        projects = [{"name": project["name"], "id":project["id"]} for project in data]
        self.logger.info(projects)
        return projects

    def get_project_versions_by_id(self, project_id):
        url = self.url_base + "/api/latest/project/%s/versions" % project_id
        response = requests.get(url, headers=self.headers, auth=self.auth)
        time.sleep(SLEEPTIME)
        self.logger.info("Project: {0} versions: {1}".format(project_id, response.json()))
        return response.json()

    def get_create_issue_metadata(self):
        url = self.url_base + "/api/latest/issue/createmeta"
        response = requests.get(url, headers=self.headers, auth=self.auth)
        time.sleep(SLEEPTIME)
        self.logger.info("Create issue metadata: {0}".format(response.json()))
        return response.json()

    def get_all_issue_type(self):
        url = self.url_base + "/api/latest/issuetype"
        response = requests.get(url, headers=self.headers, auth=self.auth)
        time.sleep(SLEEPTIME)
        self.logger.info("All issue type: {0}".format(response.json()))
        return response.json()

    def get_user_account_id(self):
        url = self.url_base + "/api/latest/user"
        payload = {'username': self.user}
        response = requests.get(url, headers = self.headers, auth = self.auth, params=payload)
        time.sleep(SLEEPTIME)
        self.logger.info(response.json())

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
        url = self.url_base + "/api/latest/issue"
        response = requests.post(url, data=json.dumps(issue), headers=self.headers, auth=self.auth)
        time.sleep(SLEEPTIME)
        self.logger.info("Create issue: {0}".format(response.json()))
        return eval(response.text)["id"]

    def add_test_step(self, issueid, step):
        url = self.url_base + "/zephyr/latest/teststep/%s" % issueid
        headers = self.headers
        headers["User-Agent"] = "ZFJImporter"
        headers["AO-7DEABF"] = str(uuid.uuid4())
        response = requests.post(url, data=json.dumps(step), headers=headers, auth=self.auth)
        time.sleep(SLEEPTIME)
        self.logger.info("Add test step: {0}".format(response.json()))

    def get_issue_by_id(self, issueid):
        url = self.url_base + "/api/latest/issue/%s" % issueid
        response = requests.get(url, headers = self.headers, auth = self.auth)
        time.sleep(SLEEPTIME)
        self.logger.info("issue info: {0}".format(response.json()))
        return response.json()


if __name__ == '__main__':
    js = JiraService()
    js.get_projects()