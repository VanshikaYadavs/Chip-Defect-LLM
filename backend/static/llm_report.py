import requests

def query_llama(prompt):
    """
    Send a prompt to the local LLaMA model via Ollama.
    """
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"⚠️ LLaMA API error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"⚠️ Error connecting to LLaMA: {str(e)}"

def generate_llm_report(defect_classes):
    """
    Generate a professional LLM-based report from unique defect types.
    """
    if not defect_classes:
        return "✅ No defects were detected in the chip. Everything looks fine!"

    # Remove duplicate defects
    unique_defects = list(set(defect_classes))

    # Construct a structured prompt for LLaMA
    prompt = (
        "You are a senior PCB defect analysis engineer. For each of the following chip defect types, "
        "provide:\n"
        "1. What it is (short technical definition)\n"
        "2. Major causes (3-4 bullet points)\n"
        "3. Prevention tips (3-4 bullet points)\n\n"
    )
    for defect in unique_defects:
        prompt += f"- {defect}\n"

    print("🧠 Sending prompt to LLaMA...\n")
    llm_response = query_llama(prompt)

    return f"⚠️ Detected defects with detailed insights:\n\n{llm_response}"

import matplotlib.pyplot as plt
from collections import Counter
import os

def generate_defect_chart(defects, output_path="backend/static/chart.png"):
    """
    Generates a bar chart showing frequency of each defect class.
    Saves the chart as an image file.
    """
    if not defects:
        return None

    counts = Counter(defects)
    classes = list(counts.keys())
    values = list(counts.values())

    plt.figure(figsize=(6, 4))
    bars = plt.bar(classes, values, color='tomato')
    plt.title("Detected Chip Defects")
    plt.xlabel("Defect Type")
    plt.ylabel("Count")
    plt.xticks(rotation=20)
    plt.tight_layout()

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, int(yval), ha='center', va='bottom')

    # Save chart
    plt.savefig(output_path)
    plt.close()

    return output_path
