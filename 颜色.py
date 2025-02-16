from PIL import Image, ImageDraw
import colorsys
import json

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#f6cec1')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def get_complementary_color(rgb):
    # 计算反色
    return tuple(255 - c for c in rgb)

def generate_palette_image(hex_color, output_path, json_output_path):
    # 转换颜色空间
    r, g, b = hex_to_rgb(hex_color)
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    h_deg = round(h * 360, 2)
    s_percent = round(s * 100, 2)
    base_l = round(l * 100, 2)

    # 生成5个调色板（主色+4个衍生色调）
    palettes_h = [
        h_deg,                        # 主色调
        (h_deg + 30) % 360,           # 类似色+30
        (h_deg - 30) % 360,           # 类似色-30
        (h_deg + 150) % 360,          # 补色+30
        (h_deg - 150) % 360           # 补色-30
    ]

    # 生成13级亮度阶梯（从亮到暗）
    lightness_levels = [round(98 - (i * 7.5), 2) for i in range(13)]

    # 生成所有颜色
    all_colors = []
    for palette_h in palettes_h:
        palette_colors = []
        for l in lightness_levels:
            # 动态调整饱和度（中间亮度时饱和度最高）
            dynamic_s = s_percent * (0.3 + 0.7 * (1 - abs(50 - l)/50))
            
            # 转换回RGB
            h_norm = palette_h / 360
            s_norm = max(0, min(100, dynamic_s)) / 100
            l_norm = max(0, min(100, l)) / 100
            
            r, g, b = colorsys.hls_to_rgb(h_norm, l_norm, s_norm)
            rgb = tuple(int(round(c * 255)) for c in (r, g, b))
            palette_colors.append(rgb)
        all_colors.append(palette_colors)

    # 创建图像
    img = Image.new('RGB', (500, 1300))
    draw = ImageDraw.Draw(img)

    # 绘制色块
    for palette_idx in range(5):
        for color_idx in range(13):
            x0 = palette_idx * 100
            y0 = color_idx * 100
            draw.rectangle(
                [(x0, y0), (x0 + 100, y0 + 100)],
                fill=all_colors[palette_idx][color_idx]
            )

    img.save(output_path, 'JPEG', quality=95)

    # 生成颜色信息并保存为JSON
    color_info = []
    for palette_idx in range(5):
        palette_colors = []
        for color_idx in range(13):
            rgb = all_colors[palette_idx][color_idx]
            hex_color = rgb_to_hex(rgb)
            complementary_rgb = get_complementary_color(rgb)
            complementary_hex = rgb_to_hex(complementary_rgb)
            palette_colors.append({
                'rgb': rgb,
                'hex': hex_color,
                'complementary_rgb': complementary_rgb,
                'complementary_hex': complementary_hex
            })
        color_info.append(palette_colors)

    with open(json_output_path, 'w') as f:
        json.dump(color_info, f, indent=4)

# 使用示例
generate_palette_image('#6750A4', 'material_you_palette.jpg', 'material_you_palette.json')