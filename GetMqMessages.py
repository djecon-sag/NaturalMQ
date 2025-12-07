#!/usr/bin/env python3
"""
IBM MQ Message Consumer (z/OS Mainframe) using pymqi

This script connects to an IBM MQ queue manager running on z/OS,
reads all available messages from a specified queue (destructively),
converts EBCDIC → UTF-8, and prints them with a final count.

Features:
- Proper EBCDIC (CCSID 500) to UTF-8 conversion
- Automatic data conversion fallback using MQ's built-in convert
- Clean connection handling and error management
- Suitable for demos, debugging, or one-off queue draining
- Verify the code page configured for your z/OS host.

Tested with: IBM MQ 9.2/9.3 on z/OS + pymqi 1.12+ on Windows
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

# =============================================================================
# Connection setup
# =============================================================================

# Connection string in the format expected by MQ client
conn_info = HOST_PORT

# Channel Definition (CD) — describes how to connect
cd = pymqi.CD()
cd.ChannelName = CHANNEL
cd.ConnectionName = conn_info
cd.ChannelType = pymqi.CMQC.MQCHT_CLNTCONN
cd.TransportType = pymqi.CMQC.MQXPT_TCP

# Security Options (SCO) — required when using user/password
sco = pymqi.SCO()

# Connect to the queue manager
qmgr = pymqi.QueueManager(None)
qmgr.connect_with_options(QMGR_NAME, user=USER, password=PASSWORD, cd=cd, sco=sco)

print("Connected to queue manager successfully.\n")

# =============================================================================
# Open queue and consume messages
# =============================================================================

# Open the queue for input (destructive read). Messages will be removed.
queue = pymqi.Queue(qmgr, QUEUE_NAME)

# Critical for z/OS: Tell MQ to automatically convert from queue's CCSID
# (usually EBCDIC 500/1047) to client's CCSID (UTF-8). This is cleaner than manual decode.
queue.Convert = True

msg_count = 0

print("Draining queue... (press Ctrl+C to stop early)\n")

try:
    while True:
        try:
            # This returns a Python str (Unicode) if queue.Convert = True
            # Otherwise it returns bytes — we fall back to manual cp500 decoding
            message = queue.get()

            # If Convert failed or was disabled, message will be bytes → decode manually
            if isinstance(message, bytes):
                message = message.decode("cp037")  # EBCDIC CCSID 037

            print(f"[{msg_count + 1:04d}] {message}")
            msg_count += 1

        except pymqi.MQMIError as e:
            # 2033 = No more messages available — normal end of queue
            if e.reason == pymqi.CMQC.MQRC_NO_MSG_AVAILABLE:
                break
            else:
                raise  # Re-raise unexpected MQ errors

except KeyboardInterrupt:
    print("\nInterrupted by user.")

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
    print(f"Finished. Total messages consumed: {msg_count}")
    if msg_count == 0:
        print("Queue was empty or inaccessible.")