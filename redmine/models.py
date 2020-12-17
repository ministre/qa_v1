from redminelib import Redmine
from qa_v1 import settings
from redminelib.exceptions import ResourceNotFoundError, ForbiddenError, AuthError, ValidationError


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
