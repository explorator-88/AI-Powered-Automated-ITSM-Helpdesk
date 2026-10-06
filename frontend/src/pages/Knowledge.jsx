import { useState } from "react";

import api from "../services/api";


export default function Knowledge() {

    const articles = [
        {
            id: "KB001",
            title: "VPN Authentication Failure",
            category: "Network",
            subcategory: "VPN",
            owner: "Network Support",
            priority: "P2",
        },
        {
            id: "KB002",
            title: "Password Expired or Password Reset Required",
            category: "Account and Access",
            subcategory: "Password",
            owner: "Identity and Access Management",
            priority: "P2",
        },
        {
            id: "KB003",
            title: "Outlook Email Synchronization and Connectivity",
            category: "Collaboration",
            subcategory: "Outlook",
            owner: "Collaboration Support",
            priority: "P3",
        },
        {
            id: "KB004",
            title: "Corporate Wi-Fi Connectivity Problem",
            category: "Network",
            subcategory: "Wi-Fi",
            owner: "Network Support",
            priority: "P3",
        },
        {
            id: "KB005",
            title: "Slow Laptop or Poor System Performance",
            category: "Hardware and Performance",
            subcategory: "Laptop Performance",
            owner: "End User Computing",
            priority: "P3",
        },
        {
            id: "KB006",
            title: "Approved Software Installation Request",
            category: "Software and Applications",
            subcategory: "Software Installation",
            owner: "Endpoint Management",
            priority: "P3",
        },
        {
            id: "KB007",
            title: "Corporate Application Access Request",
            category: "Account and Access",
            subcategory: "Application Access",
            owner: "Identity and Access Management",
            priority: "P2",
        },
    ];


    // --------------------------------------------------
    // UPLOAD STATE
    // --------------------------------------------------

    const [selectedFile, setSelectedFile] =
        useState(null);

    const [uploading, setUploading] =
        useState(false);

    const [uploadResult, setUploadResult] =
        useState(null);

    const [error, setError] =
        useState("");


    // --------------------------------------------------
    // KNOWLEDGE ASSISTANT STATE
    // --------------------------------------------------

    const [question, setQuestion] =
        useState("");

    const [answer, setAnswer] =
        useState(null);

    const [asking, setAsking] =
        useState(false);

    const [chatError, setChatError] =
        useState("");


    // --------------------------------------------------
    // FILE SELECTION
    // --------------------------------------------------

    const handleFileChange = (event) => {

        const file =
            event.target.files[0];


        setError("");
        setUploadResult(null);


        if (!file) {

            setSelectedFile(null);

            return;
        }


        const extension =
            file.name
                .split(".")
                .pop()
                .toLowerCase();


        if (
            !["pdf", "md"].includes(
                extension
            )
        ) {

            setSelectedFile(null);

            setError(
                "Please select a PDF or Markdown (.md) file."
            );

            return;
        }


        setSelectedFile(file);
    };


    // --------------------------------------------------
    // UPLOAD KNOWLEDGE DOCUMENT
    // --------------------------------------------------

    const handleUpload = async () => {

        if (!selectedFile) {

            setError(
                "Please select a knowledge document first."
            );

            return;
        }


        setUploading(true);
        setError("");
        setUploadResult(null);


        const formData =
            new FormData();


        formData.append(
            "file",
            selectedFile
        );


        try {

            const response =
                await api.post(
                    "/knowledge/upload",
                    formData,
                    {
                        headers: {
                            "Content-Type":
                                "multipart/form-data",
                        },
                    }
                );


            setUploadResult(
                response.data
            );


            setSelectedFile(null);


            const fileInput =
                document.getElementById(
                    "knowledge-file-input"
                );


            if (fileInput) {
                fileInput.value = "";
            }


        } catch (err) {

            const message =
                err.response?.data?.detail ||
                "Knowledge document upload failed.";


            setError(message);


        } finally {

            setUploading(false);
        }
    };


    // --------------------------------------------------
    // ASK KNOWLEDGE BASE
    // --------------------------------------------------

    const handleAskQuestion =
        async () => {

            if (!question.trim()) {

                setChatError(
                    "Please enter a question."
                );

                return;
            }


            setAsking(true);
            setChatError("");
            setAnswer(null);


            try {

                const response =
                    await api.post(
                        "/chat",
                        {
                            message:
                                question.trim(),
                        }
                    );


                setAnswer(
                    response.data
                );


            } catch (err) {

                const message =
                    err.response?.data?.detail ||
                    "Unable to retrieve an answer from the knowledge base.";


                setChatError(message);


            } finally {

                setAsking(false);
            }
        };


    // --------------------------------------------------
    // PAGE
    // --------------------------------------------------

    return (

        <div>

            {/* PAGE HEADER */}

            <div className="page-header">

                <h1>
                    Knowledge Base
                </h1>

                <p>
                    Approved enterprise knowledge used
                    by the AI retrieval and self-service
                    workflows.
                </p>

            </div>


            {/* ==========================================
                KNOWLEDGE INGESTION
            ========================================== */}

            <div className="panel knowledge-upload-panel">

                <div className="panel-header">

                    <div>

                        <h2>
                            Knowledge Ingestion
                        </h2>

                        <p className="panel-description">

                            Upload a PDF or Markdown knowledge
                            document to automatically process,
                            embed, and index it for RAG.

                        </p>

                    </div>


                    <span className="kb-status">
                        RAG Active
                    </span>

                </div>


                <div className="knowledge-upload-area">

                    <div className="upload-input-section">

                        <label
                            htmlFor="knowledge-file-input"
                            className="upload-label"
                        >
                            Select Knowledge Document
                        </label>


                        <input
                            id="knowledge-file-input"
                            type="file"
                            accept=".pdf,.md"
                            onChange={
                                handleFileChange
                            }
                        />


                        <p className="upload-help">

                            Supported formats:
                            PDF and Markdown

                        </p>

                    </div>


                    {selectedFile && (

                        <div className="selected-file">

                            <div>

                                <strong>
                                    {selectedFile.name}
                                </strong>

                                <span>
                                    {
                                        (
                                            selectedFile.size /
                                            1024
                                        ).toFixed(1)
                                    } KB
                                </span>

                            </div>

                        </div>

                    )}


                    <button
                        className="primary-button"
                        onClick={handleUpload}
                        disabled={
                            !selectedFile ||
                            uploading
                        }
                    >

                        {uploading
                            ? "Processing & Indexing..."
                            : "Upload & Index Knowledge"}

                    </button>

                </div>


                {/* UPLOAD SUCCESS */}

                {uploadResult && (

                    <div className="upload-success">

                        <strong>
                            Knowledge document
                            indexed successfully
                        </strong>


                        <p>
                            {uploadResult.file_name}
                        </p>


                        <div className="upload-result-stats">

                            <span>
                                Chunks Created:{" "}

                                <strong>
                                    {
                                        uploadResult.chunks_created
                                    }
                                </strong>
                            </span>


                            <span>
                                Total Indexed Chunks:{" "}

                                <strong>
                                    {
                                        uploadResult.total_chunks
                                    }
                                </strong>
                            </span>


                            <span>
                                FAISS Index:{" "}

                                <strong>
                                    Updated
                                </strong>
                            </span>

                        </div>

                    </div>

                )}


                {/* UPLOAD ERROR */}

                {error && (

                    <div className="upload-error">
                        {error}
                    </div>

                )}

            </div>


            {/* ==========================================
                KNOWLEDGE ASSISTANT
            ========================================== */}

            <div className="panel knowledge-assistant-panel">

                <div className="panel-header">

                    <div>

                        <h2>
                            Knowledge Assistant
                        </h2>

                        <p className="panel-description">

                            Ask questions about the approved
                            enterprise knowledge base. The AI
                            retrieves relevant knowledge and
                            generates a grounded response.

                        </p>

                    </div>


                    <span className="kb-status">
                        RAG Query
                    </span>

                </div>


                <div className="knowledge-query-area">

                    <textarea
                        className="knowledge-query-input"
                        placeholder="Ask a question about the knowledge base..."
                        value={question}
                        onChange={(event) => {

                            setQuestion(
                                event.target.value
                            );

                            setChatError("");

                        }}
                        onKeyDown={(event) => {

                            if (
                                event.key ===
                                    "Enter" &&
                                !event.shiftKey
                            ) {

                                event.preventDefault();

                                handleAskQuestion();
                            }

                        }}
                    />


                    <button
                        className="primary-button"
                        onClick={
                            handleAskQuestion
                        }
                        disabled={
                            !question.trim() ||
                            asking
                        }
                    >

                        {asking
                            ? "Searching Knowledge Base..."
                            : "Ask Knowledge Base"}

                    </button>

                </div>


                {/* CHAT ERROR */}

                {chatError && (

                    <div className="upload-error">

                        {chatError}

                    </div>

                )}


                {/* ANSWER */}

                {answer && (

                    <div className="knowledge-answer">

                        <div className="answer-header">

                            <h3>
                                AI Answer
                            </h3>


                            <span className="confidence-badge">

                                Confidence:{" "}

                                {
                                    (
                                        answer.confidence *
                                        100
                                    ).toFixed(0)
                                }%

                            </span>

                        </div>


                        <p className="answer-text">

                            {answer.answer}

                        </p>


                        {/* SOURCES */}

                        {answer.sources?.length >
                            0 && (

                            <div className="knowledge-sources">

                                <h3>
                                    Knowledge Sources
                                </h3>


                                {answer.sources.map(
                                    (
                                        source,
                                        index
                                    ) => (

                                        <div
                                            className="knowledge-source"
                                            key={
                                                `${source.source_file}-${index}`
                                            }
                                        >

                                            <div>

                                                <strong>

                                                    {
                                                        source.title ||
                                                        source.source_file
                                                    }

                                                </strong>


                                                <span>

                                                    {
                                                        source.source_file
                                                    }

                                                </span>

                                            </div>


                                            <span className="similarity-score">

                                                Similarity:{" "}

                                                {
                                                    source.similarity_score
                                                }

                                            </span>

                                        </div>

                                    )
                                )}

                            </div>

                        )}


                        {/* NO SOURCES */}

                        {answer.sources?.length ===
                            0 && (

                            <div className="upload-error">

                                No approved knowledge
                                source was found.
                                Please contact the IT
                                helpdesk.

                            </div>

                        )}

                    </div>

                )}

            </div>


            {/* ==========================================
                KNOWLEDGE ARTICLES
            ========================================== */}

            <div className="panel">

                <div className="panel-header">

                    <div>

                        <h2>
                            Knowledge Articles
                        </h2>

                        <p className="panel-description">

                            7 approved knowledge articles
                            available for semantic search.

                        </p>

                    </div>


                    <span className="kb-status">
                        RAG Active
                    </span>

                </div>


                <div className="knowledge-table">

                    <div className="knowledge-header">

                        <span>
                            ID
                        </span>

                        <span>
                            Article
                        </span>

                        <span>
                            Category
                        </span>

                        <span>
                            Owner
                        </span>

                        <span>
                            Priority
                        </span>

                    </div>


                    {articles.map(
                        (article) => (

                            <div
                                className="knowledge-row"
                                key={
                                    article.id
                                }
                            >

                                <strong>
                                    {article.id}
                                </strong>


                                <div>

                                    <strong>
                                        {
                                            article.title
                                        }
                                    </strong>


                                    <span className="article-subcategory">

                                        {
                                            article.subcategory
                                        }

                                    </span>

                                </div>


                                <span>
                                    {
                                        article.category
                                    }
                                </span>


                                <span>
                                    {
                                        article.owner
                                    }
                                </span>


                                <span
                                    className={`priority-badge ${article.priority.toLowerCase()}`}
                                >
                                    {
                                        article.priority
                                    }
                                </span>

                            </div>

                        )
                    )}

                </div>

            </div>


            {/* ==========================================
                RAG PIPELINE + GOVERNANCE
            ========================================== */}

            <div className="knowledge-info-grid">


                {/* RAG PIPELINE */}

                <div className="panel">

                    <h2>
                        RAG Pipeline
                    </h2>


                    <div className="pipeline">

                        <div className="pipeline-step">

                            <strong>
                                1
                            </strong>

                            <span>
                                Knowledge Documents
                            </span>

                        </div>


                        <div className="pipeline-arrow">
                            →
                        </div>


                        <div className="pipeline-step">

                            <strong>
                                2
                            </strong>

                            <span>
                                Chunking
                            </span>

                        </div>


                        <div className="pipeline-arrow">
                            →
                        </div>


                        <div className="pipeline-step">

                            <strong>
                                3
                            </strong>

                            <span>
                                Embeddings
                            </span>

                        </div>


                        <div className="pipeline-arrow">
                            →
                        </div>


                        <div className="pipeline-step">

                            <strong>
                                4
                            </strong>

                            <span>
                                FAISS Search
                            </span>

                        </div>


                        <div className="pipeline-arrow">
                            →
                        </div>


                        <div className="pipeline-step">

                            <strong>
                                5
                            </strong>

                            <span>
                                Grounded Answer
                            </span>

                        </div>

                    </div>

                </div>


                {/* AI GOVERNANCE */}

                <div className="panel">

                    <h2>
                        AI Governance
                    </h2>


                    <div className="governance-item">

                        <span className="governance-icon">
                            ✓
                        </span>

                        <div>

                            <strong>
                                Approved Sources
                            </strong>

                            <p>
                                Responses are grounded
                                in the approved
                                knowledge base.
                            </p>

                        </div>

                    </div>


                    <div className="governance-item">

                        <span className="governance-icon">
                            ✓
                        </span>

                        <div>

                            <strong>
                                Source Attribution
                            </strong>

                            <p>
                                Retrieved knowledge
                                articles are displayed
                                with AI responses.
                            </p>

                        </div>

                    </div>


                    <div className="governance-item">

                        <span className="governance-icon">
                            ✓
                        </span>

                        <div>

                            <strong>
                                Fallback
                            </strong>

                            <p>
                                Requests without
                                sufficient knowledge
                                are escalated.
                            </p>

                        </div>

                    </div>

                </div>

            </div>

        </div>
    );
}