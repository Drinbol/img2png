#!/usr/bin/env python3
"""
img2png — 图片批量转 PNG

将目录中的图片统一转换为 PNG 并输出到指定目录。
支持 jpg / jpeg / webp / gif / bmp / tiff / ico 等格式。
注意：即使后缀名是 .png，实际内容也可能是 webp 等格式（按文件头识别，不按扩展名）。

用法：
    python main.py 输入目录 [-o 输出目录] [-r]
"""

import argparse
import sys
from pathlib import Path

from PIL import Image

# PIL 可读取的常见图片格式
IMAGE_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp',
    '.tiff', '.tif', '.ico', '.ppm', '.pgm', '.pbm',
}


def convert_images(input_dir: str, output_dir: str | None = None, recursive: bool = False) -> None:
    """将目录中的图片转换为 PNG 格式"""
    input_path = Path(input_dir).resolve()
    if not input_path.is_dir():
        print(f"错误: 目录不存在或不是目录: {input_path}")
        sys.exit(1)

    # 默认输出目录为 <输入目录>/Output
    output_path = Path(output_dir).resolve() if output_dir else input_path / "Output"
    output_path.mkdir(parents=True, exist_ok=True)

    files = input_path.rglob("*") if recursive else input_path.iterdir()

    converted = 0
    failed = 0

    print(f"扫描目录: {input_path}{'（含子目录）' if recursive else ''}")
    print(f"输出目录: {output_path}")
    print("-" * 50)

    for file_path in sorted(files):
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        # 跳过输出目录里的文件，避免递归时自我复制
        if output_path in file_path.parents:
            continue

        output_file = output_path / f"{file_path.stem}.png"

        try:
            # PIL 按文件头识别真实格式，不依赖扩展名
            with Image.open(file_path) as img:
                # RGBA / 调色板 / 灰度+透明 统一转成 RGBA 保留透明通道
                if img.mode in ('RGBA', 'P', 'LA'):
                    img = img.convert('RGBA')
                else:
                    img = img.convert('RGB')
                img.save(output_file, 'PNG')

            print(f"✓ {file_path.name} -> {output_file.name}")
            converted += 1

        except Exception as e:
            print(f"✗ {file_path.name} 转换失败: {e}")
            failed += 1

    print("-" * 50)
    print(f"转换完成: {converted} 个成功, {failed} 个失败")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="图片批量转 PNG：按文件头识别真实格式，统一转为 PNG 输出"
    )
    parser.add_argument("input", help="输入目录")
    parser.add_argument("-o", "--output", default=None, help="输出目录（默认 <输入目录>/Output）")
    parser.add_argument("-r", "--recursive", action="store_true", help="递归处理子目录")
    args = parser.parse_args()

    convert_images(args.input, args.output, args.recursive)


if __name__ == "__main__":
    main()
