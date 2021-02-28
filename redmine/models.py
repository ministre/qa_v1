from redminelib import Redmine
from qa_v1 import settings
from redminelib.exceptions import ResourceNotFoundError, ForbiddenError, AuthError, ValidationError
from device.models import DeviceType, Device, DevicePhoto, DeviceSample, DeviceSampleAccount
from testplan.models import Test, TestConfig, TestImage, TestFile, TestLink, TestComment, TestPlan, Category
from protocol.models import Protocol, TestResult, TestResultNote, TestResultConfig, TestResultImage, TestResultIssue
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
                    return [False, _('Parent project error') + ': ' + str(is_parent_project[1])]
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

    def create_or_update_wiki(self, project: str, wiki_text: str, wiki_title='Wiki', parent_wiki_title=None):
        if parent_wiki_title:
            is_parent_wiki = self.get_wiki(project=project, wiki_title=parent_wiki_title)
            if is_parent_wiki[0] != 200:
                return [False, str(_('Parent Wiki error')) + ': ' + str(is_parent_wiki[1])]
        is_wiki = self.get_wiki(project=project, wiki_title=wiki_title)
        if is_wiki[0] == 200:
            if parent_wiki_title:
                self.redmine.wiki_page.update(wiki_title, project_id=project, text=wiki_text,
                                              parent_title=parent_wiki_title)
            else:
                self.redmine.wiki_page.update(wiki_title, project_id=project, text=wiki_text)
            return [True, _('Wiki updated')]
        elif is_wiki[0] == 404:
            if parent_wiki_title:
                self.redmine.wiki_page.create(project_id=project, title=wiki_title, text=wiki_text,
                                              parent_title=parent_wiki_title)
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
            is_wiki = r.create_or_update_wiki(project=project, wiki_text=wiki)
            if not is_wiki[0]:
                return is_wiki
            else:
                message += '. ' + str(is_wiki[1]) + '.'
                return [True, message]


class RedmineDevice:
    @staticmethod
    def build_wiki(device: Device, project_name: str, general=False, photos=False, samples=False, protocols=False):
        wiki = 'h1. ' + project_name + '\r\n\r'
        if general:
            wiki += '\nh2. ' + str(_('General Information')) + '\r' \
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

        if photos:
            wiki += '\n\r\nh2. ' + str(_('Photos')) + '\r\n\r'
            photos = DevicePhoto.objects.filter(device=device).order_by('id')
            for photo in photos:
                wiki += '\n{{collapse(' + photo.desc + ')\r'
                wiki += '\n!'
                if photo.width or photo.height:
                    wiki += '{'
                    if photo.width:
                        wiki += 'width:' + str(photo.width) + 'px;'
                    if photo.height:
                        wiki += 'height:' + str(photo.height) + 'px;'
                    wiki += '}'
                wiki += settings.REDMINE_MEDIA_ROOT + str(photo.photo) + '!\r\n}}\r\n\r'

        if samples:
            wiki += '\n\r\nh2. ' + str(_('Samples')) + '\r\n\r'
            samples = DeviceSample.objects.filter(device=device).order_by('id')
            for sample in samples:
                wiki += '\n\r'
                if sample.sn:
                    wiki += '\n| ' + str(_('Serial Number')) + ': | ' + sample.sn + ' |\r'
                if sample.sn:
                    wiki += '\n| ' + str(_('Description')) + ': | ' + sample.desc + ' |\r'
                accounts = DeviceSampleAccount.objects.filter(sample=sample)
                for account in accounts:
                    wiki += '\n| ' + str(_('Username')) + ': | ' + account.username + ' |\r'
                    wiki += '\n| ' + str(_('Password')) + ': | ' + account.password + ' |\r'
                wiki += '\n\r'

        if protocols:
            wiki += '\nh2. ' + str(_('Protocols')) + '\r\n\r'
            device_protocols = Protocol.objects.filter(device=device).order_by('id')
            for device_protocol in device_protocols:
                wiki += '\n* [[Protocol_' + str(device_protocol.id) + '|' + str(_('SW Ver.')) + ': ' + \
                        str(device_protocol.sw) + ' / ' + str(_('Date of testing')) + ': ' + \
                        str(device_protocol.date_of_start.strftime('%d.%m.%Y'))
                if device_protocol.date_of_finish:
                    wiki += ' - ' + str(device_protocol.date_of_finish.strftime('%d.%m.%Y'))
                wiki += ']]\r'

        return wiki

    @staticmethod
    def export(device: Device, project: str, project_name: str, project_desc: str, project_parent: str,
               general=False, photos=False, samples=False, protocols=False):
        r = RedmineProject()
        redmine_project = r.create_or_update_project(project=project, project_name=project_name,
                                                     project_desc=project_desc, project_parent=project_parent)
        if not redmine_project[0]:
            return redmine_project
        else:
            message = redmine_project[1]
            wiki = RedmineDevice.build_wiki(device=device, project_name=project_name, general=general,
                                            photos=photos, samples=samples, protocols=protocols)
            is_wiki = r.create_or_update_wiki(project=project, wiki_text=wiki)
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
                        if result['result_redmine_wiki']:
                            wiki += '[[' + str(result['result_redmine_wiki']) + '|' + str(result['test_name']) + ']]'
                        else:
                            wiki += str(result['test_name'])
                        if result['configs']:
                            wiki += ' ' + u'\u2699'
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
            is_wiki = r.create_or_update_wiki(project=project, wiki_text=wiki, wiki_title=project_wiki,
                                              parent_wiki_title='wiki')
            return is_wiki


