"""
改进的文件识别功能
支持无分隔符文件名（如：王五身份证.jpg）
"""

import os
import json


def identify_file_improved(filename, config):
    """
    改进的文件识别函数

    支持格式：
    1. 张三_身份证.jpg (下划线)
    2. 张三-身份证.jpg (横杠)
    3. 张三身份证.jpg (无分隔符) ← 新增支持！

    参数:
        filename: 文件名
        config: 配置字典

    返回:
        (申请人名字, 材料类型)
    """
    # 去掉扩展名
    name_without_ext = os.path.splitext(filename)[0]

    # 初始化
    applicant = None
    material = "其他材料"

    # ========== 步骤1: 尝试识别材料类型 ==========
    found_materials = []
    remaining_text = name_without_ext

    # 遍历所有材料类型
    for material_type, keywords in config['file_patterns'].items():
        for keyword in keywords:
            if keyword in remaining_text.lower():
                found_materials.append(material_type)
                # 找到关键词位置
                idx = remaining_text.lower().find(keyword)
                # 提取关键词前面的部分（可能是申请人）
                remaining_text = remaining_text[:idx]
                break
        if found_materials:
            break

    # 如果找到材料类型
    if found_materials:
        material = found_materials[0]

    # ========== 步骤2: 提取申请人名字 ==========

    # 方法1: 下划线分隔
    if '_' in filename:
        parts = filename.split('_')
        applicant = parts[0]

    # 方法2: 横杠分隔
    elif '-' in filename:
        parts = filename.split('-')
        applicant = parts[0]

    # 方法3: 无分隔符（新增！）
    else:
        # remaining_text 是去掉了材料类型后的剩余部分
        # 例如: "王五身份证" → 找到"身份证" → remaining="王五"
        if remaining_text and len(remaining_text) > 0:
            # 去掉可能的分隔符和空格
            applicant = remaining_text.strip('_- ')

            # 如果剩余部分太短（少于2个字符），可能不是名字
            if len(applicant) < 2:
                applicant = None
            # 如果剩余部分太长（超过10个字符），可能识别错误
            elif len(applicant) > 10:
                applicant = None
        else:
            applicant = None

    return applicant, material


# ========== 测试代码 ==========
def test_improved_identify():
    """测试改进的识别功能"""
    # 加载配置
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    # 测试用例
    test_cases = [
        # (文件名, 预期申请人, 预期材料类型)
        ("张三_身份证.jpg", "张三", "身份证"),
        ("李四-申请表.docx", "李四", "申请表"),
        ("王五身份证.png", "王五", "身份证"),  # 无分隔符
        ("赵六租赁合同.pdf", "赵六", "租赁合同"),  # 无分隔符
        ("test_id.jpg", "test", "身份证"),
        ("租赁合同.pdf", None, "租赁合同"),  # 无申请人
        ("营业执照.pdf", None, "其他材料"),  # 未定义类型
    ]

    print("=" * 70)
    print("改进版识别功能测试")
    print("=" * 70)
    print()

    results = []

    for filename, expected_applicant, expected_material in test_cases:
        # 调用改进的识别函数
        applicant, material = identify_file_improved(filename, config)

        # 检查结果
        applicant_match = applicant == expected_applicant
        material_match = material == expected_material

        status = "[OK]" if (applicant_match and material_match) else "[FAIL]"

        print(f"{status} {filename}")
        print(f"   申请人: {applicant} (预期: {expected_applicant}) {'O' if applicant_match else 'X'}")
        print(f"   材料类型: {material} (预期: {expected_material}) {'O' if material_match else 'X'}")
        print()

        results.append(applicant_match and material_match)

    # 统计
    success_count = sum(results)
    total_count = len(results)
    success_rate = success_count / total_count * 100

    print("=" * 70)
    print(f"测试结果: {success_count}/{total_count} 通过 ({success_rate:.1f}%)")
    print("=" * 70)

    if success_rate >= 85:
        print("\n[成功] 识别效果良好！")
    else:
        print("\n[提示] 还有改进空间")


if __name__ == '__main__':
    test_improved_identify()
