##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## InitSentry
##

### INFRA
# sentry sdk import
import sentry_sdk

### LOGS
# logs import
import logging

# Init Magi's Sentry
class InitSentry():
    def __init__(self):
        logging.info("Attempt to connect to Sentry")

    def Initialize(self):
        sentry_sdk.init(
            "https://840739ef53034860b515d400dc4b6219@o1036766.ingest.sentry.io/6004367",
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=1.0
        )
        logging.info("Magi linked Sentry")
