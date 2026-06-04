import re
import ollama


class AnswerResult:

    def __init__(self, answer):
        self.answer = answer


class AnswerEngine:

    def __init__(self):
        pass

    def clean_text(self, text):

        text = text.replace("", " ")

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def answer(self, question, knowledge_base):

        greetings = [
            "hi",
            "hello",
            "hey"
        ]

        if question.lower().strip() in greetings:

            return AnswerResult(
                "Hello 👋 Upload documents and ask questions."
            )

        question_lower = question.lower()

        chunks = knowledge_base.search(question)

        if not chunks:

            return AnswerResult(
                "No relevant information found in the document."
            )

        context = "\n\n".join([
            self.clean_text(chunk.text[:1200])
            for chunk in chunks
        ])

        # ===================================
        # MODES
        # ===================================

        describe_keywords = [
            "overview",
            "explain this pdf",
            "explain this file",
            "about this pdf"
        ]

        short_summary_keywords = [
            "short summary",
            "summary",
            "summarize",
            "document summary"
        ]

        # ===================================
        # DESCRIBE MODE
        # ===================================

        if any(
            keyword in question_lower
            for keyword in describe_keywords
        ):

            prompt = f"""
You are a professional AI document analyst.

Analyze the uploaded document and provide:

1. Main topics
2. Important concepts

DO NOT provide short summary.

Use ONLY document context.

Document Context:
{context}
"""

        # ===================================
        # SUMMARY MODE
        # ===================================

        elif any(
            keyword in question_lower
            for keyword in short_summary_keywords
        ):

            prompt = f"""
You are a professional AI document analyst.

Analyze uploaded document and provide:

Short summary

Use ONLY document context.

Document Context:
{context}
"""

        # ===================================
        # NORMAL QUESTIONS
        # ===================================

        else:

            prompt = f"""
You are an intelligent AI assistant.

Answer the user's question clearly and naturally.

IMPORTANT:

- Use ONLY provided document context
- Give short and accurate answers
- Do not add unrelated information

If answer not found say:

"The answer was not found in document."

Question:
{question}

Document Context:
{context}
"""

        try:

            response = ollama.chat(
                model='llama3',
                messages=[
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            )

            answer = response[
                'message'
            ]['content']

            answer = self.clean_text(answer)

            # ==========================
            # REMOVE MARKDOWN SYMBOLS
            # ==========================

            answer = answer.replace("**", "")
            answer = answer.replace("__", "")
            answer = answer.replace("###", "")
            answer = answer.replace("##", "")
            answer = answer.replace("#", "")

            # ==========================
            # FORMAT FIXES
            # ==========================

            answer = answer.replace(
                "• ",
                "\n• "
            )

            answer = answer.replace(
                "✓ ",
                "\n✓ "
            )

            for i in range(1,30):

                answer = answer.replace(
                    f"{i}. ",
                    f"\n{i}. "
                )

            section_titles = [

                "Main Topics:",
                "Important Concepts:",
                "Short Summary:",
                "Summary:",
                "Overview:"
            ]

            for title in section_titles:

                answer = answer.replace(
                    title,
                    f"\n\n{title}\n"
                )

            answer = re.sub(
                r"\n{3,}",
                "\n\n",
                answer
            )

            answer = answer.strip()

            return AnswerResult(
                answer
            )

        except Exception as e:

            return AnswerResult(
                f"Error: {str(e)}"
            )