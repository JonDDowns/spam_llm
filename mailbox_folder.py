import mailbox
import os
import pickle as pkl
import yaml
import logging
logger = logging.getLogger(__name__)


class mbox_folder:
    """
    Reads in the raw Berkley Inbox files and turns them into
    a list of dictionaries. It pulls all keyed items as well as
    the email payload. A flag is added to indicate whether the
    directory is a junk folder.
    """

    def __init__(self, infile: str, junk: bool=False):
        logger.info(f'Generating mailbox object from: {infile}')
        self.infile = infile
        self.message_list = self.from_raw()
        self.junk = junk

    def from_raw(self):
        """
        This function parses the Berkley inbox file
        """
        mb = mailbox.mbox(self.infile)
        message_list = []
        for message in mb.itervalues():
            data = dict(message)
            data['Content'] = message.get_payload()[0]
            message_list.append(data)
        return message_list


if __name__ == '__main__':
    # Load config
    with open('config.yaml', 'r') as f:
        cfg = yaml.safe_load(f)

    # Turn each mailbox from config into our new class
    for x in cfg['mailbox_folders']:
        logger.info(f'Processing {x}...')

        infile = os.path.join(cfg['profile_dir'], x)
        outfile = os.path.join('data', x)
        outdir = os.path.dirname(outfile)
        if not os.path.exists(outdir):
            os.makedirs(outdir, exist_ok=False)

        junk = (x == 'Junk')

        if not os.path.exists(outfile):
            folder = mbox_folder(infile, junk=junk)
            with open(outfile, 'wb') as f:
                pkl.dump(folder, f)
            logger.info(f"New pickled mailbox at {outfile}.")
        else:
             logger.info(f'Mailbox {x} has already been processed. Skipping.')

