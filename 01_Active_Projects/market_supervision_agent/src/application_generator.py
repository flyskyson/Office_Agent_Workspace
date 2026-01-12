"""
申请书生成器 - 复用v3.0的Jinja2模板系统

功能：
- 加载Word模板
- 填充经营户数据
- 生成申请书文档
- 模板管理
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from loguru import logger

try:
    from docxtpl import DocxTemplate
    HAS_DOCTPL = True
except ImportError:
    HAS_DOCTPL = False
    logger.warning("docxtpl未安装，请运行: pip install docxtpl")


class ApplicationGenerator:
    """申请书生成器 - 复用v3.0模板系统"""

    def __init__(self, template_path: str = "templates", config_path: str = "config.json"):
        """初始化生成器

        Args:
            template_path: 模板目录路径
            config_path: 配置文件路径
        """
        self.template_path = Path(template_path)
        self.config_path = Path(config_path)

        # 加载配置
        self.config = self._load_config()

        logger.info(f"申请书生成器初始化: 模板路径={self.template_path}")

    def _load_config(self) -> Dict:
        """加载全局配置

        Returns:
            配置字典
        """
        if not self.config_path.exists():
            logger.warning(f"配置文件不存在: {self.config_path}")
            return self._get_default_config()

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载配置失败: {e}")
            return self._get_default_config()

    def _get_default_config(self) -> Dict:
        """获取默认配置"""
        return {
            'constants': {
                'postal_code': '537820',
                'operation_period': '长期',
                'region': '广西壮族自治区玉林市兴业县蒲塘镇'
            },
            'defaults': {
                'business_scope_licensed': '小餐饮',
                'business_scope_general': '食品销售（仅销售预包装食品）'
            },
            'field_mappings': {}
        }

    def generate_application(
        self,
        operator_data: Dict,
        template_name: str = "个体工商户开业登记申请书.docx",
        output_dir: str = "output"
    ) -> str:
        """生成申请书

        Args:
            operator_data: 经营户数据
            template_name: 模板文件名
            output_dir: 输出目录

        Returns:
            生成文件路径
        """
        if not HAS_DOCTPL:
            raise RuntimeError("docxtpl未安装，请运行: pip install docxtpl")

        # 加载模板
        template_file = self.template_path / template_name
        if not template_file.exists():
            raise FileNotFoundError(f"模板文件不存在: {template_file}")

        # 准备上下文数据
        context = self._prepare_context(operator_data)

        # 渲染模板
        doc = DocxTemplate(str(template_file))
        doc.render(context)

        # 保存文件
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # 使用安全的文件名，避免中文文件名问题
        operator_name = operator_data.get('operator_name', 'unknown')
        id_card = operator_data.get('id_card', '')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 文件名格式: application_身份证后4位_时间戳.docx
        # 避免使用中文店名或姓名
        id_suffix = id_card[-4:] if id_card else '0000'
        safe_filename = f"application_{id_suffix}_{timestamp}.docx"
        output_file = output_path / safe_filename

        # 创建元数据文件保存原始信息
        metadata_file = output_path / f".{safe_filename}.meta.json"
        import json
        metadata = {
            "operator_name": operator_name,
            "business_name": operator_data.get('business_name', ''),
            "id_card": id_card,
            "original_filename": f"{operator_data.get('business_name', operator_name)}_申请书_{timestamp}.docx",
            "generated_at": datetime.now().isoformat()
        }
        metadata_file.write_text(json.dumps(metadata, ensure_ascii=False), encoding='utf-8')

        doc.save(str(output_file))

        logger.info(f"申请书生成成功: {output_file} (经营者: {operator_name})")
        return str(output_file)

    def _prepare_context(self, operator_data: Dict) -> Dict:
        """准备模板渲染上下文

        Args:
            operator_data: 原始数据

        Returns:
            模板上下文字典
        """
        # 合并数据：常量 < 默认值 < 用户数据
        context = {}

        # 1. 应用常量
        context.update(self.config.get('constants', {}))

        # 2. 应用默认值（用户数据优先）
        defaults = self.config.get('defaults', {})
        for key, value in defaults.items():
            if key not in operator_data or not operator_data[key]:
                context[key] = value

        # 3. 应用用户数据
        context.update(operator_data)

        # 4. 字段映射（如果配置了映射）
        field_mappings = self.config.get('field_mappings', {})
        if field_mappings:
            mapped_context = {}
            for template_field, data_field in field_mappings.items():
                if data_field in context:
                    mapped_context[template_field] = context[data_field]
            # 合并映射和未映射的字段
            context = {**mapped_context, **context}

        # 5. 特殊字段处理
        context = self._process_special_fields(context)

        return context

    def _process_special_fields(self, context: Dict) -> Dict:
        """处理特殊字段

        Args:
            context: 上下文字典

        Returns:
            处理后的上下文
        """
        # 处理经营范围（分许可项目和一般项目）
        if 'business_scope' in context:
            scope = context['business_scope']

            if isinstance(scope, str):
                # 尝试分割
                parts = [s.strip() for s in scope.replace('；', ';').split(';')]

                if len(parts) >= 2:
                    context['business_scope_licensed'] = parts[0]
                    context['business_scope_general'] = '；'.join(parts[1:])
                else:
                    context['business_scope_licensed'] = scope
                    context['business_scope_general'] = context.get(
                        'business_scope_general',
                        '食品销售（仅销售预包装食品）'
                    )

        # 确保有许可和一般项目字段
        if 'business_scope_licensed' not in context:
            context['business_scope_licensed'] = context.get('business_scope', '')
        if 'business_scope_general' not in context:
            context['business_scope_general'] = context.get(
                'business_scope_general',
                '食品销售（仅销售预包装食品）'
            )

        # 处理性别
        if 'gender' in context and context['gender']:
            g = context['gender']
            if g in ['男', 'M', 'Male', '男性']:
                context['gender'] = '男'
            elif g in ['女', 'F', 'Female', '女性']:
                context['gender'] = '女'

        # 添加当前日期
        context['current_date'] = datetime.now().strftime('%Y年%m月%d日')
        context['current_year'] = datetime.now().strftime('%Y')
        context['current_month'] = datetime.now().strftime('%m')

        return context

    def list_templates(self) -> List[Dict]:
        """列出所有可用模板

        Returns:
            模板列表
        """
        templates = []

        if not self.template_path.exists():
            return templates

        for template_file in self.template_path.glob('*.docx'):
            templates.append({
                'name': template_file.name,
                'path': str(template_file),
                'size_kb': round(template_file.stat().st_size / 1024, 2)
            })

        return sorted(templates, key=lambda x: x['name'])

    def validate_template(self, template_name: str) -> Dict:
        """验证模板并获取所需变量

        Args:
            template_name: 模板文件名

        Returns:
            验证结果
        """
        if not HAS_DOCTPL:
            return {'error': 'docxtpl未安装'}

        template_file = self.template_path / template_name
        if not template_file.exists():
            return {'error': f'模板文件不存在: {template_name}'}

        try:
            doc = DocxTemplate(str(template_file))
            variables = doc.get_undeclared_template_variables()

            return {
                'template': template_name,
                'variables': sorted(list(variables)),
                'variable_count': len(variables)
            }
        except Exception as e:
            return {'error': f'验证失败: {str(e)}'}

    def check_data_completeness(
        self,
        operator_data: Dict,
        template_name: str
    ) -> Dict:
        """检查数据完整性

        Args:
            operator_data: 经营户数据
            template_name: 模板文件名

        Returns:
            完整性检查结果
        """
        validation = self.validate_template(template_name)

        if 'error' in validation:
            return validation

        required_vars = set(validation['variables'])
        provided_vars = set(operator_data.keys())

        missing = required_vars - provided_vars
        extra = provided_vars - required_vars

        return {
            'template': template_name,
            'required': len(required_vars),
            'provided': len(provided_vars & required_vars),
            'missing_fields': sorted(list(missing)),
            'extra_fields': sorted(list(extra)),
            'is_complete': len(missing) == 0
        }

    def batch_generate(
        self,
        operators_data: List[Dict],
        template_name: str = "个体工商户开业登记申请书.docx",
        output_dir: str = "output"
    ) -> List[Dict]:
        """批量生成申请书

        Args:
            operators_data: 经营户数据列表
            template_name: 模板文件名
            output_dir: 输出目录

        Returns:
            生成结果列表
        """
        results = []

        for i, data in enumerate(operators_data):
            try:
                output_path = self.generate_application(
                    data,
                    template_name,
                    output_dir
                )

                results.append({
                    'index': i,
                    'success': True,
                    'output': output_path,
                    'operator_name': data.get('operator_name', ''),
                    'business_name': data.get('business_name', '')
                })

            except Exception as e:
                results.append({
                    'index': i,
                    'success': False,
                    'error': str(e),
                    'operator_name': data.get('operator_name', ''),
                })
                logger.error(f"生成失败 (#{i}): {e}")

        # 汇总
        success_count = sum(1 for r in results if r['success'])
        logger.info(f"批量生成完成: {success_count}/{len(operators_data)} 成功")

        return results


# 便捷函数
def generate_application(
    operator_data: Dict,
    template_name: str = "个体工商户开业登记申请书.docx",
    output_dir: str = "output"
) -> str:
    """便捷函数：生成申请书

    Args:
        operator_data: 经营户数据
        template_name: 模板文件名
        output_dir: 输出目录

    Returns:
        生成文件路径
    """
    generator = ApplicationGenerator()
    return generator.generate_application(operator_data, template_name, output_dir)


def generate_from_database(
    db,
    operator_id: int,
    template_name: str = "个体工商户开业登记申请书.docx",
    output_dir: str = "output"
) -> str:
    """便捷函数：从数据库记录生成申请书

    Args:
        db: DatabaseManager实例
        operator_id: 经营户ID
        template_name: 模板文件名
        output_dir: 输出目录

    Returns:
        生成文件路径
    """
    # 获取数据
    operator = db.get_operator_by_id(operator_id)
    if not operator:
        raise ValueError(f"经营户不存在: ID={operator_id}")

    # 生成
    generator = ApplicationGenerator()
    return generator.generate_application(operator, template_name, output_dir)
