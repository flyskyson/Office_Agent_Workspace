#!/usr/bin/env python3
"""
个体工商户申请表自动生成系统
专为市场监管工作人员设计 - 零基础友好版
"""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, Any, List

class ApplicationGenerator:
    """申请表生成器 - 零基础友好设计"""

    def __init__(self, template_dir: str = "templates"):
        """
        初始化申请表生成器

        Args:
            template_dir: 模板文件目录
        """
        self.template_dir = Path(template_dir)
        self.template_dir.mkdir(exist_ok=True)

        # 创建默认模板（如果不存在）
        self._create_default_templates()

        print("=" * 60)
        print("  个体工商户申请表自动生成系统")
        print("  版本 1.0 - 零基础友好设计")
        print("=" * 60)

    def _create_default_templates(self):
        """创建默认模板文件"""
        templates = {
            "设立登记申请书": self._get_registration_template(),
            "变更登记申请书": self._get_change_template(),
            "注销登记申请书": self._get_cancellation_template(),
            "年报申请表": self._get_annual_report_template()
        }

        for name, content in templates.items():
            template_file = self.template_dir / f"{name}.txt"
            if not template_file.exists():
                template_file.write_text(content, encoding='utf-8')
                print(f"[OK] 创建模板文件: {name}.txt")

    def _get_registration_template(self) -> str:
        """获取设立登记申请书模板"""
        return """个体工商户设立登记申请书

申请事项：个体工商户设立登记

一、基本信息
1. 个体工商户名称：{business_name}
2. 经营者姓名：{operator_name}
3. 性别：{gender}
4. 身份证号码：{id_card}
5. 联系电话：{phone}
6. 电子邮箱：{email}

二、经营信息
1. 经营场所：{business_address}
2. 邮政编码：{postal_code}
3. 经营面积：{business_area}平方米
4. 经营范围：{business_scope}
5. 主营业务：{main_business}
6. 行业类型：{business_type}

三、资金信息
1. 资金数额：{registered_capital}元
2. 资金来源：{capital_source}
3. 出资形式：{investment_form}
4. 经营期限：{operation_period}

四、经营者声明
本人承诺所填写内容及提交的材料真实、合法、有效，并对申请材料的真实性负责。

经营者签字：___________________
申请日期：{application_date}

五、附件清单
1. 经营者身份证复印件
2. 经营场所使用证明
3. 其他相关材料
"""

    def _get_change_template(self) -> str:
        """获取变更登记申请书模板"""
        return """个体工商户变更登记申请书

申请事项：个体工商户变更登记

一、原登记信息
1. 个体工商户名称：{original_business_name}
2. 统一社会信用代码：{credit_code}
3. 经营者姓名：{original_operator_name}

二、变更事项
变更类型：{change_type}

{change_details}

三、变更原因
{change_reason}

四、经营者声明
本人承诺所填写内容及提交的材料真实、合法、有效，并对申请材料的真实性负责。

经营者签字：___________________
申请日期：{application_date}

五、附件清单
1. 经营者身份证复印件
2. 变更相关证明文件
3. 其他相关材料
"""

    def _get_cancellation_template(self) -> str:
        """获取注销登记申请书模板"""
        return """个体工商户注销登记申请书

申请事项：个体工商户注销登记

一、基本信息
1. 个体工商户名称：{business_name}
2. 统一社会信用代码：{credit_code}
3. 经营者姓名：{operator_name}
4. 联系电话：{phone}

二、注销信息
1. 注销原因：{cancellation_reason}
2. 清算情况：{liquidation_status}
3. 税务清税证明：{tax_clearance}
4. 社保清缴证明：{social_insurance_clearance}

三、经营者声明
本人承诺所填写内容及提交的材料真实、合法、有效，并对申请材料的真实性负责。
本个体工商户债权债务已清理完毕，如有遗留问题由本人承担全部责任。

经营者签字：___________________
申请日期：{application_date}

四、附件清单
1. 经营者身份证复印件
2. 营业执照正副本
3. 清算报告
4. 税务清税证明
5. 社保清缴证明
6. 其他相关材料
"""

    def _get_annual_report_template(self) -> str:
        """获取年报申请表模板"""
        return """个体工商户年度报告表

报告年度：{report_year}

一、基本信息
1. 个体工商户名称：{business_name}
2. 统一社会信用代码：{credit_code}
3. 经营者姓名：{operator_name}
4. 经营场所：{business_address}
5. 联系电话：{phone}

二、经营情况
1. 年营业收入：{annual_revenue}元
2. 营业成本：{operating_costs}元
3. 毛利润：{gross_profit}元
4. 净利润：{net_profit}元
5. 从业人数：{employee_count}人
6. 资产总额：{asset_total}元
7. 负债总额：{liability_total}元

三、行政许可情况
1. 是否取得行政许可：{has_license}
2. 许可证类型：{license_type}
3. 许可证编号：{license_number}
4. 有效期限：{validity_period}

四、经营者声明
本人承诺所报告内容真实、合法、有效，并对报告内容的真实性负责。

经营者签字：___________________
报告日期：{report_date}

五、备注
{remarks}
"""

    def show_menu(self):
        """显示主菜单"""
        print("\n[菜单] 请选择要生成的申请表类型：")
        print("1. 个体工商户设立登记申请书")
        print("2. 个体工商户变更登记申请书")
        print("3. 个体工商户注销登记申请书")
        print("4. 个体工商户年度报告表")
        print("5. 查看所有模板")
        print("6. 退出系统")

        choice = input("\n请输入选项编号 (1-6): ").strip()
        return choice

    def generate_registration(self):
        """生成设立登记申请书"""
        print("\n[生成] 生成个体工商户设立登记申请书")
        print("请填写以下信息（按Enter跳过可选字段）：")

        data = {
            "business_name": input("个体工商户名称: "),
            "operator_name": input("经营者姓名: "),
            "gender": input("性别（男/女）: "),
            "id_card": input("身份证号码: "),
            "phone": input("联系电话: "),
            "email": input("电子邮箱（可选）: ") or "未提供",
            "business_address": input("经营场所: "),
            "postal_code": input("邮政编码（可选）: ") or "未提供",
            "business_area": input("经营面积（平方米，可选）: ") or "未提供",
            "business_scope": input("经营范围: "),
            "main_business": input("主营业务（可选）: ") or "未提供",
            "business_type": input("行业类型（可选）: ") or "未提供",
            "registered_capital": input("资金数额（元）: "),
            "capital_source": input("资金来源（可选）: ") or "自有资金",
            "investment_form": input("出资形式（可选）: ") or "货币",
            "operation_period": input("经营期限（可选）: ") or "长期",
            "application_date": datetime.datetime.now().strftime("%Y年%m月%d日")
        }

        # 读取模板
        template_file = self.template_dir / "设立登记申请书.txt"
        template = template_file.read_text(encoding='utf-8')

        # 填充模板
        application = template.format(**data)

        # 保存文件
        filename = f"设立登记申请书_{data['business_name']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        output_dir = Path("generated_applications")
        output_dir.mkdir(exist_ok=True)

        output_file = output_dir / filename
        output_file.write_text(application, encoding='utf-8')

        print(f"\n[OK] 申请表生成成功！")
        print(f"📁 保存位置: {output_file}")

        # 同时保存数据为JSON
        data_file = output_dir / f"{filename}.json"
        data_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

        return application

    def generate_change(self):
        """生成变更登记申请书"""
        print("\n[生成] 生成个体工商户变更登记申请书")

        # 选择变更类型
        print("\n请选择变更类型：")
        print("1. 名称变更")
        print("2. 经营者变更")
        print("3. 地址变更")
        print("4. 经营范围变更")
        print("5. 其他变更")

        change_type_map = {
            "1": "名称变更",
            "2": "经营者变更",
            "3": "地址变更",
            "4": "经营范围变更",
            "5": "其他变更"
        }

        change_choice = input("\n请输入变更类型编号 (1-5): ").strip()
        change_type = change_type_map.get(change_choice, "其他变更")

        # 根据变更类型收集信息
        change_details = ""
        if change_type == "名称变更":
            change_details = "原名称：{original_name}\n新名称：{new_name}"
            original_name = input("原个体工商户名称: ")
            new_name = input("新个体工商户名称: ")
            change_details = change_details.format(original_name=original_name, new_name=new_name)
        elif change_type == "经营者变更":
            change_details = "原经营者：{original_operator}\n新经营者：{new_operator}\n新身份证号码：{new_id_card}"
            original_operator = input("原经营者姓名: ")
            new_operator = input("新经营者姓名: ")
            new_id_card = input("新经营者身份证号码: ")
            change_details = change_details.format(
                original_operator=original_operator,
                new_operator=new_operator,
                new_id_card=new_id_card
            )
        elif change_type == "地址变更":
            change_details = "原经营场所：{original_address}\n新经营场所：{new_address}"
            original_address = input("原经营场所: ")
            new_address = input("新经营场所: ")
            change_details = change_details.format(original_address=original_address, new_address=new_address)
        else:
            change_details = input("请描述变更内容: ")

        data = {
            "original_business_name": input("原个体工商户名称: "),
            "credit_code": input("统一社会信用代码: "),
            "original_operator_name": input("原经营者姓名: "),
            "change_type": change_type,
            "change_details": change_details,
            "change_reason": input("变更原因: "),
            "application_date": datetime.datetime.now().strftime("%Y年%m月%d日")
        }

        # 读取模板
        template_file = self.template_dir / "变更登记申请书.txt"
        template = template_file.read_text(encoding='utf-8')

        # 填充模板
        application = template.format(**data)

        # 保存文件
        filename = f"变更登记申请书_{data['original_business_name']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        output_dir = Path("generated_applications")
        output_dir.mkdir(exist_ok=True)

        output_file = output_dir / filename
        output_file.write_text(application, encoding='utf-8')

        print(f"\n[OK] 变更申请表生成成功！")
        print(f"📁 保存位置: {output_file}")

        return application

    def generate_from_json(self, json_file: str):
        """从JSON文件批量生成申请表"""
        json_path = Path(json_file)
        if not json_path.exists():
            print(f"[错误] JSON文件不存在: {json_file}")
            return

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            print(f"\n📊 从JSON文件加载数据成功")
            print(f"数据记录数: {len(data) if isinstance(data, list) else 1}")

            # 判断是单个对象还是列表
            if isinstance(data, dict):
                data_list = [data]
            else:
                data_list = data

            success_count = 0
            for i, item in enumerate(data_list):
                application_type = item.get("业务类型", "设立登记")

                if application_type == "设立登记":
                    result = self._generate_from_dict(item, "设立登记申请书.txt")
                elif application_type == "变更登记":
                    result = self._generate_from_dict(item, "变更登记申请书.txt")
                elif application_type == "注销登记":
                    result = self._generate_from_dict(item, "注销登记申请书.txt")
                elif application_type == "年报":
                    result = self._generate_from_dict(item, "年报申请表.txt")
                else:
                    print(f"⚠️  未知的业务类型: {application_type}")
                    continue

                if result:
                    success_count += 1

            print(f"\n[OK] 批量生成完成！成功生成 {success_count}/{len(data_list)} 个申请表")

        except Exception as e:
            print(f"[错误] 处理JSON文件失败: {str(e)}")

    def _generate_from_dict(self, data: Dict[str, Any], template_name: str) -> bool:
        """从字典数据生成申请表"""
        try:
            # 读取模板
            template_file = self.template_dir / template_name
            template = template_file.read_text(encoding='utf-8')

            # 添加日期字段
            if "application_date" not in data:
                data["application_date"] = datetime.datetime.now().strftime("%Y年%m月%d日")
            if "report_date" not in data and template_name == "年报申请表.txt":
                data["report_date"] = datetime.datetime.now().strftime("%Y年%m月%d日")

            # 填充模板
            application = template.format(**data)

            # 生成文件名
            business_name = data.get("business_name", data.get("个体工商户名称", "未知"))
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{template_name.replace('.txt', '')}_{business_name}_{timestamp}.txt"

            # 保存文件
            output_dir = Path("generated_applications")
            output_dir.mkdir(exist_ok=True)

            output_file = output_dir / filename
            output_file.write_text(application, encoding='utf-8')

            print(f"  [OK] 生成: {filename}")
            return True

        except Exception as e:
            print(f"  [错误] 生成失败: {str(e)}")
            return False

    def show_templates(self):
        """显示所有模板"""
        print("\n📚 可用模板列表：")

        template_files = list(self.template_dir.glob("*.txt"))

        if not template_files:
            print("暂无模板文件")
            return

        for i, template_file in enumerate(template_files, 1):
            print(f"{i}. {template_file.stem}")

            # 显示模板预览
            try:
                content = template_file.read_text(encoding='utf-8')
                preview = content[:200] + "..." if len(content) > 200 else content
                print(f"   预览: {preview}")
                print()
            except:
                print(f"   无法读取模板内容")
                print()

def main():
    """主函数"""
    print("正在启动申请表自动生成系统...")

    # 创建生成器实例
    generator = ApplicationGenerator()

    while True:
        choice = generator.show_menu()

        if choice == "1":
            generator.generate_registration()
        elif choice == "2":
            generator.generate_change()
        elif choice == "3":
            print("注销登记功能开发中...")
            # generator.generate_cancellation()
        elif choice == "4":
            print("年报功能开发中...")
            # generator.generate_annual_report()
        elif choice == "5":
            generator.show_templates()
        elif choice == "6":
            print("\n[再见] 感谢使用申请表自动生成系统！")
            print("生成的文件保存在 generated_applications/ 目录中")
            break
        elif choice.lower() == "json":
            # 隐藏功能：从JSON文件批量生成
            json_file = input("请输入JSON文件路径: ").strip()
            generator.generate_from_json(json_file)
        else:
            print("[错误] 无效选项，请重新选择")

        input("\n按Enter键继续...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[退出] 程序已退出")
    except Exception as e:
        print(f"\n[错误] 程序运行出错: {str(e)}")
        import traceback
        traceback.print_exc()