class RedmineResult:
    @staticmethod
    def build_wiki(result: TestResult, test_desc=False, result_notes=False, result_configs=False,
                   result_images=False, result_summary=False):
        # header
        wiki = '\n' + str(_('Protocol')) + ' ' + str(result.protocol.device.vendor.name) + ' ' + \
               str(result.protocol.device) + u' \u00bb ' + str(result.test.get_num()[0]) + '. ' + \
               str(result.test.cat) + u' \u00bb ' + str(result.test.get_num()[0]) + '.' + \
               str(result.test.get_num()[1]) + '. ' + str(result.test) + '\r\n\r'
        # test description
        wiki += '\nh1. ' + str(_('Test description')) + '\r\n\r'
        if test_desc:
            if result.test.purpose:
                wiki += '\nh2. ' + str(_('Purpose')) + '\r\n\r'
                wiki += '\n' + result.test.purpose + '\r\n\r'
            if result.test.procedure:
                wiki += '\nh2. ' + str(_('Procedure')) + '\r\n\r'
                wiki += '\n' + result.test.procedure + '\r\n\r'
            if result.test.expected:
                wiki += '\nh2. ' + str(_('Expected result')) + '\r\n\r'
                wiki += '\n' + result.test.expected + '\r\n\r'
        wiki += '\n---\r\n\r'
        # test details
        wiki += '\nh1. ' + str(_('Result details')) + '\r\n\r'
        # notes
        if result_notes:
            notes = TestResultNote.objects.filter(result=result).order_by('id')
            if notes:
                wiki += '\nh2. ' + str(_('Notes')) + '\r\n\r'
            for note in notes:
                if note.desc:
                    wiki += '\nh3. ' + note.desc + '\r\n\r'
                if note.format == 0:
                    wiki += '\n' + note.text + '\r\n\r'
                else:
                    wiki += '\n<pre>' + note.text + '</pre>\r\n\r'
        # configs
        if result_configs:
            configs = TestResultConfig.objects.filter(result=result).order_by('id')
            if configs:
                wiki += '\nh2. ' + str(_('Configurations')) + '\r\n\r'
            for config in configs:
                if config.desc:
                    wiki += '\nh3. ' + config.desc + '\r\n\r'
                if config.lang == 'json':
                    config.lang = 'javascript'
                wiki += '\n<pre><code class="' + config.lang + '">\r' + \
                        '\n' + config.config + '\r' + \
                        '\n</code></pre>\r\n\r'
        # images
        if result_images:
            images = TestResultImage.objects.filter(result=result).order_by('id')
            if images:
                wiki += '\nh2. ' + str(_('Images')) + '\r\n\r'
            for image in images:
                if image.desc:
                    wiki += '\nh3. ' + image.desc + '\r\n\r'
                wiki += '\n!'
                if image.width or image.height:
                    wiki += '{'
                    if image.width:
                        wiki += 'width:' + str(image.width) + 'px;'
                    if image.height:
                        wiki += 'height:' + str(image.height) + 'px;'
                    wiki += '}'
                wiki += settings.REDMINE_MEDIA_ROOT + str(image.image) + '!\r\n\r'
        # summary
        if result_summary:
            wiki += '\nh1. ' + str(_('Result')) + '\r\n\r'
            res = '%{background:gray}' + str(_('Not tested')) + '%'
            if result.result == 1:
                res = '%{background:red}' + str(_('Not passed')) + '%'
            elif result.result == 2:
                res = '%{background:yellow}' + str(_('Passed with warning')) + '%'
            elif result.result == 3:
                res = '%{background:lightgreen}' + str(_('Passed')) + '%'

            wiki += '\n' + res + '\r\n\r'
            if result.comment:
                wiki += '\nh2. ' + str(_('Comment')) + '\r\n\r' + \
                        '\n' + result.comment + '\r\n\r'
            issues = TestResultIssue.objects.filter(result=result).order_by('id')
            if issues:
                wiki += '\nh2. ' + str(_('Issues')) + '\r\n\r'
                for issue in issues:
                    wiki += '\n# ' + issue.text + '\r'
        return wiki

    @staticmethod
    def export(result: TestResult, project: str, project_wiki: str, project_parent_wiki: str, test_desc=False,
               result_notes=False, result_configs=False, result_images=False, result_summary=False):
        r = RedmineProject()
        is_project = r.check_project(project=project)
        if is_project[0] != 200:
            return [False, is_project[1]]
        else:
            wiki = RedmineResult.build_wiki(result=result, test_desc=test_desc, result_notes=result_notes,
                                            result_configs=result_configs, result_images=result_images,
                                            result_summary=result_summary)
            is_wiki = r.create_or_update_wiki(project=project, wiki_text=wiki, wiki_title=project_wiki,
                                              parent_wiki_title=project_parent_wiki)
            return is_wiki


