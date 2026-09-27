import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are a document intelligence assistant.
Answer ONLY using the supplied document context.
Do not use outside knowledge or invent facts.
If the context is insufficient, clearly say that the information was not found.
Keep answers concise."""

def generate_answer(question, results):
    context = "\n\n".join(
        f"[Document: {r['metadata']['source']} | Page: {r['metadata']['page']}]\n{r['text']}"
        for r in results
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"CONTEXT:\n{context}\n\nQUESTION:\n{question}"}
        ]
    )
    sources, seen = [], set()
    for r in results:
        s = {"document": r["metadata"]["source"], "page": r["metadata"]["page"]}
        key = (s["document"], s["page"])
        if key not in seen:
            sources.append(s)
            seen.add(key)
    return {"answer": response.choices[0].message.content, "sources": sources}
