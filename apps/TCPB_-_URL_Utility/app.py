# -*- coding: utf-8 -*-
""" ThreatConnect Playbook App """

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

# Import default Playbook Class (Required)
from playbook_app import PlaybookApp


class App(PlaybookApp):
    """ Playbook App """

    def start(self):
        self.schemes = []
        self.netlocs = []
        self.paths = []
        self.params = []
        self.queries = []
        self.fragments = []
        self.updated_urls = []

    def run(self):
        """  Run the App main logic.

        This method should contain the core logic of the App.
        """
        # todo:add support for tcentities/tcentity arrays
        urls = self.tcex.playbook.read(self.args.urls, True)

        self.tcex.log.info(f'Processing {len(urls)} urls')

        for url in urls:
            parsed_url = urlparse(url)
            self.schemes.append(parsed_url.scheme)
            self.netlocs.append(parsed_url.netloc)
            self.paths.append(parsed_url.path)
            self.params.append(parsed_url.params)
            self.queries.append(parsed_url.query)
            self.fragments.append(parsed_url.fragment)

            if self.args.remove_query_strings:
                url = url.replace(f'?{parsed_url.query}', '')

            if self.args.remove_fragments:
                url = url.replace(f'#{parsed_url.fragment}', '')

            if self.args.remove_path:
                url = url.replace(parsed_url.path, '')

            self.updated_urls.append(url)

        # set the App exit message
        self.exit_message = 'URLs processed.'

    def write_output(self):
        """ Write the Playbook output variables.

        This method should be overridden with the output variables defined in the install.json
        configuration file.
        """
        self.tcex.log.info('Writing Output')
        self.tcex.playbook.create_output('url.schemes', self.schemes, 'StringArray')
        if self.schemes:
            self.tcex.playbook.create_output('url.schemes.0', self.schemes[0], 'String')

        self.tcex.playbook.create_output('url.domainNames', self.netlocs, 'StringArray')
        if self.netlocs:
            self.tcex.playbook.create_output('url.domainNames.0', self.netlocs[0], 'String')

        self.tcex.playbook.create_output('url.paths', self.paths, 'StringArray')
        if self.paths:
            self.tcex.playbook.create_output('url.paths.0', self.paths[0], 'String')

        self.tcex.playbook.create_output('url.params', self.params, 'StringArray')
        if self.params:
            self.tcex.playbook.create_output('url.params.0', self.params[0], 'String')

        self.tcex.playbook.create_output('url.queries', self.queries, 'StringArray')
        if self.queries:
            self.tcex.playbook.create_output('url.queries.0', self.queries[0], 'String')

        self.tcex.playbook.create_output('url.fragments', self.fragments, 'StringArray')
        if self.fragments:
            self.tcex.playbook.create_output('url.fragments.0', self.fragments[0], 'String')

        self.tcex.playbook.create_output('url.updatedUrls', self.updated_urls, 'StringArray')
