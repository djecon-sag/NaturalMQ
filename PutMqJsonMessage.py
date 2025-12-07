#!/usr/bin/env python3
"""
IBM MQ Message Producer (z/OS Mainframe) using pymqi

This script connects to an IBM MQ queue manager running on z/OS and
puts a configurable number of text messages onto a target queue.

Key points:
- Messages are generated as random ASCII text (up to 80 chars)
- Text is explicitly encoded to EBCDIC CCSID 500 (cp500) before PUT
- MQMD is set with CodedCharSetId=500 and MQFMT_STRING
- Uses the same connection pattern as the consumer script
- Verify the code page configured for your z/OS host.

Adjust QMGR_NAME, CHANNEL, HOST_PORT, QUEUE_NAME, USER, PASSWORD
for your environment as needed.
"""

import pymqi
from dotenv import load_dotenv
import os

# =============================================================================
# Configuration — Update these values for your environment
# =============================================================================
load_dotenv()
QUEUE_NAME = os.getenv("QUEUE_NAME")
QMGR_NAME  = os.getenv("QMGR_NAME")
CHANNEL    = os.getenv("CHANNEL")
HOST_PORT  = os.getenv("HOST_PORT")
USER       = os.getenv("USER")
PASSWORD   = os.getenv("PASSWORD")

print("IBM MQ Message Drainer")
print(f"Host      :", HOST_PORT)
print(f"Channel   :", CHANNEL)
print(f"Queue     :", QUEUE_NAME)
print(f"Queue Mgr :", QMGR_NAME)
print("-" * 60)

# Convert to bytes for pymqi
QUEUE_NAME = QUEUE_NAME.encode()
QMGR_NAME  = QMGR_NAME.encode()
CHANNEL    = CHANNEL.encode()
HOST_PORT  = HOST_PORT.encode()
USER       = USER.encode()
PASSWORD   = PASSWORD.encode()

# Message generation
NUM_MESSAGES     = 1         # How many messages to send
EBCDIC_CODEPAGE  = "cp037"

# =============================================================================
# Connection setup
# =============================================================================

print("IBM MQ Message Producer")
print(f"Host      : {HOST_PORT.decode(errors='ignore')}")
print(f"Queue     : {QUEUE_NAME.decode(errors='ignore')}")
print(f"Queue Mgr : {QMGR_NAME.decode(errors='ignore')}")
print("-" * 60)

# Connection string in the format expected by MQ client
conn_info = HOST_PORT

# Channel Definition (CD) — describes how to connect
cd = pymqi.CD()
cd.ChannelName     = CHANNEL
cd.ConnectionName  = conn_info
cd.ChannelType     = pymqi.CMQC.MQCHT_CLNTCONN
cd.TransportType   = pymqi.CMQC.MQXPT_TCP

# Security Options (SCO) — required when using user/password
sco = pymqi.SCO()

# Connect to the queue manager
qmgr = pymqi.QueueManager(None)
qmgr.connect_with_options(QMGR_NAME, user=USER, password=PASSWORD, cd=cd, sco=sco)

print("Connected to queue manager successfully.\n")

# =============================================================================
# Open queue for output and put messages
# =============================================================================

open_options = pymqi.CMQC.MQOO_OUTPUT
queue = pymqi.Queue(qmgr, QUEUE_NAME, open_options)

# MQMD (message descriptor) and PMO (put message options)
md = pymqi.MD()
md.Format          = pymqi.CMQC.MQFMT_STRING
md.CodedCharSetId  = 500  # EBCDIC CCSID 500 on z/OS

pmo = pymqi.PMO()
pmo.Options = pymqi.CMQC.MQPMO_NO_SYNCPOINT

print(f"Putting {NUM_MESSAGES} messages (EBCDIC {EBCDIC_CODEPAGE})...\n")

try:
    for i in range(1, NUM_MESSAGES + 1):

        text = """[{"ISN_EMPLOYEES":1,"PERSONNEL_ID":"50005800","FIRST_NAME":"SIMONE","NAME":"SMITH","MIDDLE_NAME":"SARAH","MAR_STAT":"M","SEX":"F","BIRTH":"1990-12-04","CITY":"JOIGNY","POST_CODE":"89300","COUNTRY":"F  ","AREA_CODE":"1033","PHONE":"44864858","DEPT":"","JOB_TITLE":"CHEF DE SERVICE","LEAVE_DUE":19,"LEAVE_TAKEN":5,"LEAVE_LEFT":"8fnw9Q==","DEPARTMENT":"    ","DEPT_PERSON":"      SMITH"}]"""
        # Explicitly encode to EBCDIC bytes before PUT
        data_ebcdic = text.encode(EBCDIC_CODEPAGE)

        # Optional: show first message as hex for verification

        queue.put(data_ebcdic, md, pmo)
        print(f"[{i:04d}] Sent ({len(data_ebcdic)} bytes EBCDIC): {text}")

except pymqi.MQMIError as e:
    print(f"\nMQ Error while putting messages: {e}")
    raise

finally:
    # =============================================================================
    # Cleanup — always close handles and disconnect
    # =============================================================================
    try:
        queue.close()
    except Exception:
        pass

    qmgr.disconnect()

    print("-" * 60)
    print(f"Finished. Total messages sent: {NUM_MESSAGES}")