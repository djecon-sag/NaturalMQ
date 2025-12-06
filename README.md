📬 NaturalMQ — Python & Natural Code Samples for IBM WebSphere MQ on z/OS

NaturalMQ is a collection of sample programs demonstrating how to put, get, and browse messages on IBM WebSphere MQ (IBM MQ) running on z/OS, using both:
	•	Python (pymqi)
	•	Software AG Natural

The repository is intended for developers, system integrators, and mainframe modernization teams who want clear, working examples of how to interact with MQ queues and topics from distributed and mainframe environments.

⸻

✨ Features

🐍 Python (pymqi) Samples
	•	Connect to IBM MQ queue manager on z/OS using SVRCONN channels
	•	Put messages to MQ with proper EBCDIC encoding (ccsid cp037 / cp500)
	•	Get and auto-convert messages (UTF-8 ↔ EBCDIC)
	•	Browse messages without removing them from the queue
	•	Check queue depths programmatically
	•	Fully parameterized via .env (queue, channel, host, credentials)

📘 Natural Mainframe Samples
	•	Classic Natural code for interacting with MQ on z/OS
	•	Example modules for MQPUT and MQGET flows
	•	Demonstrates how Natural applications exchange JSON payloads with distributed systems

⸻

🗂 Repository Structure
NaturalMQ/
│
├── python/
│   ├── PutMqMessage.py          # PUT message to MQ (EBCDIC-safe)
│   ├── GetMqMessages.py         # GET & convert messages
│   ├── BrowseMqMessages.py      # Browse queue non-destructively
│   ├── QueueDepth.py            # Query queue depth using MQINQ
│   ├── env.example              # Template .env file
│   └── utils/
│       └── encoding.py          # EBCDIC helpers (cp037 / cp500)
│
├── natural/
│   ├── MQPUT.NAT                # Natural sample for MQPUT
│   ├── MQGET.NAT                # Natural sample for MQGET
│   └── MQJSON.NAT               # JSON handling example
│
└── README.md

