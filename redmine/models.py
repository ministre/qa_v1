from redminelib import Redmine
from qa_v1 import settings
from redminelib.exceptions import ResourceNotFoundError, ForbiddenError, AuthError, ValidationError
from device.models import DeviceType


class RedmineProject:
    def __init__(self):
        self.redmine = Redmine(settings.REDMINE_URL, key=settings.REDMINE_KEY, version=settings.REDMINE_VERSION)

    def check_project(self, redmine_project: str):
        try:
            project = self.redmine.project.get(redmine_project)
            return [True, project.id]
        except ConnectionError:
            return [False, 'Connection error']
        except AuthError:
            return [False, 'Authentication error']
        except ResourceNotFoundError:
            return [False, 'Project not found']
        except ForbiddenError:
            return [False, 'Requested project resource is forbidden']


class RedmineDeviceType:
    @staticmethod
    def export(device_type: DeviceType, project: str, project_name: str, project_desc: str, project_parent: str,
               general_info: bool):
        return [True, {'device_type': device_type.name, 'project': project, 'project_name': project_name,
                       'project_desc': project_desc, 'project_parent': project_parent, 'general_info': general_info}]
