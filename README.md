📬 **NaturalMQ**

Python & Natural Programming Language Code Samples for IBM WebSphere MQ on z/OS

NaturalMQ provides working examples of how to put, get, browse, and inspect messages on IBM MQ (WebSphere MQ) running on z/OS, using:
	
	•	Python (pymqi)
	•	Natural on z/OS

The repository is designed for developers involved in mainframe integration, modernization, and hybrid application messaging.

⸻


**Natural Programming Language Samples**


Natural Messaging is a software component that enables Natural applications to interact seamlessly with IBM MQ systems. It supports message-oriented middleware operations (PUT, GET and BROWSE) directly from Natural programs, eliminating the need for low-level MQ APIs.

This functionality is provided through structured views that define the necessary fields and parameters for MQ operations. These views can be accessed using standard Natural syntax, allowing messaging operations to integrate naturally into the programming environment.

Key features:

* PUT: Place messages in queues.
* GET: Retrieve messages from queues.
* BROWSE: Inspect messages without removing them from queues.

Natural Messaging views are accessed using the following Natural statements:

PROCESS to perform actions such as PUT or GET.

FIND to browse messages (read-only access).

General syntax:

    PROCESS MQ-QUEUE-VIEW USING
      FUNCTION     = 'PUT' | 'GET',
      QMANAGER     = queue-manager-name,
      QNAME        = queue-name,
      [optional control or message fields = value]
      [optional GIVING field-name]


MQ View

    1 MQ-QUEUE-VIEW VIEW OF MQ-QUEUE
     2 ERROR-CODE                /* MQ reason code
     2 ERROR-TEXT                /* Text describing the reason code
     2 FUNCTION                  /* Operation: GET, PUT
     2 QMANAGER                  /* Queue manager name
     2 QNAME                     /* Queue name
     2 PRIORITY                  /* Priority (0=low, 9=high)
     2 MESSAGE-10K               /* Extended message field
     2 PUT-DATE                  /* Put date (YYYYMMDD)
     2 PUT-TIME                  /* Put time (HHMMSSTH)
     2 REPLY-TO-QNAME            /* Queue name for receiving reply
     2 REPLY-TO-QMANAGER         /* Queue manager to receive reply
     2 USER-ID                   /* User ID of PUT/GET requester


📘 **Natural MQ Sample Programs**

	• BRWIBMMQ Browse MQ Queue (messages not deleted)
	• GETIBMMQ Get MQ Messages 
	• PUTIBMMQ Put MQ Messages 
	• CNTIBMMQ Count MQ Messages





🐍 Python Samples (pymqi)

	* Connect to z/OS MQ using SVRCONN channels 
	* PUT messages with correct EBCDIC encoding (cp037, cp500)
	* GET messages with automatic CCSID conversion
	* Browse queue messages without removing them
	* Query queue depth
	* .env-driven configuration (queue names, host, channel, credentials)
	* JSON message handling


📄 **Requirements**

	•	IBM MQ 9.x (z/OS or distributed)
	•	Valid SVRCONN channel configured on the mainframe
	•	Python 3.10+ recommended
	•	For Natural samples: Natural on z/OS with MQ interface enabled

**Getting Started (Python)**

1. Install dependencies


    pip install pymqi python-dotenv


2. Create your .env file

 * Copy .env_example to .env
 * Update .env using your MQ details


    QUEUE_NAME=queue-name
    QMGR_NAME=queue-manager-name
    CHANNEL=channel-name
    HOST_PORT=mqhosturl(mqhostport)
    USER=username
    PASSWORD=password

3. Run a script

  Put messages (EBCDIC-safe):

    python PutMqMessages.py

  Put a JSON message

    python PutMqJsonMessage.py

  Get messages

    python GetMqMessages.py

  Get Message Queue Depth / Browse Messages

    python MqQueueUtil.py --mode depth
    python MqQueueUtil.py --mode browse --max 10





    