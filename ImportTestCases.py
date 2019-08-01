# -*- coding: utf-8 -*-

from service.JiraService import JiraService
from service.WorkBookService import WorkBookService
from Utils import log_conf
import logging
import time
import datetime
import os

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

module_logger = log_conf()


class ImportTestCases:
    def __init__(self, user, password, test_case_file):
        self.js = JiraService(user=user, password=password)
        self.wbs = WorkBookService(filename=test_case_file)
        self.logger = logging.getLogger("ImportTestCases")

    def import_test_cases(self, project_id):
        cases = self.wbs.get_test_cases()
        if len(cases) == 0:
            self.logger.warning("case file is empty!")
            return
        else:
            for i in range(len(cases)):
                self.logger.info("case: {0}".format(cases[i]))
                case = self.js.generate_issue_payload(cases[i]["title"], project_id=project_id)
                issue_id = self.js.create_issue(case)
                for j in range(len(cases[i]["steps"])):
                    step = cases[i]["steps"][j]
                    self.js.add_test_step(issue_id, step)


def main():
    module_logger.info("===============starting at {0}".format(datetime.datetime.now()))
    user = "admin"
    password = "admin"
    test_case_file = r"./TestCase/Sample Excel Test Sheet.xlsx"

    module_logger.info("user: {0}, password: {1}".format(user, password))

    job = ImportTestCases(user=user, password=password, test_case_file=test_case_file)

    projects = job.js.get_projects()
    time.sleep(0.5)

    project = input("Please input project name: ")
    while True:
        if project in [item["name"] for item in projects]:
            break
        else:
            print("Project: <" + project + "> is incorrect")
            project = input("Please input project name again: ")

    for item in projects:
        if item["name"] == project:
            project_id = item["id"]
    module_logger.info("{0} id is {1}".format(project, project_id))
    job.import_test_cases(project_id)
    module_logger.info("===============end")


if __name__ == '__main__':
    main()
