# img2png

图片批量转 PNG 工具。按**文件头**识别真实格式（不信任扩展名），统一转换为 PNG 输出。

## 特点

- 支持 jpg / jpeg / webp / gif / bmp / tiff / ico 等常见格式
- 后缀名是假的也能识别（例如 `.png` 实际是 webp）
- 自动保留透明通道（RGBA / 调色板 / LA 统一转 RGBA）
- 可选递归处理子目录

## 安装

```bash
uv sync        # Python 3.12+，依赖：pillow
```

## 使用

```bash
# 转换目录，输出到 <输入目录>/Output
uv run python main.py /path/to/images

# 指定输出目录
uv run python main.py /path/to/images -o /path/to/out

# 递归处理子目录
uv run python main.py /path/to/images -r
```

## 输出

- 文件名不变，扩展名统一为 `.png`
- 已存在于输出目录中的文件不会被重复处理（递归时自动跳过输出目录）

## 许可证

MIT
