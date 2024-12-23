from cicd.core.logger import setup_logger

logger = setup_logger('e2e.default')
compact_logger = setup_logger('e2e.compact', fmt='%(message)s')
