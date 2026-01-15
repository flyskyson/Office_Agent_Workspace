#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理工具 - 管理项目配置文件

功能:
1. 查看当前配置
2. 编辑配置
3. 重置为默认配置
4. 导出/导入配置
5. 验证配置正确性

作者: Claude Code
日期: 2026-01-12
"""

import json
import sys
from pathlib import Path


class ConfigManager:
    """配置管理器"""

    def __init__(self, config_file="config.json"):
        self.config_file = Path(__file__).parent / config_file
        self.config = self.load()

    def load(self):
        """加载配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[警告] 配置文件不存在: {self.config_file}")
            return self.get_default_config()
        except json.JSONDecodeError as e:
            print(f"[错误] 配置文件格式错误: {e}")
            return self.get_default_config()

    def save(self, config=None):
        """保存配置文件"""
        if config is None:
            config = self.config

        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            print(f"[成功] 配置已保存到: {self.config_file}")
            return True
        except Exception as e:
            print(f"[错误] 保存配置失败: {e}")
            return False

    def get_default_config(self):
        """获取默认配置"""
        return {
            "_说明": "全局配置文件 - 包含常量数据和默认值",
            "_版本": "v3.0",
            "_最后更新": "2026-01-12",

            "constants": {
                "_说明": "经营户数据区常量 - 这些字段在每次申请时保持不变",
                "postal_code": "537820",
                "postal_code_说明": "广西玉林市兴业县蒲塘镇邮政编码",
                "id_card_type": "身份证",
                "id_card_type_说明": "经营者身份证件类型，固定为身份证",
                "region": "广西壮族自治区玉林市兴业县蒲塘镇",
                "region_说明": "所属行政区域"
            },

            "defaults": {
                "_说明": "默认值 - 当用户没有提供时使用这些值",
                "business_scope_licensed": "小餐饮",
                "business_scope_general": "食品销售（仅销售预包装食品）",
                "business_scope_note_licensed": "（依法须经批准的项目，经相关部门批准后方可开展经营活动，具体经营项目以相关部门批准文件或许可证件为准）",
                "business_scope_note_general": "（除依法须经批准的项目外，凭营业执照依法自主开展经营活动）",
                "operation_period": "长期"
            },

            "data_template": {
                "_说明": "数据模板 - 新用户可以参考这个格式准备数据",
                "business_name": "示例：张三便利店",
                "operator_name": "示例：张三",
                "phone": "示例：13800138000",
                "email": "示例：zhangsan@example.com",
                "business_address": "示例：广西玉林市兴业县蒲塘镇商业街88号",
                "id_card": "示例：450101199001011234",
                "gender": "示例：男"
            }
        }

    def show(self):
        """显示当前配置"""
        print("\n" + "=" * 70)
        print("当前配置")
        print("=" * 70)

        # 显示常量
        print("\n【常量配置】")
        constants = self.config.get('constants', {})
        for key, value in constants.items():
            if not key.startswith('_'):
                print(f"  {key}: {value}")

        # 显示默认值
        print("\n【默认值配置】")
        defaults = self.config.get('defaults', {})
        for key, value in defaults.items():
            if not key.startswith('_'):
                print(f"  {key}: {value}")

        # 显示数据模板
        print("\n【数据模板示例】")
        template = self.config.get('data_template', {})
        for key, value in template.items():
            if not key.startswith('_'):
                print(f"  {key}: {value}")

        print("\n" + "=" * 70)

    def edit(self):
        """交互式编辑配置"""
        print("\n配置编辑器")
        print("-" * 70)

        # 编辑常量
        print("\n【编辑常量】")
        constants = self.config.get('constants', {})
        print("当前常量配置:")
        for key, value in constants.items():
            if not key.startswith('_'):
                print(f"  {key}: {value}")

        print("\n是否要修改常量配置？(y/n): ", end='')
        if input().lower() == 'y':
            self._edit_section('constants', constants)

        # 编辑默认值
        print("\n【编辑默认值】")
        defaults = self.config.get('defaults', {})
        print("当前默认值配置:")
        for key, value in defaults.items():
            if not key.startswith('_'):
                print(f"  {key}: {value}")

        print("\n是否要修改默认值配置？(y/n): ", end='')
        if input().lower() == 'y':
            self._edit_section('defaults', defaults)

        # 保存
        print("\n是否保存配置？(y/n): ", end='')
        if input().lower() == 'y':
            self.save()
        else:
            print("[取消] 配置未保存")

    def _edit_section(self, section_name, section_data):
        """编辑配置的某个部分"""
        print(f"\n编辑 {section_name}（留空保持不变）")

        for key in list(section_data.keys()):
            if key.startswith('_'):
                continue

            current_value = section_data[key]
            print(f"{key} [{current_value}]: ", end='')
            new_value = input().strip()

            if new_value:
                section_data[key] = new_value

        self.config[section_name] = section_data

    def reset(self):
        """重置为默认配置"""
        print("\n[警告] 这将覆盖当前配置！")
        print("确定要重置为默认配置吗？(y/n): ", end='')

        if input().lower() == 'y':
            self.config = self.get_default_config()
            self.save()
            print("[成功] 配置已重置为默认值")
        else:
            print("[取消] 操作已取消")

    def export(self, output_file=None):
        """导出配置到文件"""
        if output_file is None:
            output_file = f"config_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        output_path = Path(__file__).parent / output_file

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            print(f"[成功] 配置已导出到: {output_path}")
            return True
        except Exception as e:
            print(f"[错误] 导出配置失败: {e}")
            return False

    def import_config(self, input_file):
        """从文件导入配置"""
        input_path = Path(input_file)

        if not input_path.is_absolute():
            input_path = Path(__file__).parent / input_path

        if not input_path.exists():
            print(f"[错误] 文件不存在: {input_path}")
            return False

        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)

            # 验证导入的配置
            if self.validate(imported_config):
                print("\n导入的配置内容预览:")
                print(json.dumps(imported_config, ensure_ascii=False, indent=2))

                print("\n确定要导入此配置吗？(y/n): ", end='')
                if input().lower() == 'y':
                    self.config = imported_config
                    self.save()
                    print("[成功] 配置已导入")
                    return True
                else:
                    print("[取消] 导入已取消")
                    return False
            else:
                print("[错误] 导入的配置格式不正确")
                return False

        except Exception as e:
            print(f"[错误] 导入配置失败: {e}")
            return False

    def validate(self, config=None):
        """验证配置是否正确"""
        if config is None:
            config = self.config

        required_sections = ['constants', 'defaults', 'data_template']

        for section in required_sections:
            if section not in config:
                print(f"[错误] 缺少必需的配置部分: {section}")
                return False

        return True

    def create_data_template(self):
        """创建数据模板文件"""
        template_data = {}

        # 从配置中获取模板
        data_template = self.config.get('data_template', {})

        print("\n创建新数据文件")
        print("-" * 70)

        for key, value in data_template.items():
            if key.startswith('_'):
                continue

            print(f"{key} {value}")
            new_value = input("请输入: ").strip()

            if new_value and new_value != value:
                # 去掉"示例："前缀
                if new_value.startswith("示例："):
                    new_value = new_value[3:]

            template_data[key] = new_value

        # 保存到文件
        output_file = f"new_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output_path = Path(__file__).parent / output_file

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, ensure_ascii=False, indent=2)
            print(f"\n[成功] 数据文件已创建: {output_file}")
            return output_path
        except Exception as e:
            print(f"[错误] 创建数据文件失败: {e}")
            return None


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description='配置管理工具 - 管理项目配置文件',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--show', action='store_true', help='显示当前配置')
    parser.add_argument('--edit', action='store_true', help='编辑配置')
    parser.add_argument('--reset', action='store_true', help='重置为默认配置')
    parser.add_argument('--export', metavar='输出文件', nargs='?', const='auto',
                        help='导出配置到文件')
    parser.add_argument('--import', metavar='输入文件', dest='import_file',
                        help='从文件导入配置')
    parser.add_argument('--validate', action='store_true', help='验证配置')
    parser.add_argument('--new-data', action='store_true',
                        help='创建新的数据文件')

    args = parser.parse_args()

    manager = ConfigManager()

    if args.show:
        manager.show()

    elif args.edit:
        manager.edit()

    elif args.reset:
        manager.reset()

    elif args.export:
        if args.export == 'auto':
            manager.export()
        else:
            manager.export(args.export)

    elif args.import_file:
        manager.import_config(args.import_file)

    elif args.validate:
        if manager.validate():
            print("[成功] 配置格式正确")
        else:
            print("[错误] 配置格式不正确")
            sys.exit(1)

    elif args.new_data:
        manager.create_data_template()

    else:
        # 默认显示配置
        manager.show()

        print("\n常用命令:")
        print("  python config_manager.py --show      显示当前配置")
        print("  python config_manager.py --edit      编辑配置")
        print("  python config_manager.py --reset     重置为默认配置")
        print("  python config_manager.py --export    导出配置")
        print("  python config_manager.py --new-data  创建新数据文件")


if __name__ == "__main__":
    import datetime
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[中断] 用户取消操作")
        sys.exit(0)
    except Exception as e:
        print(f"\n[异常] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
