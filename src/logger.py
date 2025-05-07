"""
QR2Key - Logging configuration
"""

import os
import sys
from loguru import logger

def setup_logger(log_level="INFO", log_dir="logs"):
    """Configure the logger with rotation and level."""
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    logger.remove()
    
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level
    )
    
    logger.add(
        os.path.join(log_dir, "qr2key_{time:YYYY-MM-DD}.log"),
        rotation="1 day",    # Rotate daily
        retention="7 days",  # Keep logs for 7 days
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=log_level,
        compression="zip"    # Compress rotated logs
    )
    
    logger.info(f"Logger initialized with level {log_level}")
    logger.info(f"Log files will be stored in {os.path.abspath(log_dir)}")
    
    return logger
