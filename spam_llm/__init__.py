"""
File: spam_llm/__init__.py
Author: Jon Downs
Date: 5/24/2024
Description: This sets up the supporting library for the spam_llm project.
"""

from spam_llm import mailbox_folder
from spam_llm import compute_metrics
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
