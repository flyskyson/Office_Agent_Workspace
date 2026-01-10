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