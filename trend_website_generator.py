import os
import re
import json
import argparse
from pathlib import Path
from collections import Counter, defaultdict

def analyze_css(css_content):
    colors = re.findall(r'#[0-9a-fA-F]{3,8}', css_content)
    gradients = re.findall(r'linear-gradient\s*\([^)]*\)', css_content, re.I)
    fonts = re.findall(r'font-family\s*[:\(]?\s*["\']?([^";\')]+)["\']?', css_content, re.I)
    transparency = len(re.findall(r'rgba\s*\([^)]*\)', css_content, re.I))
    blur = len(re.findall(r'backdrop-filter\s*:\s*blur|filter\s*:\s*blur', css_content, re.I))
    transforms = len(re.findall(r'transform\s*:', css_content, re.I))
    return {
        'colors': colors,
        'gradients': gradients,
        'fonts': fonts,
        'transparency': transparency,
        'blur': blur,
        'transforms': transforms
    }

def analyze_html(html_content):
    classes = re.findall(r'class\s*=\s*["\']([^"\']*)["\']', html_content, re.I)
    ids = re.findall(r'id\s*=\s*["\']([^"\']*)["\']', html_content, re.I)
    ai_related = len(re.findall(r'\b(ai|neural|circuit|data|brain|robot|smart|intelligent|futuristic|tech)\b', html_content, re.I))
    flat_classes = []
    for cls in classes:
        flat_classes.extend(cls.split())
    return {
        'classes': flat_classes,
        'ids': ids,
        'ai_related_count': ai_related
    }

def analyze_website(input_dir):
    input_path = Path(input_dir)
    all_css = ''
    all_html = ''
    css_files = list(input_path.rglob('*.css')) + list(input_path.rglob('*.scss'))
    html_files = list(input_path.rglob('*.html')) + list(input_path.rglob('*.htm'))

    for css_file in css_files:
        try:
            with open(css_file, 'r', encoding='utf-8', errors='ignore') as f:
                all_css += f.read() + '\n'
        except:
            pass

    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                all_html += f.read() + '\n'
        except:
            pass

    css_analysis = analyze_css(all_css)
    html_analysis = analyze_html(all_html)

    # Determine dominant colors
    color_counts = Counter(css_analysis['colors'])
    dominant_colors = [color for color, _ in color_counts.most_common(5)] if color_counts else ['#000000', '#ffffff']

    # Determine if it follows AI trends
    ai_trend_score = 0
    if any('#000000' in c or '#111111' in c or '#222222' in c for c in dominant_colors):
        ai_trend_score += 2
    if any('linear-gradient' in g and ('#0066ff' in g or '#6600ff' in g or '#0099ff' in g) for g in css_analysis['gradients']):
        ai_trend_score += 2
    if any(font in str(css_analysis['fonts']) for font in ['Orbitron', 'Exo', 'Russo One', 'Eurostile']):
        ai_trend_score += 2
    if html_analysis['ai_related_count'] > 3:
        ai_trend_score += 2
    if css_analysis['transparency'] > 5:
        ai_trend_score += 1
    if css_analysis['blur'] > 2:
        ai_trend_score += 1
    if css_analysis['transforms'] > 10:
        ai_trend_score += 1

    follows_ai_trend = ai_trend_score >= 4

    return {
        'dominant_colors': dominant_colors[:3] if len(dominant_colors) >= 3 else dominant_colors + ['#ffffff'] * (3 - len(dominant_colors)),
        'gradients': css_analysis['gradients'][:2] if css_analysis['gradients'] else ['linear-gradient(135deg, #0066ff 0%, #6600ff 100%)'],
        'fonts': list(set(css_analysis['fonts']))[:2] if css_analysis['fonts'] => ['Orbitron', 'sans-serif'],
        'follows_ai_trend': follows_ai_trend,
        'ai_trend_score': ai_trend_score,
        'transparency': css_analysis['transparency'],
        'blur': css_analysis['blur'],
        'transforms': css_analysis['transforms'],
        'common_classes': [item for item, _ in Counter(html_analysis['classes']).most_common(5)] if html_analysis['classes'] => ['container'],
        'common_ids': html_analysis['ids'][:3] if html_analysis['ids'] => ['header', 'content', 'footer']
    }