class RedmineTest:
    @staticmethod
    def export(test: Test, project: str, project_wiki: str, configs=False, images=False,
               files=False, links=False, comments=False):
        r = RedmineProject()
        is_project = r.check_project(project=project)
        if is_project[0] != 200:
            return [False, is_project[1]]
        else:
            wiki = RedmineTest.build_wiki(test=test, configs=configs, images=images, files=files, links=links,
                                          comments=comments)
            is_wiki = r.create_or_update_wiki(project=project, wiki_text=wiki, wiki_title=project_wiki)
            return is_wiki

    @staticmethod
    def build_wiki(test: Test, configs=False, images=False, files=False, links=False, comments=False):
        wiki = 'h1. ' + test.name + '\r\n\r'
        wiki += RedmineTest.get_details(test=test, configs=configs, images=images, files=files, links=links,
                                        comments=comments)
        return wiki

    @staticmethod
    def get_details(test: Test, configs=False, images=False, files=False, links=False, comments=False):
        wiki = '\nh2. ' + str(_('Category')) + '\r\n\r'
        wiki += '\n' + test.cat.name + '\r\n\r'
        if test.purpose:
            wiki += '\nh2. ' + str(_('Purpose')) + '\r\n\r'
            wiki += '\n' + test.purpose + '\r\n\r'
        if test.procedure:
            wiki += '\nh2. ' + str(_('Procedure')) + '\r\n\r'
            wiki += '\n' + test.procedure + '\r\n\r'
        if test.expected:
            wiki += '\nh2. ' + str(_('Expected result')) + '\r\n\r'
            wiki += '\n' + test.expected + '\r\n\r'
        if configs:
            test_configs = TestConfig.objects.filter(test=test).order_by('id')
            if test_configs:
                wiki += '\nh2. ' + str(_('Configurations')) + '\r\n\r'
                for test_config in test_configs:
                    if test_config.parent:
                        if test_config.parent.desc:
                            wiki += '\nh3. ' + test_config.parent.desc + '\r\n\r'
                        if test_config.parent.lang == 'json':
                            test_config.parent.lang = 'javascript'
                        wiki += '\n<pre><code class="' + test_config.parent.lang + '">\r' + \
                                '\n' + test_config.parent.config + '\r' + \
                                '\n</code></pre>\r\n\r'
                    else:
                        if test_config.desc:
                            wiki += '\nh3. ' + test_config.desc + '\r\n\r'
                        if test_config.lang == 'json':
                            test_config.lang = 'javascript'
                        wiki += '\n<pre><code class="' + test_config.lang + '">\r' + \
                                '\n' + test_config.config + '\r' + \
                                '\n</code></pre>\r\n\r'
        if images:
            test_images = TestImage.objects.filter(test=test).order_by('id')
            if test_images:
                wiki += '\nh2. ' + str(_('Images')) + '\r\n\r'
                for test_image in test_images:
                    if test_image.parent:
                        if test_image.parent.desc:
                            wiki += '\nh3. ' + test_image.parent.desc + '\r\n\r'
                        wiki += '\n!'
                        if test_image.parent.width or test_image.parent.height:
                            wiki += '{'
                            if test_image.parent.width:
                                wiki += 'width:' + str(test_image.parent.width) + 'px;'
                            if test_image.parent.height:
                                wiki += 'height:' + str(test_image.parent.height) + 'px;'
                            wiki += '}'
                        wiki += settings.REDMINE_MEDIA_ROOT + str(test_image.parent.image) + '!\r\n\r'
                    else:
                        if test_image.desc:
                            wiki += '\nh3. ' + test_image.desc + '\r\n\r'
                        wiki += '\n!'
                        if test_image.width or test_image.height:
                            wiki += '{'
                            if test_image.width:
                                wiki += 'width:' + str(test_image.width) + 'px;'
                            if test_image.height:
                                wiki += 'height:' + str(test_image.height) + 'px;'
                            wiki += '}'
                        wiki += settings.REDMINE_MEDIA_ROOT + str(test_image.image) + '!\r\n\r'
        if files:
            test_files = TestFile.objects.filter(test=test).order_by('id')
            if test_files:
                wiki += '\nh2. ' + str(_('Files')) + '\r\n\r'
                for test_file in test_files:
                    if test_file.parent:
                        if test_file.parent.desc:
                            wiki += '\nh3. ' + test_file.parent.desc + '\r\n\r'
                        wiki += settings.REDMINE_MEDIA_ROOT + str(test_file.parent.file) + '\r\n\r'
                    else:
                        if test_file.desc:
                            wiki += '\nh3. ' + test_file.desc + '\r\n\r'
                        wiki += settings.REDMINE_MEDIA_ROOT + str(test_file.file) + '\r\n\r'
        if links:
            test_links = TestLink.objects.filter(test=test).order_by('id')
            if test_links:
                wiki += '\nh2. ' + str(_('Links')) + '\r\n\r'
                for test_link in test_links:
                    if test_link.parent:
                        if test_link.parent.desc:
                            wiki += '\nh3. ' + test_link.parent.desc + '\r\n\r'
                        wiki += '\n' + str(test_link.parent.url) + '\r\n\r'
                    else:
                        if test_link.desc:
                            wiki += '\nh3. ' + test_link.desc + '\r\n\r'
                        wiki += '\n' + str(test_link.url) + '\r\n\r'
        if comments:
            test_comments = TestComment.objects.filter(test=test).order_by('id')
            if test_comments:
                wiki += '\nh2. ' + str(_('Comments')) + '\r\n\r'
                for test_comment in test_comments:
                    if test_comment.parent:
                        if test_comment.parent.desc:
                            wiki += '\nh3. ' + test_comment.parent.desc + '\r\n\r'
                        if test_comment.parent.format > 0:
                            wiki += '\n<pre>' + str(test_comment.parent.text) + '</pre>\r\n\r'
                        else:
                            wiki += '\n' + str(test_comment.parent.text) + '\r\n\r'
                    else:
                        if test_comment.desc:
                            wiki += '\nh3. ' + test_comment.desc + '\r\n\r'
                        if test_comment.format > 0:
                            wiki += '\n<pre>' + str(test_comment.text) + '</pre>\r\n\r'
                        else:
                            wiki += '\n' + str(test_comment.text) + '\r\n\r'

        return wiki


