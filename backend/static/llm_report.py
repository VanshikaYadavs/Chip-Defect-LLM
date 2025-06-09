
# llm_report.py

def generate_llm_report(defect_classes):
    """
    Generates a structured and non-redundant LLM report for detected chip defects.
    Includes explanation, possible causes, and prevention tips.
    """
    if not defect_classes:
        return "✅ No defects were detected in the chip. Everything looks fine!"

    response = "⚠️ Detected defects with explanations, causes, and prevention:\n\n"

    # Remove duplicates while preserving order
    seen = set()
    unique_defects = []
    for defect in defect_classes:
        if defect not in seen:
            unique_defects.append(defect)
            seen.add(defect)

    # Dictionary of details for known defect types
    defect_details = {
        "MouseBite": {
            "explanation": "MouseBite refers to small, unintended perforations or holes on the PCB edge, often from panel break-off.",
            "causes": [
                "Improper depanelization process (manual snapping or incorrect V-grooves)",
                "Weak material near the board edges",
                "Incorrect tooling setup"
            ],
            "prevention": [
                "Use routing or scoring methods correctly during panelization",
                "Ensure mechanical fixtures are properly aligned",
                "Add proper break-away tabs with optimized hole patterns"
            ]
        },
        "Missing_Hole": {
            "explanation": "A Missing Hole means a drill hole required for component leads or vias is absent.",
            "causes": [
                "Errors in the drilling file (Excellon format issues)",
                "Drilling machine malfunction or skipped operation",
                "Incorrect data transfer to the fabrication unit"
            ],
            "prevention": [
                "Verify drill files before manufacturing",
                "Perform optical or X-ray inspection post-drilling",
                "Automate DFM (Design for Manufacturing) checks"
            ]
        },
        "Open_Circuit": {
            "explanation": "An Open Circuit occurs when a track or trace is physically or electrically broken, leading to interrupted current flow.",
            "causes": [
                "Over-etching during PCB etching",
                "Cracks in traces due to flexing or stress",
                "Manufacturing defects in multilayer boards"
            ],
            "prevention": [
                "Use proper etching techniques",
                "Apply protective coatings to traces",
                "Avoid excessive bending of the PCB"
            ]
        },
        "Short_Circuit": {
            "explanation": "A Short Circuit is when unintended electrical connection occurs between two points, risking damage.",
            "causes": [
                "Bridging of solder between adjacent pads",
                "Spurious copper or residual etching",
                "Component placement errors"
            ],
            "prevention": [
                "Improve solder mask application and spacing",
                "Use AOI (Automated Optical Inspection) after soldering",
                "Maintain clean and dust-free environments"
            ]
        },
        "Spur": {
            "explanation": "Spurs are tiny, unintended protrusions of copper from a trace that can lead to shorts or signal issues.",
            "causes": [
                "Over-etching or undercutting during the etching process",
                "Contaminated copper laminate surface",
                "Improper photolithography process"
            ],
            "prevention": [
                "Use clean room environments for photolithography",
                "Optimize etching process parameters",
                "Inspect copper surfaces pre- and post-etching"
            ]
        },
        "Spurious_Cooper": {
            "explanation": "Spurious Copper refers to leftover unwanted copper that was not properly etched off.",
            "causes": [
                "Incomplete etching during PCB fabrication",
                "Contamination on photoresist layers",
                "Low-quality copper foil"
            ],
            "prevention": [
                "Ensure clean etching chemicals and proper flow rate",
                "Double-check artwork and photoresist alignment",
                "Perform post-etch inspection to catch residues"
            ]
        }
    }

    for defect in unique_defects:
        details = defect_details.get(defect)
        if details:
            response += f"---\n\n### 🛠️ {defect}\n"
            response += f"**What it is:** {details['explanation']}\n\n"
            response += "**Possible Causes:**\n"
            for cause in details['causes']:
                response += f"- {cause}\n"
            response += "\n**Prevention Tips:**\n"
            for tip in details['prevention']:
                response += f"- {tip}\n"
            response += "\n"
        else:
            response += f"- **{defect}**: No explanation available.\n\n"

    return response
