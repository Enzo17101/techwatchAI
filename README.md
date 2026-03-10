# **TechWatch AI \- Intelligent Monitoring and RAG Platform**

TechWatch AI is a full-stack monitoring platform designed to automate technology watch. It leverages Retrieval-Augmented Generation (RAG) to provide a chat interface capable of answering queries based specifically on recently processed technical articles.  
The project is built using a microservices architecture, combining a robust Spring Boot backend, a specialized FastAPI worker for AI tasks, and a modern Next.js frontend.

## **Architecture Overview**

The system consists of three specialized services:

### **1\. Java Orchestrator (Spring Boot)**

* Role: Core business logic and data persistence.  
* Features:  
  * Automated RSS feed polling via Spring Scheduling.  
  * Asynchronous processing of incoming articles.  
  * Relational data management with PostgreSQL.  
  * Centralized RESTful API for the frontend.

### **2\. Python AI Worker (FastAPI)**

* Role: Specialized AI processing and web scraping.  
* Features:  
  * Advanced Scraping: Content extraction using BeautifulSoup with DOM sanitization.  
  * Vectorization: Embedding generation using the nomic-embed-text model via Ollama.  
  * Semantic Search: High-performance vector retrieval using pgvector.  
  * RAG Pipeline: Contextual answer generation using Large Language Models.

### **3\. Next.js Frontend**

* Role: Interactive user dashboard.  
* Features:  
  * Real-time monitoring feed.  
  * Intelligent Chat Interface with full session history.  
  * Responsive design with Tailwind CSS and system-aware dark mode.

## **AI and RAG Implementation**

TechWatch AI implements a Retrieval-Augmented Generation workflow to ensure response accuracy and minimize hallucinations:

1. Ingestion: Articles are scraped and cleaned to remove non-essential elements such as scripts, headers, and footers.  
2. Embedding: Text is converted into 768-dimension vectors and stored in PostgreSQL using the pgvector extension.  
3. Retrieval: User queries are vectorized to perform a semantic search, retrieving the most relevant context snippets from the database.  
4. Generation: The LLM processes the query alongside the retrieved context to produce a grounded, professional response.

## **Technical Stack**

### **Backend Orchestrator**

* Language: Java 21  
* Framework: Spring Boot 3.2, Spring Data JPA  
* Database: PostgreSQL 16 with pgvector  
* Build Tool: Maven

### **AI Worker**

* Language: Python 3.11+  
* Framework: FastAPI, SQLAlchemy  
* AI Integration: Ollama (nomic-embed-text, qwen family)  
* Scraping: BeautifulSoup4, Requests

### **Frontend**

* Framework: Next.js (App Router), TypeScript  
* Styling: Tailwind CSS, Lucide React  
* API Client: Axios

### **Infrastructure**

* Containerization: Docker and Docker Compose

## **Key Highlights**

* Cross-Language Integration: Demonstrates a scalable bridge between a Java enterprise backend and a Python AI service.  
* Smart Truncation: Implements custom logic to handle LLM context windows by preventing word splitting during content processing.  
* Unified Database: Direct integration of semantic search within a relational PostgreSQL database, avoiding the need for a separate vector-only store.  
* Production-Ready Code: Focus on error handling, logging, and asynchronous task management.