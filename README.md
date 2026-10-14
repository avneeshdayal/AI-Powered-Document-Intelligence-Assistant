
# AI-Powered Document Intelligence Assistant

A personal AI-powered PDF assistant built with Python, Streamlit, ChromaDB, and Google Gemini. It helps me quickly understand large volumes of academic material by summarising PDFs, finding relevant information, and answering questions from course notes, case studies, assignments, and other study documents.

## Problem Statement

During my MBA, I regularly work with multiple PDFs containing lecture notes, case studies, course materials, assignments, and reference documents. Reading through every document to find important concepts, understand a case, or prepare for discussions can be time-consuming.

I built this project to make studying more efficient by allowing me to interact with my PDFs through natural-language questions instead of manually searching through every file.

## Solution

The application uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant passages from uploaded PDFs and generate answers using Google Gemini.

It extracts text while preserving page information, splits the content into smaller chunks, indexes those chunks using ChromaDB, and retrieves relevant context for each question. The generated response is displayed alongside source references so I can return to the original material when needed.

## Features

- **Multiple PDF uploads:** Work with several study documents in one workspace.
- **Document text extraction:** Extract readable text and retain document names and page numbers.
- **Text chunking:** Split lengthy documents into smaller passages for efficient retrieval.
- **Vector search:** Use ChromaDB to find relevant passages based on a question.
- **AI-powered answers:** Generate context-based answers using Google Gemini.
- **PDF question answering:** Ask questions about concepts, definitions, frameworks, examples, and case studies.
- **Source references:** View the document, page number, and supporting text behind an answer.
- **Conversational interface:** Ask multiple questions in a chat-style interface.
- **Index status:** View the indexed PDFs and the number of text chunks created.
- **Error handling:** Display errors for indexing failures, missing API configuration, and PDFs without extractable text.

## Use Cases

I use this project to support my academic workflow, including:

- **Quick PDF summaries:** Understand the main ideas in lengthy course materials.
- **Case study analysis:** Find relevant information and evidence within case study documents.
- **Concept clarification:** Ask for explanations of management theories, models, frameworks, and technical concepts.
- **Exam preparation:** Locate definitions, key points, and important topics across study materials.
- **Assignment support:** Find relevant passages and information in reference documents.
- **Cross-document search:** Search across multiple indexed PDFs without opening each file individually.
- **Source verification:** Check which document and page contain information used in an answer.

## How It Works

```text
Upload Academic PDFs
        |
        v
Extract Text and Page Metadata
        |
        v
Split Text into Chunks
        |
        v
Create ChromaDB Vector Index
        |
        v
Ask a Question
        |
        v
Retrieve Relevant Passages
        |
        v
Send Question and Context to Gemini
        |
        v
Generate Context-Based Answer
        |
        v
Display Answer and Source References
```

## Example Questions

Questions I can ask about my study materials include:

- Summarise this PDF and highlight its key takeaways.
- Explain the main problem and recommendations in this case study.
- What are the important concepts discussed in this document?
- Explain this management framework in simple language.
- What are the main arguments and conclusions of the case?
- Compare the concepts discussed in these documents.
- Which page explains this particular concept?
- What evidence does the document provide for this conclusion?

The quality of an answer depends on the text extracted from the PDFs and the relevance of the passages retrieved by the application.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and document-processing pipeline |
| Streamlit | Interactive web interface and chat experience |
| Google Gemini API | AI-powered answer generation |
| ChromaDB | Vector storage and similarity-based retrieval |
| PyPDF | PDF text extraction |
| python-dotenv | Environment variable management |

## How to Use

1. Upload one or more PDFs from the sidebar.
2. Click **Index documents** to extract, chunk, and index the content.
3. Enter a question in the chat input.
4. Review the generated answer.
5. Expand the sources section to inspect the relevant passages and page numbers.
6. Ask additional questions or clear the current chat history when needed.


## Current Limitations

- Answer quality depends on the quality of text extraction and retrieval.
- Scanned documents may require an additional OCR pipeline.
- Answers should be checked against the original documents, particularly for academic submissions and case study analysis.
- Chat history is maintained in Streamlit session state and is not permanent database-backed history.
- Formal evaluation of retrieval quality and answer accuracy has not been established unless evaluation experiments are implemented and documented.

## Future Enhancements

- **Document summarisation mode:** Generate structured summaries with key concepts, takeaways, examples, and conclusions.
- **Study notes generation:** Turn course materials into revision notes and topic-wise summaries.
- **Case study assistant:** Extract the problem statement, stakeholders, root causes, alternatives, recommendations, and conclusions from case studies.
- **Retrieval reranking:** Improve the relevance of passages provided to the language model.
- **RAG evaluation:** Measure retrieval relevance, answer correctness, and source-grounding quality.
- **Document comparison:** Compare concepts and arguments across multiple PDFs.
- **Quiz generation:** Generate practice questions and revision quizzes from indexed study materials.
- **Feedback mechanism:** Collect feedback to identify inaccurate or unhelpful answers.

## Project Goal

The goal of this personal project is to make studying and working with large volumes of PDF-based academic material faster and more convenient. By combining document processing, vector retrieval, and generative AI, the application provides a foundation for an AI study assistant that helps me find information, understand concepts, analyse case studies, and prepare revision material more efficiently.

---

**Built with Python, Streamlit, ChromaDB, and Google Gemini.**
