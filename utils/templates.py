"""
Resume Templates Module
Provides different resume templates/styles
"""

TEMPLATES = {
    "professional": {
        "name": "Professional",
        "description": "Clean, traditional format ideal for corporate roles",
        "colors": {
            "primary": "#2c3e50",
            "secondary": "#3498db",
            "text": "#000000",
            "background": "#ffffff"
        },
        "fonts": {
            "header": "Arial, Helvetica, sans-serif",
            "body": "Arial, Helvetica, sans-serif",
            "size_header": "24pt",
            "size_body": "11pt"
        },
        "layout": "single_column"
    },
    "modern": {
        "name": "Modern",
        "description": "Contemporary design with accent colors",
        "colors": {
            "primary": "#1a1a1a",
            "secondary": "#667eea",
            "text": "#000000",
            "background": "#ffffff"
        },
        "fonts": {
            "header": "Helvetica, Arial, sans-serif",
            "body": "Helvetica, Arial, sans-serif",
            "size_header": "26pt",
            "size_body": "10.5pt"
        },
        "layout": "single_column"
    },
    "creative": {
        "name": "Creative",
        "description": "Bold design for creative industries",
        "colors": {
            "primary": "#2d3748",
            "secondary": "#ed8936",
            "text": "#000000",
            "background": "#ffffff"
        },
        "fonts": {
            "header": "Georgia, serif",
            "body": "Arial, sans-serif",
            "size_header": "28pt",
            "size_body": "11pt"
        },
        "layout": "single_column"
    },
    "minimal": {
        "name": "Minimal",
        "description": "Simple, elegant design focusing on content",
        "colors": {
            "primary": "#000000",
            "secondary": "#4a5568",
            "text": "#000000",
            "background": "#ffffff"
        },
        "fonts": {
            "header": "Arial, sans-serif",
            "body": "Arial, sans-serif",
            "size_header": "22pt",
            "size_body": "10pt"
        },
        "layout": "single_column"
    }
}

def get_template(template_name: str = "professional"):
    """Get template configuration by name"""
    return TEMPLATES.get(template_name, TEMPLATES["professional"])

def get_all_templates():
    """Get all available templates"""
    return TEMPLATES

def apply_template_to_html(html: str, template_name: str = "professional"):
    """Apply template styling to resume HTML"""
    template = get_template(template_name)
    
    # Replace color placeholders
    html = html.replace("#2c3e50", template["colors"]["primary"])
    html = html.replace("#3498db", template["colors"]["secondary"])
    html = html.replace("#000", template["colors"]["text"])
    html = html.replace("white", template["colors"]["background"])
    
    # Replace font placeholders
    html = html.replace("'Arial', 'Helvetica', sans-serif", template["fonts"]["header"])
    html = html.replace("11pt", template["fonts"]["size_body"])
    html = html.replace("24pt", template["fonts"]["size_header"])
    
    return html
