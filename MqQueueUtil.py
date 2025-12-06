#!/usr/bin/env python3
"""
IBM MQ Queue Utility (z/OS, pymqi)

Features:
- Show current queue depth (non-destructive)
- Browse messages without removing them from the queue

Browsing:
- Uses MQOO_BROWSE + MQGMO_BROWSE_FIRST / MQGMO_BROWSE_NEXT
- Messages are *not* removed from the queue
- Attempts automatic MQ conversion; falls back to cp500 (EBCDIC) decode

Usage examples:
    python MqQueueUtil.py --mode depth
    python MqQueueUtil.py --mode browse --max 10
"""

import argparse
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


EBCDIC_CODEPAGE = "cp037"               # Typical z/OS CCSID for EBCDIC


# =============================================================================
# Common connection helper
# =============================================================================

def connect_qmgr():
    """Connect to the MQ queue manager and return qmgr handle."""
    conn_info = HOST_PORT

    cd = pymqi.CD()
    cd.ChannelName    = CHANNEL
    cd.ConnectionName = conn_info
    cd.ChannelType    = pymqi.CMQC.MQCHT_CLNTCONN
    cd.TransportType  = pymqi.CMQC.MQXPT_TCP

    sco = pymqi.SCO()

    qmgr = pymqi.QueueManager(None)
    qmgr.connect_with_options(QMGR_NAME, user=USER, password=PASSWORD, cd=cd, sco=sco)
    return qmgr


# =============================================================================
# Mode 1: Get queue depth
# =============================================================================

def show_queue_depth():
    """Inquire current queue depth (MQIA_CURRENT_Q_DEPTH) without touching messages."""
    qmgr = None
    queue = None

    try:
        qmgr = connect_qmgr()
        queue = pymqi.Queue(qmgr, QUEUE_NAME)

        depth = queue.inquire(pymqi.CMQC.MQIA_CURRENT_Q_DEPTH)
        print(f"Queue manager : {QMGR_NAME.decode(errors='ignore')}")
        print(f"Queue         : {QUEUE_NAME.decode(errors='ignore')}")
        print("-" * 60)
        print(f"Current depth : {depth} messages")

    finally:
        if queue is not None:
            try:
                queue.close()
            except Exception:
                pass
        if qmgr is not None:
            qmgr.disconnect()


# =============================================================================
# Mode 2: Browse messages non-destructively
# =============================================================================

def browse_messages(max_messages: int):
    """
    Browse up to max_messages messages without removing them.

    Uses:
      - MQOO_BROWSE | MQOO_INPUT_AS_Q_DEF
      - MQGMO_BROWSE_FIRST / MQGMO_BROWSE_NEXT
      - MQGMO_NO_SYNCPOINT | MQGMO_FAIL_IF_QUIESCING
    """
    qmgr = None
    queue = None

    try:
        qmgr = connect_qmgr()

        open_opts = (
            pymqi.CMQC.MQOO_BROWSE |
            pymqi.CMQC.MQOO_INPUT_AS_Q_DEF
        )

        queue = pymqi.Queue(qmgr, QUEUE_NAME, open_opts)
        queue.Convert = True  # Ask MQ to convert from EBCDIC queue CCSID to client CCSID where possible

        print(f"Queue manager : {QMGR_NAME.decode(errors='ignore')}")
        print(f"Queue         : {QUEUE_NAME.decode(errors='ignore')}")
        print("-" * 60)
        print(f"Browsing up to {max_messages} message(s) (non-destructive)...\n")

        # Set up MD/GMO
        md = pymqi.MD()
        gmo = pymqi.GMO()
        gmo.Options = (
            pymqi.CMQC.MQGMO_BROWSE_FIRST |
            pymqi.CMQC.MQGMO_NO_SYNCPOINT |
            pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING
        )

        count = 0

        while count < max_messages:
            try:
                # None => let MQ allocate size; MD/GMO control browse behaviour
                data = queue.get(None, md, gmo)

                # After first message, switch to BROWSE_NEXT
                gmo.Options = (
                    pymqi.CMQC.MQGMO_BROWSE_NEXT |
                    pymqi.CMQC.MQGMO_NO_SYNCPOINT |
                    pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING
                )

                # Handle conversion:
                # - If queue.Convert worked, we get str
                # - Otherwise we get bytes → manually decode as EBCDIC cp500
                if isinstance(data, bytes):
                    try:
                        text = data.decode(EBCDIC_CODEPAGE)
                    except UnicodeDecodeError:
                        # Fallback: show as hex if decoding fails
                        text = f"<binary, {len(data)} bytes> " \
                               f"hex={data.hex().upper()}"
                else:
                    text = data

                count += 1
                print(f"[{count:04d}] {text}")

            except pymqi.MQMIError as e:
                if e.reason == pymqi.CMQC.MQRC_NO_MSG_AVAILABLE:
                    # End of queue for browsing
                    if count == 0:
                        print("No messages available for browse.")
                    break
                else:
                    raise

        print("\n" + "-" * 60)
        print(f"Browse complete. Messages browsed: {count}")

    finally:
        if queue is not None:
            try:
                queue.close()
            except Exception:
                pass
        if qmgr is not None:
            qmgr.disconnect()


# =============================================================================
# CLI entry point
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="IBM MQ Queue Utility (depth / browse)")
    parser.add_argument(
        "--mode",
        choices=["depth", "browse"],
        required=True,
        help="Operation mode: 'depth' to show queue depth, 'browse' to browse messages."
    )
    parser.add_argument(
        "--max",
        type=int,
        default=10,
        help="Max messages to browse (only used with --mode browse, default=10)."
    )

    args = parser.parse_args()

    if args.mode == "depth":
        show_queue_depth()
    elif args.mode == "browse":
        browse_messages(args.max)


if __name__ == "__main__":
    main()