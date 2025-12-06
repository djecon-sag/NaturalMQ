📬 **NaturalMQ**

Python & Natural Code Samples for IBM WebSphere MQ on z/OS

NaturalMQ provides working examples of how to put, get, browse, and inspect messages on IBM MQ (WebSphere MQ) running on z/OS, using:
	
	•	Python (pymqi)
	•	Natural on z/OS

The repository is designed for developers involved in mainframe integration, modernization, and hybrid application messaging.

⸻

✨ **Features**

🐍 Python Samples (pymqi)

	* Connect to z/OS MQ using SVRCONN channels 
	* PUT messages with correct EBCDIC encoding (cp037, cp500)
	* GET messages with automatic CCSID conversion
	* Browse queue messages without removing them
	* Query queue depth
	*.env-driven configuration (queue names, host, channel, credentials)
	* JSON message handling


📘 **Natural Samples**

	•	MQPUT and MQGET examples using Natural
	•	JSON payload integration
	•	MQMD setup for correct CCSID, FORMAT, and persistence options

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

  

