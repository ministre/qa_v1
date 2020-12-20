from redminelib import Redmine
from qa_v1 import settings
from redminelib.exceptions import ResourceNotFoundError, ForbiddenError, AuthError, ValidationError
from device.models import DeviceType, Device
from protocol.models import Protocol, TestResult
from protocol.views import get_numbers_of_results
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
        if parent_wiki_title:
            is_parent_wiki = self.get_wiki(project=project, wiki_title=parent_wiki_title)
            if is_parent_wiki[0] != 200:
                return [False, str(_('Parent Wiki error')) + ': ' + str(is_parent_wiki[1])]
        is_wiki = self.get_wiki(project=project, wiki_title=wiki_title)
        if is_wiki[0] == 200:
            if parent_wiki_title:
                self.redmine.wiki_page.update(wiki_title, project_id=project, text=wiki_text, parent_title='wiki')
            else:
                self.redmine.wiki_page.update(wiki_title, project_id=project, text=wiki_text)
            return [True, _('Wiki updated')]
        elif is_wiki[0] == 404:
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
            wiki += '\nh2. ' + str(_('General')) + '\r' \
                    '\n\r' \
                    '\n| ' + str(_('Name')) + ': | ' + device_type.name + ' |\r'
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


class RedmineDevice:
    @staticmethod
    def build_wiki(device: Device, project_name: str, general_info: bool):
        wiki = 'h1. ' + project_name + '\r\n\r'
        if general_info:
            wiki += '\nh2. ' + str(_('General')) + '\r' \
                    '\n\r' \
                    '\n| ' + str(_('Device Type')) + ': | ' + device.type.name + ' |\r' \
                    '\n| ' + str(_('Vendor')) + ': | ' + device.vendor.name + ' |\r' \
                    '\n| ' + str(_('Model')) + ': | ' + device.model + ' |\r'

            if device.hw:
                wiki += '\n| ' + str(_('Hardware Version')) + ': | ' + device.hw + ' |\r' \

            wiki += '\n\r' \
                    '\nh2. Внешний вид\r\n\r' \
                    '\nh2. Результаты испытаний\r\n\r'
        return wiki

    @staticmethod
    def export(device: Device, project: str, project_name: str, project_desc: str, project_parent: str,
               general_info: bool):
        r = RedmineProject()
        redmine_project = r.create_or_update_project(project=project, project_name=project_name,
                                                     project_desc=project_desc, project_parent=project_parent)
        if not redmine_project[0]:
            return redmine_project
        else:
            message = redmine_project[1]
            wiki = RedmineDevice.build_wiki(device=device, project_name=project_name, general_info=general_info)
            is_wiki = r.create_or_update_wiki(project=project, wiki_title='Wiki', wiki_text=wiki)
            if not is_wiki[0]:
                return is_wiki
            else:
                message += '. ' + str(is_wiki[1]) + '.'
                return [True, message]


class RedmineProtocol:
    @staticmethod
    def build_wiki(protocol: Protocol, project_name: str, general_info: bool):
        wiki = 'h1. ' + project_name + '\r\n\r'
        if general_info:
            wiki += '\nh2. ' + str(_('General')) + '\r\n\r' \
                    '\n| ' + str(_('Device')) + ': | ' + protocol.device.vendor.name + ' ' + str(protocol.device) + ' |\r' \
                    '\n| ' + str(_('Testplan')) + ': | ' + str(_('Testplan')) + ' ' + str(protocol.testplan) + ' |\r' \
                    '\n| ' + str(_('Software Version')) + ': | ' + protocol.sw + ' |\r'
            if protocol.sw_checksum:
                wiki += '\n| ' + str(_('Checksum')) + ': | ' + protocol.sw_checksum + ' |\r'
            wiki += '\n| ' + str(_('Started')) + ': | ' + protocol.date_of_start.strftime('%d.%m.%Y') + '|\r'
            if protocol.date_of_finish:
                wiki += '\n| ' + str(_('Completed')) + ': | ' + protocol.date_of_finish.strftime('%d.%m.%Y') + '|\r'
            if protocol.engineer_login:
                wiki += '\n| ' + str(_('Engineer Login')) + ': | ' + protocol.engineer_login + ' |\r'
            if protocol.engineer_password:
                wiki += '\n| ' + str(_('Engineer Password')) + ': | ' + protocol.engineer_password + ' |\r'
            if protocol.sysinfo:
                wiki += '\n\r\n{{collapse(' + str(_('System Information')) + ')\r\n' + protocol.sysinfo + '\r\n}}\r'
            if protocol.console:
                wiki += '\n\r\n{{collapse(' + str(_('Console port parameters')) + ')\r\n' + protocol.console + \
                        '\r\n}}\r'

            wiki += '\n\r\nh2. ' + str(_('Test Results')) + '\r\n\r' \
                    '\n|_. № |_. ' + str(_('Names')) + ': |_. ' + str(_('Results')) + \
                    ': |_. ' + str(_('Comments')) + ': |\r'

            results = TestResult.objects.filter(protocol=protocol).order_by("id")
            numbers_of_testplan = get_numbers_of_results(results)
            zipped_results = zip(results, numbers_of_testplan)
            for result, num in zipped_results:
                test_status = None
                if result.result == 0:
                    test_status = '{{checkbox(?)}}'
                elif result.result == 1:
                    test_status = '{{checkbox(0)}}'
                elif result.result == 2:
                    test_status = u'\u00b1'
                elif result.result == 3:
                    test_status = '{{checkbox(1)}}'
                # category header row
                digit = num.split('.')
                if digit[1] == '1':
                    header = '|_. ' + digit[0] + ' |' + '\\4. *' + result.test.category + '* |\n'
                else:
                    header = ''
                # test row
                wiki += header + '| ' + num + ' | [[test_result_' + str(result.id) + '|' + \
                        result.test.name + ']] |_. ' + test_status + ' | ' + result.comment + ' |\n'
        return wiki

    @staticmethod
    def export(protocol: Protocol, project: str, project_wiki: str, general_info: bool):
        r = RedmineProject()
        is_project = r.check_project(project=project)
        if is_project[0] != 200:
            return [False, is_project[1]]
        else:
            project_name = str(_('Protocol')) + ' ' + protocol.device.vendor.name + str(protocol.device)
            wiki = RedmineProtocol.build_wiki(protocol=protocol, project_name=project_name, general_info=general_info)
            is_wiki = r.create_or_update_wiki(project=project, wiki_title=project_wiki, wiki_text=wiki,
                                              parent_wiki_title='wiki')
            return is_wiki