def generate_website(trends, output_dir):
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Generate HTML
    html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Immersive AI Trend Experience</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="scroll-container">
        <section class="slide" id="slide1">
            <div class="slide-content">
                <h1>AI Trends Immersion</h1>
                <p>Exploring the visual language of artificial intelligence</p>
            </div>
            <div class="slide-object" id="object1">
                <div class="object-content">
                    <h2>Neural Networks</h2>
                    <p>Interconnected nodes forming intelligent patterns</p>
                </div>
            </div>
        </section>
        <section class="slide" id="slide2">
            <div class="slide-content">
                <h2>Data Flows</h2>
                <p>Information moving through intelligent systems</p>
            </div>
            <div class="slide-object" id="object2">
                <div class="object-content">
                    <h2>Pattern Recognition</h2>
                    <p>Finding order in complex information</p>
                </div>
            </div>
        </section>
        <section class="slide" id="slide3">
            <div class="slide-content">
                <h2>Learning Algorithms</h2>
                <p>Systems that improve through experience</p>
            </div>
            <div class="slide-object" id="object3">
                <div class="object-content">
                    <h2>Adaptive Intelligence</h2>
                    <p>Evolving responses to new challenges</p>
                </div>
            </div>
        </section>
    </div>
    <script src="script.js"></script>
</body>
</html>'''

    # Generate CSS
    primary_color = trends['dominant_colors'][0] if trends['dominant_colors'] else '#000000'
    secondary_color = trends['dominant_colors'][1] if len(trends['dominant_colors']) > 1 else '#6600ff'
    accent_color = trends['dominant_colors'][2] if len(trends['dominant_colors']) > 2 else '#0066ff'
    font_primary = trends['fonts'][0] if trends['fonts'] else 'Orbitron'
    font_secondary = trends['fonts'][1] if len(trends['fonts']) > 1 else 'sans-serif'

    css_template = f'''/* AI Trend Generated Website */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: '{font_primary}', {font_secondary};
    overflow: hidden;
    height: 100vh;
    background: {primary_color};
    color: white;
}}

.scroll-container {{
    height: 100vh;
    overflow-y: scroll;
    scroll-snap-type: y mandatory;
    scroll-behavior: smooth;
    display: flex;
    flex-direction: column;
}}

.slide {{
    height: 100vh;
    width: 100vw;
    scroll-snap-align: start;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    padding: 0 5rem;
}}

.slide-content {{
    text-align: center;
    max-width: 600px;
    z-index: 2;
}}

.slide-content h1 {{
    font-size: 4rem;
    margin-bottom: 1rem;
    background: linear-gradient(to right, {primary_color}, {secondary_color});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.slide-content h2 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color: {accent_color};
}}

.slide-content p {{
    font-size: 1.2rem;
    line-height: 1.6;
    opacity: 0.9;
}}

.slide-object {{
    position: absolute;
    width: 300px;
    height: 300px;
    border-radius: 20px;
    background: {secondary_color};
    opacity: 0.8;
    backdrop-filter: blur(10px);
    border: 2px solid {accent_color};
    box-shadow: 0 0 30px rgba(0, 102, 255, 0.3);
    transition: all 0.5s ease;
    z-index: 1;
}}

.slide-object:hover {{
    transform: scale(1.1);
    box-shadow: 0 0 50px rgba(0, 102, 255, 0.5);
}}

