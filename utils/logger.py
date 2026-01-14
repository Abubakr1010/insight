import logging

logger = logging.getLogger("insight")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()  
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

logger.debug("This is a debug message") 
logger.info("App started successfully")      
logger.warning("Something might be wrong") 
logger.error("An error occurred!")           
logger.critical("Critical failure!")    