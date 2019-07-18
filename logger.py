import logging
logging.basicConfig(filename = "reports.log",level = logging.DEBUG,format='%(asctime)s %(message)s')
logging.info("this info")
logging.warning("this warning")
logging.debug("this debug")
