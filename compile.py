from jinja2 import Environment, FileSystemLoader
import json

def generate_static_html(template_name, output_path, **context):
    # 设置模板加载器
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    
    # 加载模板
    template = env.get_template(template_name)
    
    # 渲染模板
    rendered_html = template.render(**context)
    
    # 将渲染结果保存为静态 HTML 文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered_html)

def main():
    with open('nav_items.json', 'r', encoding='utf-8') as f:
        nav_items = json.load(f)
    
    generate_static_html('index.html', 'static/index.html', nav_items=nav_items)
    print('index.html generated successfully')

if __name__ == "__main__":
    main()