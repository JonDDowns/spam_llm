import yaml
from spam_llm.mailbox_folder import mbox_folder
import logging
import sys
import pickle
import os

log = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

if __name__ == '__main__':
    # Load config
    with open('config.yaml', 'r') as f:
        cfg = yaml.safe_load(f)

    # Turn each mailbox from config into our new class
    for x in cfg['mailbox_folders']:
        log.info(f'Processing {x}...')

        # Prep filepaths, make new directories if needed
        infile = os.path.join(cfg['tbird_profile_dir'], x)
        outfile = os.path.join('data', 'raw', x)
        outdir = os.path.dirname(outfile)
        if not os.path.exists(outdir):
            os.makedirs(outdir, exist_ok=False)

        # The name of junk mail folders are 'Junk'
        junk = (x == 'Junk')

        # Process file if it is not already in data subdir
        # Otherwise, notify that it was skipped b/c it exists
        if not os.path.exists(outfile):
            folder = mbox_folder(infile, junk=junk)
            with open(outfile, 'wb') as f:
                pickle.dump(folder, f)
            log.info(f"New pickled mailbox at {outfile}.")
        else:
             log.info(f'Mailbox {x} has already been processed. Skipping.')
