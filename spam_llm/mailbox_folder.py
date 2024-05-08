"""
File: mailbox_folder.py
Author: Jon Downs
Date: 5/24/2024
Description: This creates the mbox_folder class to process a Thunderbird inbox.
             If called directly, the script processes all such inboxes and saves
             them locally to ./data/raw/[MAILBOX FILE NAME]. Requires a config.yaml
             file 
"""

import mailbox
import base64
import logging
log = logging.getLogger(__name__)


class mbox_folder:
    """
    Reads in the raw Berkley Inbox files and turns them into
    a list of dictionaries. It pulls all keyed items as well as
    the email payload. A flag is added to indicate whether the
    directory is a junk folder.
    """

    def __init__(self, infile: str, junk: bool=False):
        log.info(f'Generating mailbox object from: {infile}')
        self.infile = infile
        self.message_list = self.from_raw()
        self.junk = junk

    def from_raw(self):
        """
        This function parses the Berkley inbox file, noting if any records
        could not be formatted.
        """
        mb = mailbox.mbox(self.infile)
        message_list = []

        i = 0
        for message in mb.itervalues():
            try:
                message_list.append(self.process_message(message))
            except:
                i += 1
        if i > 0:
            log.warning(f'{i} messages could not be parsed and have been excluded.')
        return message_list


    def process_message(self, message):
        """
        Processes a single message in a mailbox file.
        Includes special handling for payloads that have base64 encoding.

        :param self: A mailbox object
        :param message: The message to be processed
        :return: A dictionary object that includes the following fields, if they were present 
        in the message: From, To, Subject, Received, Content.
        """
        # Pull out desired fields
        keys = ['From', 'To', 'Subject', 'Received']
        data = {key: value for key, value in message.items() if key in keys}

        # Pull message contents. For multipart messages, it is usually the first.
        data['multi'] = message.is_multipart()
        if data['multi']:
            content = str(message.get_payload()[0])
        else:
            content = message.get_payload(decode=True)

        # Sometimes bytes were remaining-- get rid of problematic chars
        if isinstance(content, bytes):
            content = content.decode(errors='replace')

        # If this pattern is found, let's parse the payload line by line and attempt base64
        # encoding on each. Normal text should throw an error: handle this by sending original
        # string.
        out_content = []
        if 'base64' in content:
            for line in content.split('\n'):
                    try: 
                        new = base64.b64decode(line)
                        new = new.decode('utf-8')
                        out_content.append(new)
                    except:
                        out_content.append(line)
        data['Content'] = '\n'.join(out_content)
        return data

