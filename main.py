import fitz
import os
import json

def analyze_font_styles(doc):
    styles = {}
    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict", flags=4)["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        size = round(span["size"])
                        if size not in styles:
                            styles[size] = 0
                        styles[size] += len(span["text"])
    if not styles:
        return 12, []
    body_size = max(styles, key=styles.get)
    heading_styles = sorted([size for size in styles if size > body_size * 1.1], reverse=True)
    return body_size, heading_styles

def extract_headings_by_heuristic(doc):
    body_size, heading_styles = analyze_font_styles(doc)
    if not heading_styles:
        return {"title": "", "outline": []}
        
    level_map = {size: f"H{i+1}" for i, size in enumerate(heading_styles[:3])}
    
    title = ""
    outline = []
    
    title_size = heading_styles[0]
    page = doc[0]
    blocks = page.get_text("dict", flags=4)["blocks"]
    for block in blocks:
        if "lines" in block:
            for line in block["lines"]:
                if all(round(span["size"]) == title_size for span in line["spans"]):
                    line_text = "".join(span["text"] for span in line["spans"]).strip()
                    if line_text:
                        title = line_text
                        break
            if title:
                break

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict", flags=4)["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    line_text = "".join(span["text"] for span in line["spans"]).strip()
                    if not line_text or not line["spans"]:
                        continue
                    
                    line_size = round(line["spans"][0]["size"])
                    
                    if line_size in level_map and line_text != title:
                        outline.append({
                            "level": level_map[line_size],
                            "text": line_text,
                            "page": page_num + 1
                        })
                        
    return {"title": title, "outline": outline}

def extract_headings_from_toc(doc):
    toc = doc.get_toc()
    title = doc.metadata.get("title", "")
    outline = []
    
    for level, text, page in toc:
        if level <= 3:
            outline.append({
                "level": f"H{level}",
                "text": text,
                "page": page
            })
            
    return {"title": title, "outline": outline}

def process_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        if doc.get_toc():
            return extract_headings_from_toc(doc)
        else:
            return extract_headings_by_heuristic(doc)
    except Exception as e:
        print(f"Error processing {os.path.basename(file_path)}: {e}")
        return None

def main():
    INPUT_DIR = "input"
    OUTPUT_DIR = "output"

    if not os.path.exists(INPUT_DIR):
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]
    pdf_files.sort()

    if not pdf_files:
        return

    for pdf_file in pdf_files:
        print(f"--- Processing {pdf_file} ---")
        file_path = os.path.join(INPUT_DIR, pdf_file)
        result = process_pdf(file_path)
        
        if result:
            output_filename = f"{os.path.splitext(pdf_file)[0]}.json"
            output_filepath = os.path.join(OUTPUT_DIR, output_filename)
            
            with open(output_filepath, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
            
            print(f"Successfully created JSON output for: {pdf_file}")

if __name__ == "__main__":
    main()