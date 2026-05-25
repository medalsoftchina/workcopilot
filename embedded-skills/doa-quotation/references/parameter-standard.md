# 报价与敏捷拆分参数标准

这份参数标准用于统一 `classic-quotation-template.py` 和 `agile-sprint-template.py` 的输入接口。

## 通用参数

以下字段建议两个脚本统一保留：

| 参数 | 类型 | 说明 |
| ------ | ------ | ------ |
| `output_file` | string | 输出文件名 |
| `project_name` | string | 项目名称 |
| `customer_name` | string | 客户名称 |
| `vendor_name` | string | 报价主体中文名称 |
| `vendor_name_en` | string | 报价主体英文名称，可选 |
| `template_source` | string | 模板来源说明，如 `客户目录/工时报价模板` |
| `quote_date` | date/string | 报价日期 |
| `tax_rate` | number/string | 税率，经典报价建议数值，敏捷模板可展示文本 |
| `expected_total_effort_range` | string | 用户选择的期望总工时范围，如 `10以下`、`10-30`、`30-50`、`50-70`、`70-100` |
| `currency_symbol` | string | 币种符号，默认 `¥` |
| `delivery_cycle` | string | 交付周期/项目周期 |
| `quote_owner` | string | 编制人或销售负责人 |
| `customer_contact` | string | 客户联系人 |
| `customer_email` | string | 客户邮箱 |
| `customer_phone` | string | 客户电话 |
| `remark_notes` | list[string] | 备注条款或说明列表 |

## 经典报价专属参数

| 参数 | 类型 | 说明 |
| ------ | ------ | ------ |
| `quote_title` | string | 报价单标题 |
| `due_days` | int | 截止日期天数 |
| `discount_rate` | number | 折扣系数，如 `0.90` |
| `role_rates` | dict | 角色单价，例如 `{"PM/BA/SA": 3500, "PG/PT": 3000}` |
| `change_request_rates` | dict | CR/Enhancement 单价 |
| `vendor_address_cn` | string | 中文地址 |
| `vendor_address_en` | string | 英文地址 |
| `vendor_tel` | string | 电话 |
| `vendor_fax` | string | 传真 |
| `sales_contact` | string | 销售联系人 |
| `sales_email` | string | 销售邮箱 |
| `sales_phone` | string | 销售电话 |

### 经典报价数据列表

`workload_items` 每项建议结构：

```python
{
    "scenario": "开发实施",
    "task_name": "接口开发与联调",
    "pm_ba_sa_days": 1,
    "pg_pt_days": 5,
    "remark": ""
}
```

## 敏捷拆分专属参数

| 参数 | 类型 | 说明 |
| ------ | ------ | ------ |
| `title` | string | 总览页标题 |
| `methodology` | string | 方法论，如 `Scrum + 持续交付` |
| `iteration_cycle` | string | 迭代周期说明 |
| `duration_text` | string | 总周期说明 |
| `amount_ex_tax` | number | 不含税金额 |
| `amount_inc_tax` | number | 含税金额 |
| `pm_days_total` | number | PM/BA 总人天 |
| `pg_days_total` | number | PG/PT 总人天 |
| `total_days` | number | 总人天 |

### 敏捷拆分数据列表

`sprints` 每项建议结构：

```python
{
    "sprint": "Sprint 1",
    "name": "核心功能开发",
    "period": "第3-4周",
    "goal": "完成核心模块",
    "pm_days": 0,
    "pg_days": 8,
    "fee": 17600,
    "milestone": "核心模块可用",
    "acceptance": "核心接口打通"
}
```

`tasks` 每项建议结构：

```python
{
    "task_id": "T-1.1",
    "sprint": "Sprint 1",
    "quote_id": "2",
    "category": "功能开发",
    "sub_item": "核心模块",
    "task_name": "核心功能开发",
    "description": "实现首批功能",
    "role": "PG/PT",
    "pm_days": 0,
    "pg_days": 2,
    "fee": 4400,
    "priority": "P0",
    "dependency": "T-0.1",
    "story_id": "1.1",
    "acceptance": "功能可演示",
    "status": "未开始"
}
```

## 使用原则

1. 优先只替换参数数据，不先改脚本结构。
2. 同一个项目中，经典报价与敏捷拆分尽量复用相同的 `project_name`、`customer_name`、`vendor_name`、`tax_rate`。
3. 如果客户模板有强约束，可以增加字段，但尽量不要删除通用字段。
4. 若存在多个模板族，先保持参数名一致，再做模板分支差异化。
