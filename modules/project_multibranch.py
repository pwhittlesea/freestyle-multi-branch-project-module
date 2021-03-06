# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


"""
The Multi Branch Project module handles creating Multi Branch Jenkins projects.

To create a Multi Branch project, specify ``multibranch`` in the ``project-type``
attribute to the :ref:`Job` definition.
"""

import xml.etree.ElementTree as XML
import jenkins_jobs.modules.base


class MultiBranch(jenkins_jobs.modules.base.Base):
    sequence = 0

    choices_private_repo = {
        'default':
        'hudson.maven.local_repo.DefaultLocalRepositoryLocator',
        'local-to-workspace':
        'hudson.maven.local_repo.PerJobLocalRepositoryLocator',
        'local-to-executor':
        'hudson.maven.local_repo.PerExecutorLocalRepositoryLocator',
    }

    settings = {
        'default-settings':
        'jenkins.mvn.DefaultSettingsProvider',
        'settings':
        'jenkins.mvn.FilePathSettingsProvider',
        'config-file-provider-settings':
        'org.jenkinsci.plugins.configfiles.maven.job.MvnSettingsProvider',
        'default-global-settings':
        'jenkins.mvn.DefaultGlobalSettingsProvider',
        'global-settings':
        'jenkins.mvn.FilePathGlobalSettingsProvider',
        'config-file-provider-global-settings':
        'org.jenkinsci.plugins.configfiles.maven.job.'
        'MvnGlobalSettingsProvider',
    }

    def root_xml(self, data):
        xml_parent = XML.Element('freestyle-multi-branch-project')
        xml_parent.attrib['plugin'] = "multi-branch-project-plugin@0.1.3"
        if 'maven' not in data:
            return xml_parent
        if 'root-module' in data['maven']:
            root_module = XML.SubElement(xml_parent, 'rootModule')
            XML.SubElement(root_module, 'groupId').text = \
                data['maven']['root-module']['group-id']
            XML.SubElement(root_module, 'artifactId').text = \
                data['maven']['root-module']['artifact-id']
        XML.SubElement(xml_parent, 'goals').text = data['maven']['goals']

        maven_opts = data['maven'].get('maven-opts')
        if maven_opts:
            XML.SubElement(xml_parent, 'mavenOpts').text = maven_opts

        maven_name = data['maven'].get('maven-name')
        if maven_name:
            XML.SubElement(xml_parent, 'mavenName').text = maven_name

        private_repo = data['maven'].get('private-repository')
        if private_repo:
            if private_repo not in self.choices_private_repo.keys():
                raise ValueError('Not a valid private-repository "%s", '
                                 'must be one of "%s"' %
                                 (private_repo,
                                  ", ".join(self.choices_private_repo.keys())))
            XML.SubElement(xml_parent,
                           'localRepository',
                           attrib={'class':
                                   self.choices_private_repo[private_repo]})

        XML.SubElement(xml_parent, 'ignoreUpstremChanges').text = str(
            data['maven'].get('ignore-upstream-changes', True)).lower()

        XML.SubElement(xml_parent, 'rootPOM').text = \
            data['maven'].get('root-pom', 'pom.xml')
        XML.SubElement(xml_parent, 'aggregatorStyleBuild').text = 'true'
        XML.SubElement(xml_parent, 'incrementalBuild').text = 'false'
        XML.SubElement(xml_parent, 'perModuleEmail').text = 'true'
        XML.SubElement(xml_parent, 'archivingDisabled').text = str(
            not data['maven'].get('automatic-archiving', True)).lower()
        XML.SubElement(xml_parent, 'resolveDependencies').text = 'false'
        XML.SubElement(xml_parent, 'processPlugins').text = 'false'
        XML.SubElement(xml_parent, 'mavenValidationLevel').text = '-1'
        XML.SubElement(xml_parent, 'runHeadless').text = 'false'
        if 'settings' in data['maven']:
            # Support for Config File Provider
            settings_file = str(data['maven'].get('settings', ''))
            if settings_file.startswith(
                'org.jenkinsci.plugins.configfiles.maven.MavenSettingsConfig'):
                settings = XML.SubElement(
                    xml_parent,
                    'settings',
                    {'class': self.settings['config-file-provider-settings']})
                XML.SubElement(
                    settings,
                    'settingsConfigId').text = settings_file
            else:
                settings = XML.SubElement(
                    xml_parent,
                    'settings',
                    {'class': self.settings['settings']})
                XML.SubElement(settings, 'path').text = settings_file
        else:
            XML.SubElement(
                xml_parent,
                'settings',
                {'class': self.settings['default-settings']})
        if 'global-settings' in data['maven']:
            # Support for Config File Provider
            global_settings_file = str(data['maven'].get(
                'global-settings', ''))
            if global_settings_file.startswith(
                    'org.jenkinsci.plugins.configfiles.maven.'
                    'GlobalMavenSettingsConfig'):
                settings = XML.SubElement(
                    xml_parent,
                    'globalSettings',
                    {'class':
                     self.settings['config-file-provider-global-settings']})
                XML.SubElement(
                    settings,
                    'settingsConfigId').text = global_settings_file
            else:
                settings = XML.SubElement(
                    xml_parent,
                    'globalSettings',
                    {'class': self.settings['global-settings']})
                XML.SubElement(settings, 'path').text = str(
                    data['maven'].get('global-settings', ''))
        else:
            XML.SubElement(
                xml_parent,
                'globalSettings',
                {'class': self.settings['default-global-settings']})

        run_post_steps = XML.SubElement(xml_parent, 'runPostStepsIfResult')
        XML.SubElement(run_post_steps, 'name').text = 'FAILURE'
        XML.SubElement(run_post_steps, 'ordinal').text = '2'
        XML.SubElement(run_post_steps, 'color').text = 'red'

        return xml_parent
