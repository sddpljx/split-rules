#!/usr/bin/env python3
"""
将 meta-rules-dat 的域名列表转换为 Surge 规则格式

转换规则：
- 普通域名（如 apple.com.akadns.net）→ DOMAIN,apple.com.akadns.net
- 带+号的域名（如 +.apple.de）→ DOMAIN-SUFFIX,apple.de
- 忽略空行和注释行（以 # 开头）
"""

import sys
from pathlib import Path


def convert_line(line: str) -> str:
    """
    转换单行域名规则

    Args:
        line: 原始域名规则

    Returns:
        转换后的 Surge 规则，如果是空行或注释则返回空字符串
    """
    line = line.strip()

    # 跳过空行和注释
    if not line or line.startswith('#'):
        return ''

    # 处理 +. 开头的域名（域名后缀匹配）
    if line.startswith('+.'):
        domain = line[2:]  # 去掉 +.
        return f'DOMAIN-SUFFIX,{domain}'

    # 处理普通域名（完整域名匹配）
    return f'DOMAIN,{line}'


def convert_file(input_path: Path, output_path: Path) -> None:
    """
    转换整个文件

    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        converted_lines = []
        for line in lines:
            converted = convert_line(line)
            if converted:  # 只添加非空行
                converted_lines.append(converted)

        # 创建输出目录
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 写入转换后的内容
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(converted_lines))
            if converted_lines:  # 如果有内容，末尾添加换行符
                f.write('\n')

        print(f'✓ 已转换: {input_path.name} -> {output_path.name} ({len(converted_lines)} 条规则)')

    except Exception as e:
        print(f'✗ 转换失败 {input_path.name}: {e}', file=sys.stderr)
        raise


def main():
    """主函数：批量转换所有 .list 文件"""
    # 设置路径
    source_dir = Path('meta-rules-dat/geo/geosite')
    output_dir = Path('rules/geo/geosite')

    if not source_dir.exists():
        print(f'错误: 源目录不存在: {source_dir}', file=sys.stderr)
        sys.exit(1)

    # 获取所有 .list 文件
    list_files = sorted(source_dir.glob('*.list'))

    if not list_files:
        print(f'警告: 在 {source_dir} 中未找到 .list 文件', file=sys.stderr)
        sys.exit(0)

    print(f'找到 {len(list_files)} 个 .list 文件')
    print('=' * 60)

    # 转换所有文件
    success_count = 0
    for list_file in list_files:
        # 输出文件名保持一致，但放在 rules 目录下
        output_file = output_dir / list_file.name

        try:
            convert_file(list_file, output_file)
            success_count += 1
        except Exception:
            continue

    print('=' * 60)
    print(f'转换完成: {success_count}/{len(list_files)} 个文件成功')

    if success_count < len(list_files):
        sys.exit(1)


if __name__ == '__main__':
    main()
