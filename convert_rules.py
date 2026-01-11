#!/usr/bin/env python3
"""
将 meta-rules-dat 的域名和 IP 列表转换为 Surge 规则格式

转换规则：
域名规则：
- 普通域名（如 apple.com.akadns.net）→ DOMAIN,apple.com.akadns.net
- 带+号的域名（如 +.apple.de）→ DOMAIN-SUFFIX,apple.de

IP 规则：
- IPv4 CIDR（如 1.1.1.0/24）→ IP-CIDR,1.1.1.0/24
- IPv6 CIDR（如 2001:db8::/32）→ IP-CIDR6,2001:db8::/32

- 忽略空行和注释行（以 # 开头）
"""

import sys
from pathlib import Path


def is_ipv6(line: str) -> bool:
    """
    判断是否为 IPv6 地址

    Args:
        line: 待判断的行

    Returns:
        如果包含冒号则判定为 IPv6
    """
    return ':' in line


def convert_domain_line(line: str) -> str:
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


def convert_ip_line(line: str) -> str:
    """
    转换单行 IP 规则

    Args:
        line: 原始 IP 规则（CIDR 格式）

    Returns:
        转换后的 Surge 规则，如果是空行或注释则返回空字符串
    """
    line = line.strip()

    # 跳过空行和注释
    if not line or line.startswith('#'):
        return ''

    # 判断 IPv4 还是 IPv6
    if is_ipv6(line):
        return f'IP-CIDR6,{line}'
    else:
        return f'IP-CIDR,{line}'


def convert_domain_file(input_path: Path, output_path: Path) -> int:
    """
    转换域名规则文件

    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径

    Returns:
        转换的规则数量
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        converted_lines = []
        for line in lines:
            converted = convert_domain_line(line)
            if converted:  # 只添加非空行
                converted_lines.append(converted)

        # 创建输出目录
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 写入转换后的内容
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(converted_lines))
            if converted_lines:  # 如果有内容，末尾添加换行符
                f.write('\n')

        return len(converted_lines)

    except Exception as e:
        print(f'✗ 转换域名规则失败 {input_path.name}: {e}', file=sys.stderr)
        raise


def convert_ip_file(input_path: Path, output_path: Path) -> int:
    """
    转换 IP 规则文件

    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径

    Returns:
        转换的规则数量
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        converted_lines = []
        for line in lines:
            converted = convert_ip_line(line)
            if converted:  # 只添加非空行
                converted_lines.append(converted)

        if not converted_lines:
            return 0

        # 创建输出目录
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 写入转换后的内容
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(converted_lines))
            if converted_lines:  # 如果有内容，末尾添加换行符
                f.write('\n')

        return len(converted_lines)

    except Exception as e:
        print(f'✗ 转换 IP 规则失败 {input_path.name}: {e}', file=sys.stderr)
        raise


def append_ip_rules(ip_file_path: Path, output_path: Path) -> int:
    """
    将 IP 规则追加到现有的域名规则文件末尾

    Args:
        ip_file_path: IP 规则文件路径
        output_path: 要追加到的输出文件路径

    Returns:
        追加的 IP 规则数量
    """
    try:
        with open(ip_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        converted_lines = []
        for line in lines:
            converted = convert_ip_line(line)
            if converted:  # 只添加非空行
                converted_lines.append(converted)

        if not converted_lines:
            return 0

        # 追加到现有文件
        with open(output_path, 'a', encoding='utf-8') as f:
            f.write('\n'.join(converted_lines))
            f.write('\n')

        return len(converted_lines)

    except Exception as e:
        print(f'✗ 追加 IP 规则失败 {ip_file_path.name}: {e}', file=sys.stderr)
        return 0


def main():
    """主函数：批量转换所有域名和 IP 规则文件"""
    # 设置路径
    domain_source_dir = Path('meta-rules-dat/geo/geosite')
    ip_source_dir = Path('meta-rules-dat/geo-lite/geoip')
    domain_output_dir = Path('rules/geo/geosite')
    ip_output_dir = Path('rules/geo/geoip')

    # 检查域名规则目录
    if not domain_source_dir.exists():
        print(f'错误: 域名规则源目录不存在: {domain_source_dir}', file=sys.stderr)
        sys.exit(1)

    # 获取所有域名 .list 文件
    domain_files = sorted(domain_source_dir.glob('*.list'))

    if not domain_files:
        print(f'警告: 在 {domain_source_dir} 中未找到 .list 文件', file=sys.stderr)
        sys.exit(0)

    print(f'找到 {len(domain_files)} 个域名规则文件')
    print('=' * 60)

    # 第一步：转换所有域名规则文件
    success_count = 0
    domain_file_names = {}  # 记录已转换的文件名

    for domain_file in domain_files:
        output_file = domain_output_dir / domain_file.name
        domain_file_names[domain_file.stem] = output_file  # 记录文件名（不含扩展名）

        try:
            rule_count = convert_domain_file(domain_file, output_file)
            print(f'✓ 域名规则: {domain_file.name} ({rule_count} 条)')
            success_count += 1
        except Exception:
            continue

    print('=' * 60)
    print(f'域名规则转换完成: {success_count}/{len(domain_files)} 个文件')

    # 第二步：处理 IP 规则
    if not ip_source_dir.exists():
        print(f'\n提示: IP 规则目录不存在: {ip_source_dir}')
        print('跳过 IP 规则处理')
        if success_count < len(domain_files):
            sys.exit(1)
        return

    ip_files = sorted(ip_source_dir.glob('*.list'))

    if not ip_files:
        print(f'\n提示: 在 {ip_source_dir} 中未找到 IP 规则文件')
        print('跳过 IP 规则处理')
        if success_count < len(domain_files):
            sys.exit(1)
        return

    print(f'\n找到 {len(ip_files)} 个 IP 规则文件')
    print('=' * 60)

    appended_count = 0  # 追加到域名规则文件的数量
    standalone_count = 0  # 单独保存的数量
    total_ip_rules = 0  # IP 规则总数

    for ip_file in ip_files:
        file_stem = ip_file.stem  # 文件名（不含扩展名）

        # 检查是否有同名的域名规则文件
        if file_stem in domain_file_names:
            # 追加到同名域名规则文件
            output_file = domain_file_names[file_stem]
            ip_count = append_ip_rules(ip_file, output_file)

            if ip_count > 0:
                print(f'✓ 追加 IP 规则: {ip_file.name} → geosite/{output_file.name} ({ip_count} 条)')
                appended_count += 1
                total_ip_rules += ip_count
        else:
            # 单独保存到 geoip 目录
            output_file = ip_output_dir / ip_file.name
            try:
                ip_count = convert_ip_file(ip_file, output_file)
                if ip_count > 0:
                    print(f'✓ IP 规则: {ip_file.name} → geoip/{ip_file.name} ({ip_count} 条)')
                    standalone_count += 1
                    total_ip_rules += ip_count
            except Exception:
                continue

    print('=' * 60)
    print(f'IP 规则处理完成:')
    print(f'  - 追加到域名规则: {appended_count} 个文件')
    print(f'  - 独立 IP 规则: {standalone_count} 个文件')
    print(f'  - IP 规则总数: {total_ip_rules} 条')
    print('=' * 60)
    print(f'总计: {success_count} 个域名规则文件，{appended_count + standalone_count} 个 IP 规则文件')

    if success_count < len(domain_files):
        sys.exit(1)


if __name__ == '__main__':
    main()