.object-content {{
    text-align: center;
    padding: 20px;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

.object-content h2 {{
    color: white;
    margin-bottom: 10px;
}}

.object-content p {{
    color: rgba(255, 255, 255, 0.8);
    font-size: 1rem;
}}

#slide1 {{ background: {primary_color}; }}
#slide2 {{ background: linear-gradient(180deg, {primary_color} 0%, {secondary_color} 100%); }}
#slide3 {{ background: {secondary_color}; }}

#object1 {{ left: 10%; bottom: 20%; }}
#object2 {{ left: 50%; bottom: 10%; transform: translateX(-50%); }}
#object3 {{ right: 10%; bottom: 20%; }}

@media (max-width: 768px) {{
    .slide-content {{
        padding: 0 2rem;
    }}
    .slide-object {{
        width: 200px;
        height: 200px;
    }}
    #object1 {{ left: 5%; }}
    #object3 {{ right: 5%; }}
}}'''

    # Generate JS
    js_template = '''// Scroll-triggered animations
document.addEventListener('DOMContentLoaded', function() {
    const slides = document.querySelectorAll('.slide');
    const objects = document.querySelectorAll('.slide-object');

    // Initialize scroll position
    let lastScrollTop = 0;

    // Scroll event listener
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const scrollDirection = scrollTop > lastScrollTop ? 'down' : 'up';
        lastScrollTop = scrollTop;

        // Animate objects based on scroll
        objects.forEach((obj, index) => {
            const slideTop = obj.offsetTop;
            const slideHeight = obj.offsetHeight;
            const windowHeight = window.innerHeight;
            const scrollCenter = scrollTop + (windowHeight / 2);

            // Calculate distance from center
            const distanceFromCenter = Math.abs(scrollCenter - (slideTop + slideHeight / 2));
            const maxDistance = windowHeight;
            const opacity = Math.max(0.3, 1 - (distanceFromCenter / maxDistance));
            const scale = 0.8 + (opacity * 0.2);

            obj.style.opacity = opacity;
            obj.style.transform = `scale(${scale})`;
        });
    });

    // Add hover effects to objects
    objects.forEach(obj => {
        obj.addEventListener('mouseenter', () => {
            obj.style.transform = 'scale(1.1)';
            obj.style.boxShadow = '0 0 40px rgba(0, 102, 255, 0.7)';
        });

        obj.addEventListener('mouseleave', () => {
            // Reset to scroll-based transform
        });
    });

    // Improve scroll behavior for touch devices
    if ('ontouchstart' in window) {
        document.documentElement.style.scrollBehavior = 'auto';
    }
});'''

    # Write files
    try:
        with open(output_path / 'index.html', 'w', encoding='utf-8') as f:
            f.write(html_template)
        with open(output_path / 'style.css', 'w', encoding='utf-8') as f:
            f.write(css_template)
        with open(output_path / 'script.js', 'w', encoding='utf-8') as f:
            f.write(js_template)
        return True
    except Exception as e:
        print(f"Error writing files: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Analyze AI trends in websites and generate immersive experiences')
    parser.add_argument('--input', '-i', required=True, help='Input directory containing vibecoded website')
    parser.add_argument('--output', '-o', required=True, help='Output directory for generated website')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input directory '{args.input}' does not exist")
        return 1

    print("Analyzing website for AI trends...")
    trends = analyze_website(args.input)

    print(f"Analysis complete:")
    print(f"  Dominant colors: {', '.join(trends['dominant_colors'])}")
    print(f"  Gradients detected: {len(trends['gradients'])}")
    print(f"  Fonts: {', '.join(trends['fonts'])}")
    print(f"  Follows AI trend: {trends['follows_ai_trend']} (score: {trends['ai_trend_score']}/10)")
    print(f"  Transparency usage: {trends['transparency']}")
    print(f"  Blur usage: {trends['blur']}")
    print(f"  Transform usage: {trends['transforms']}")

    print("\nGenerating immersive website...")
    if generate_website(trends, args.output):
        print(f"Success! Generated website saved to: {args.output}")
        print("Open index.html in your browser to experience the immersive website.")
        return 0
    else:
        print("Error: Failed to generate website")
        return 1

if __name__ == '__main__':
    exit(main())