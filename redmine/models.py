from redminelib import Redmine
from qa_v1 import settings
from redminelib.exceptions import ResourceNotFoundError, ForbiddenError, AuthError, ValidationError
from device.models import DeviceType
from django.utils.translation import gettext_lazy as _


class RedmineProject:
    def __init__(self):
        self.redmine = Redmine(settings.REDMINE_URL, key=settings.REDMINE_KEY, version=settings.REDMINE_VERSION)

    def check_project(self, project: str):
        try:
            project = self.redmine.project.get(project)
            return [200, project.id]
        except ConnectionError:
            return [500, _('Connection error')]
        except AuthError:
            return [401, _('Authentication error')]
        except ResourceNotFoundError:
            return [404, _('Project not found')]
        except ForbiddenError:
            return [403, _('Requested project resource is forbidden')]

    def create_or_update_project(self, project: str, project_name: str, project_desc='', project_parent=None):
        is_project = self.check_project(project=project)
        # update project
        if is_project[0] == 200:
            if project_desc == '':
                self.redmine.project.update(resource_id=is_project[1], name=project_name, description='')
            else:
                self.redmine.project.update(resource_id=is_project[1], name=project_name,
                                            description='__%{color:gray}' + project_desc + '%__')
            return [True, _('Project updated')]

        elif is_project[0] == 404:
            # create project
            # non-root
            if project_parent:
                is_parent_project = self.check_project(project=project_parent)
                if is_parent_project[0] != 200:
                    return [False, _('Parent project error') + ': ' + is_parent_project[1]]
                else:
                    try:
                        if project_desc:
                            self.redmine.project.create(identifier=project, name=project_name,
                                                        parent_id=is_parent_project[1], inherit_members=True,
                                                        description='__%{color:gray}' + project_desc + '%__')
                        else:
                            self.redmine.project.create(identifier=project, name=project_name,
                                                        parent_id=is_parent_project[1], inherit_members=True)
                        return [True, _('Project created')]
                    except ValidationError:
                        return [False, _('Project ID or name validation fail')]
            # root
            else:
                try:
                    if project_desc:
                        p = self.redmine.project.create(identifier=project, name=project_name,
                                                        description='__%{color:gray}' + project_desc + '%__')
                    else:
                        p = self.redmine.project.create(identifier=project, name=project_name)
                    return [True, 'Project created']
                except ValidationError:
                    return [False, _('Project ID or name validation fail')]
        return [False, is_project[1]]

    def get_wiki(self, project: str, wiki_title: str):
        try:
            wiki = self.redmine.wiki_page.get(wiki_title, project_id=project)
            return [200, wiki.text]
        except ResourceNotFoundError:
            return[404, _('Wiki not found')]
        except ForbiddenError:
            return [403, _('Requested wiki resource is forbidden')]

    def create_or_update_wiki(self, project: str, wiki_title: str, wiki_text: str, parent_wiki_title=None):
        is_wiki = self.get_wiki(project=project, wiki_title=wiki_title)
        if is_wiki[0] == 200:
            if parent_wiki_title:
                self.redmine.wiki_page.update(wiki_title, project_id=project, text=wiki_text, parent_title='wiki')
            else:
                self.redmine.wiki_page.update(wiki_title, project_id=project, text=wiki_text)
            return [True, _('Wiki updated')]
        elif is_wiki[0] == 400:
            if parent_wiki_title:
                self.redmine.wiki_page.create(project_id=project, title=wiki_title, text=wiki_text, parent_title='wiki')
            else:
                self.redmine.wiki_page.create(project_id=project, title=wiki_title, text=wiki_text)
            return [True, _('Wiki created')]
        else:
            return [False, is_wiki[1]]


class RedmineDeviceType:
    @staticmethod
    def build_wiki(device_type: DeviceType, project_name: str, general_info: bool):
        wiki = 'h1. ' + project_name + '\r' \
                                       '\n\r'
        if general_info:
            wiki += '\nh2. Общая информация\r' \
                    '\n\r' \
                    '\n| ' + _('Name') + ': | ' + device_type.name + ' |\r'
        return wiki

    @staticmethod
    def export(device_type: DeviceType, project: str, project_name: str, project_desc: str, project_parent: str,
               general_info: bool):
        r = RedmineProject()
        redmine_project = r.create_or_update_project(project=project, project_name=project_name,
                                                     project_desc=project_desc, project_parent=project_parent)
        if not redmine_project[0]:
            return redmine_project
        else:
            message = redmine_project[1]
            wiki = RedmineDeviceType.build_wiki(device_type=device_type, project_name=project_name,
                                                general_info=general_info)
            is_wiki = r.create_or_update_wiki(project=project, wiki_title='Wiki', wiki_text=wiki)
            if not is_wiki[0]:
                return is_wiki
            else:
                message += '. ' + str(is_wiki[1]) + '.'
                return [True, message]
