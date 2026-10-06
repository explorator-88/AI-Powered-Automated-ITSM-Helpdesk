AI-Powered Intelligent ITSM Helpdesk

An AI-powered IT helpdesk prototype built for the Sorim Technologies hackathon.
The project combines React, FastAPI, RAG, FAISS, MongoDB Atlas and a ServiceNow integration layer to demonstrate how common IT support requests can be understood, answered and automated.
What problem does it solve?
In a typical company, employees raise many repetitive IT requests:
- VPN not working
- Password expired
- Account locked
- Outlook problems
- Software installation
- Application access
- General troubleshooting questions
These requests often require manual ticket creation, classification, troubleshooting and follow-up.
This project shows how AI can assist with these tasks and reduce repetitive work for IT support teams.
What does the system do?
An employee submits a request in normal language.
The system then:
Employee Request → AI Understanding → Knowledge Search / Automation → Decision → ITSM Action → Audit / Resolution
Depending on the request, the system can:
- Understand and classify the request
- Assign priority and category
- Search the approved IT knowledge base
- Provide a knowledge-grounded answer
- Perform controlled self-healing actions
- Handle software provisioning requests
- Create/update ITSM records
- Store activity and audit information
- Escalate requests when an approved solution is not available
Main Features
1. Intelligent Ticket Intake
Employees can describe their problem naturally.
For example:
“My VPN authentication is failing and I cannot connect to the corporate network.”
The system identifies the type of issue, priority, category and assignment group, retrieves relevant knowledge and creates an ITSM incident through the ServiceNow integration layer.
2. AI Knowledge Assistant
The system uses Retrieval-Augmented Generation (RAG) to answer questions using the approved IT knowledge base.
Knowledge can be added using PDF or Markdown files.
The system searches the documents using semantic similarity and provides the relevant source along with the answer.
3. Self-Healing Automation
Some common issues can be handled through predefined automation workflows.
Examples include:
- Password reset
- Account unlock
- VPN status check
- Outlook restart
The AI does not get unrestricted access to execute commands.
Only approved actions from the application's action registry can be executed.
4. Knowledge Management
New IT knowledge documents can be uploaded through the application.
The system automatically processes the document, creates chunks, generates embeddings and updates the FAISS knowledge index.
5. Software Provisioning
The application demonstrates a software request workflow using an approved software catalogue and provisioning layer.
6. ITSM Integration
The project contains a ServiceNow integration layer.
For this hackathon prototype, ServiceNow is represented using a mock adapter so that the complete workflow can be demonstrated without requiring live ServiceNow credentials.
7. Audit Trail
Important automation activity is stored in MongoDB.
This allows the system to maintain records of:
- Requests
- Automation actions
- Results
- Ticket references
- Audit information
Technology Used
Frontend
- React
- JavaScript
- Vite
- Axios
Backend
- Python
- FastAPI
AI / RAG
- Hugging Face / open-source models
- Sentence Transformers
- FAISS
- FLAN-T5
- Retrieval-Augmented Generation
Database
- MongoDB Atlas
ITSM
- ServiceNow integration layer
- Mock ServiceNow adapter
Document Processing
- PDF
- Markdown
Simple Architecture
The project is divided into a few main layers:
React
Handles the employee-facing interface.
↓
FastAPI
Controls the application workflow and APIs.
↓
AI / RAG / Automation
Understands requests, searches knowledge and selects approved automation workflows.
↓
MongoDB Atlas
Stores tickets, automation records, software requests and audit information.
↓
ServiceNow
Represents the ITSM system through the mock integration layer.
Knowledge Base
The project includes several IT support knowledge articles covering areas such as:
- VPN
- Passwords
- Outlook
- Wi-Fi
- Laptop performance
- Software installation
- Application access
Additional PDF or Markdown knowledge documents can also be uploaded through the application.
Example Scenarios
Scenario 1 — VPN Issue
Employee reports a VPN authentication problem.
The system identifies the incident, finds relevant knowledge and creates the corresponding ITSM incident.

Scenario 2 — Account Locked
Employee reports that their account is locked.
The system identifies the approved account-unlock workflow, executes the controlled action and records the result.

Scenario 3 — Upload New Knowledge
An IT administrator uploads a troubleshooting PDF.
The system processes the document and adds it to the searchable knowledge base.

Scenario 4 — Employee Question
An employee asks a troubleshooting question.
The AI searches the approved knowledge and provides an answer with its source.

Scenario 5 — Software Request
An employee requests approved software.
The request goes through the software catalogue and provisioning workflow.
AI Safety Approach
One of the important design decisions in this project is that AI is not given unrestricted control over enterprise actions.
The system uses:
- Approved knowledge
- Controlled automation actions
- Source attribution
- Validation of automation results
- Audit logging
- Human escalation when an approved automated solution is unavailable
The goal is to use AI as an intelligent assistant while keeping the actual workflow and actions under application control.
Running the Project
The project has two parts:
Backend
Python + FastAPI
Frontend
React + Vite
The backend provides the APIs and AI/RAG functionality, while the frontend provides the employee and IT support interfaces.
API documentation is available through FastAPI's interactive Swagger documentation.
Important Note
This is a hackathon prototype, not a production-ready enterprise ITSM platform.
Some components are intentionally simulated, including:
- ServiceNow integration
- Self-healing system actions
The purpose of the project is to demonstrate the complete architecture, AI/RAG workflow, automation approach, ITSM integration and engineering decisions.
Future Improvements
Some possible next steps would be:
- Connect to a real ServiceNow instance
- Connect automation to real enterprise systems
- Add authentication and role-based access
- Add stronger confidence and escalation policies
- Add human approval for high-impact actions
- Add more enterprise knowledge sources
- Add automated testing and monitoring
Final Goal
The main idea behind the project is simple:
Don't use AI only to answer questions. Use it to understand an IT request, find trusted knowledge, take controlled action when appropriate, record what happened and escalate when it cannot safely resolve the issue.
