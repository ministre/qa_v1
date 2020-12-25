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
        wiki = 'h1. ' + project_name + '\r\n\r'
        if general_info:
            wiki += '\nh2. ' + str(_('General')) + '\r\n\r' \
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
    def build_wiki(device: Device, project_name: str, general_info: bool, protocols: bool):
        wiki = 'h1. ' + project_name + '\r\n\r'
        if general_info:
            wiki += '\nh2. ' + str(_('General')) + '\r' \
                    '\n\r' \
                    '\n| ' + str(_('Device Type')) + ': | ' + device.type.name + ' |\r' \
                    '\n| ' + str(_('Vendor')) + ': | ' + device.vendor.name + ' |\r' \
                    '\n| ' + str(_('Model')) + ': | ' + device.model + ' |\r'

            if device.hw:
                wiki += '\n| ' + str(_('Hardware Version')) + ': | ' + device.hw + ' |\r'
            if device.interfaces:
                wiki += '\n| ' + str(_('Interfaces')) + ': | ' + device.interfaces + ' |\r'
            if device.leds:
                wiki += '\n| ' + str(_('Leds')) + ': | ' + device.leds + ' |\r'
            if device.buttons:
                wiki += '\n| ' + str(_('Buttons')) + ': | ' + device.buttons + ' |\r'
            if device.chipsets:
                wiki += '\n| ' + str(_('Chipsets')) + ': | ' + device.chipsets + ' |\r'
            if device.memory:
                wiki += '\n| ' + str(_('Memory')) + ': | ' + device.memory + ' |\r'

            wiki += '\n\r\nh2. Внешний вид\r\n\r'
        if protocols:
            wiki += '\nh2. ' + str(_('Protocols')) + '\r\n\r'
            device_protocols = Protocol.objects.filter(device=device).order_by('id')
            for device_protocol in device_protocols:
                wiki += '\n* [[protocol_' + str(device_protocol.id) + '|' + str(_('SW Ver.')) + ': ' + \
                        str(device_protocol.sw) + ' / ' + str(_('Date of testing')) + ': ' + \
                        str(device_protocol.date_of_start.strftime('%d.%m.%Y'))
                if device_protocol.date_of_finish:
                    wiki += ' - ' + str(device_protocol.date_of_finish.strftime('%d.%m.%Y'))
                wiki += ']]\r'

        return wiki

    @staticmethod
    def export(device: Device, project: str, project_name: str, project_desc: str, project_parent: str,
               general_info: bool, protocols: bool):
        r = RedmineProject()
        redmine_project = r.create_or_update_project(project=project, project_name=project_name,
                                                     project_desc=project_desc, project_parent=project_parent)
        if not redmine_project[0]:
            return redmine_project
        else:
            message = redmine_project[1]
            wiki = RedmineDevice.build_wiki(device=device, project_name=project_name, general_info=general_info,
                                            protocols=protocols)
            is_wiki = r.create_or_update_wiki(project=project, wiki_title='Wiki', wiki_text=wiki)
            if not is_wiki[0]:
                return is_wiki
            else:
                message += '. ' + str(is_wiki[1]) + '.'
                return [True, message]


class RedmineProtocol:
    @staticmethod
    def build_wiki(protocol: Protocol, project_name: str, general=False, results=False):
        wiki = 'h1. ' + project_name + '\r\n\r'
        if general:
            wiki += '\nh2. ' + str(_('General')) + '\r\n\r' \
                    '\n| ' + str(_('Device')) + ': | ' + protocol.device.vendor.name + ' ' + str(protocol.device) + \
                    ' |\r' \
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
                wiki += '\n\r\n{{collapse(' + str(_('System Information')) + ')\r\n<pre>' + protocol.sysinfo + \
                        '</pre>\r\n}}\r'
            if protocol.console:
                wiki += '\n\r\n{{collapse(' + str(_('Console port parameters')) + ')\r\n' + protocol.console + \
                        '\r\n}}\r'
            wiki += '\n\r\nh2. ' + str(_('Test Results')) + '\r\n\r' \
                    '\n|_. № |_. ' + str(_('Names')) + ': |_. ' + str(_('Results')) + ': |_. ' + str(_('Issues')) + \
                    ': |_. ' + str(_('Comments')) + ': |\r'
        if results:
            results = protocol.get_results(headers=True)
            for result in results:
                if result['header']:
                    wiki += '\n|_. ' + str(result['num']) + '|\\5. *' + result['category_name'] + '* |\r'
                else:
                    wiki += '\n| ' + str(result['num'][0]) + '.' + str(result['num'][1]) + ' | '
                    if result['result_id']:
                        wiki += '[[results_' + str(result['num'][0]) + '_' + str(result['num'][1]) + '_'
                        if result['result_redmine_wiki']:
                            wiki += str(result['result_redmine_wiki']) + '_'
                        wiki += str(result['result_id']) + '|' + str(result['test_name']) + ']]'
                    else:
                        wiki += str(result['test_name'])
                    wiki += ' |_. '
                    if not result['result'] or result['result'] == 0:
                        wiki += '{{checkbox(?)}}'
                    if result['result'] == 1:
                        wiki += '{{checkbox(0)}}'
                    elif result['result'] == 2:
                        wiki += u'\u00b1'
                    elif result['result'] == 3:
                        wiki += '{{checkbox(1)}}'
                    wiki += ' | '
                    for issue in result['issues']:
                        wiki += str(issue) + ' '
                    wiki += ' | '
                    if result['comment']:
                        wiki += str(result['comment'])
                    else:
                        wiki += ' |\r'
        return wiki

    @staticmethod
    def export(protocol: Protocol, project: str, project_wiki: str, general=False, results=False):
        r = RedmineProject()
        is_project = r.check_project(project=project)
        if is_project[0] != 200:
            return [False, is_project[1]]
        else:
            project_name = str(_('Protocol')) + ' ' + protocol.device.vendor.name + ' ' + str(protocol.device)
            wiki = RedmineProtocol.build_wiki(protocol=protocol, project_name=project_name, general=general,
                                              results=results)
            is_wiki = r.create_or_update_wiki(project=project, wiki_title=project_wiki, wiki_text=wiki,
                                              parent_wiki_title='wiki')
            return is_wiki