class RedmineTestplan:
    @staticmethod
    def export(testplan: TestPlan, project: str, test_list=False, test_details_wiki=False):
        r = RedmineProject()
        is_project = r.check_project(project=project)
        if is_project[0] != 200:
            return [False, is_project[1]]
        else:
            wiki = RedmineTestplan.build_wiki(testplan=testplan, test_list=test_list)
            is_wiki = r.create_or_update_wiki(project=project, wiki_text=wiki)

            if test_details_wiki:
                if is_wiki[0]:
                    RedmineTestplan.create_or_update_test_details_wiki(testplan=testplan, project=project)

            return is_wiki

    @staticmethod
    def build_wiki(testplan: TestPlan, test_list=False):
        wiki = 'h1. ' + str(_('Testplan')) + ' ' + testplan.name + ' (' + testplan.version + ')\r\n\r'
        if test_list:
            wiki += '\nh2. ' + str(_('Test list')) + '\r\n\r'
            categories = Category.objects.filter(testplan=testplan).order_by('priority')
            for category in categories:
                wiki += '\nh3. ' + category.name + '\r\n\r'
                tests = Test.objects.filter(cat=category).order_by('priority')
                for test in tests:
                    if test.redmine_wiki:
                        wiki += '\n* [[' + test.redmine_wiki + '|' + test.name + ']]\r'
                    else:
                        wiki += '\n* ' + test.name + '\r'
                wiki += '\n\r'
        return wiki

    @staticmethod
    def create_or_update_test_details_wiki(testplan: TestPlan, project: str):
        categories = Category.objects.filter(testplan=testplan).order_by('priority')
        for category in categories:
            tests = Test.objects.filter(cat=category).order_by('priority')
            for test in tests:
                if test.redmine_wiki:
                    RedmineTest.export(test=test, project=project, project_wiki=test.redmine_wiki,
                                       configs=True, images=True, files=True, links=True, comments=True)
