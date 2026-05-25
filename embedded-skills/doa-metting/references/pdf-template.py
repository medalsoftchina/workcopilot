# -*- coding: utf-8 -*-
"""
会议纪要 PDF 生成模板
====================
使用方法：
  1. pip install reportlab
  2. 修改 build_pdf() 中的会议内容数据
  3. python pdf-template.py

此模板提供完整的基础设施（字体、颜色、样式、组件），
只需替换 build_pdf() 中的实际会议数据即可生成专业 PDF。
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.flowables import Flowable
import os, platform


# ══════════════════════════════════════════════
# 字体注册（跨平台自动适配）
# ══════════════════════════════════════════════
def register_fonts():
    """注册中文字体，按优先级尝试 Windows / macOS / Linux"""
    font_candidates = {
        "win32": [
            ("C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/msyhbd.ttc"),
            ("C:/Windows/Fonts/simhei.ttf", "C:/Windows/Fonts/simhei.ttf"),
        ],
        "darwin": [
            ("/System/Library/Fonts/PingFang.ttc", "/System/Library/Fonts/PingFang.ttc"),
            ("/System/Library/Fonts/STHeiti Medium.ttc", "/System/Library/Fonts/STHeiti Medium.ttc"),
        ],
        "linux": [
            ("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc", "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"),
            ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"),
        ],
    }

    system = platform.system().lower()
    if system == "windows":
        key = "win32"
    elif system == "darwin":
        key = "darwin"
    else:
        key = "linux"

    for regular, bold in font_candidates.get(key, []):
        try:
            pdfmetrics.registerFont(TTFont("ChineseFont", regular))
            pdfmetrics.registerFont(TTFont("ChineseFontBold", bold))
            return True
        except Exception:
            continue

    # Fallback: 尝试所有平台
    for k, paths in font_candidates.items():
        for regular, bold in paths:
            try:
                pdfmetrics.registerFont(TTFont("ChineseFont", regular))
                pdfmetrics.registerFont(TTFont("ChineseFontBold", bold))
                return True
            except Exception:
                continue

    print("⚠️  未找到中文字体，使用默认字体（中文可能显示异常）")
    pdfmetrics.registerFont(TTFont("ChineseFont", "Helvetica"))
    pdfmetrics.registerFont(TTFont("ChineseFontBold", "Helvetica-Bold"))
    return False

register_fonts()


# ══════════════════════════════════════════════
# 颜色体系（商务蓝主题）
# ══════════════════════════════════════════════
C_PRIMARY    = HexColor("#1A365D")   # 深蓝 - 主标题、表头
C_SECONDARY  = HexColor("#2B6CB0")   # 中蓝 - 章节标题
C_ACCENT     = HexColor("#3182CE")   # 亮蓝 - 强调、流程编号
C_LIGHT_BG   = HexColor("#EBF4FF")   # 浅蓝背景 - 信息卡片
C_LIGHT_GRAY = HexColor("#F7FAFC")   # 极浅灰 - 交替行
C_BORDER     = HexColor("#CBD5E0")   # 边框灰
C_TEXT       = HexColor("#2D3748")   # 正文色
C_SUBTEXT    = HexColor("#718096")   # 辅助文字
C_SUCCESS    = HexColor("#276749")   # 绿色 - 达成共识
C_WARNING    = HexColor("#C05621")   # 橙色 - 待确认项
C_RED        = HexColor("#C53030")   # 红色 - 紧急/重要


# ══════════════════════════════════════════════
# 样式定义
# ══════════════════════════════════════════════
styles = {}

styles["title"] = ParagraphStyle(
    "title", fontName="ChineseFontBold", fontSize=20, leading=28,
    textColor=C_PRIMARY, alignment=TA_CENTER, spaceAfter=4*mm,
)

styles["subtitle"] = ParagraphStyle(
    "subtitle", fontName="ChineseFont", fontSize=11, leading=16,
    textColor=C_SUBTEXT, alignment=TA_CENTER, spaceAfter=8*mm,
)

styles["h1"] = ParagraphStyle(
    "h1", fontName="ChineseFontBold", fontSize=14, leading=20,
    textColor=C_PRIMARY, spaceBefore=10*mm, spaceAfter=4*mm,
)

styles["h2"] = ParagraphStyle(
    "h2", fontName="ChineseFontBold", fontSize=12, leading=18,
    textColor=C_SECONDARY, spaceBefore=6*mm, spaceAfter=3*mm,
)

styles["h3"] = ParagraphStyle(
    "h3", fontName="ChineseFontBold", fontSize=10.5, leading=16,
    textColor=C_ACCENT, spaceBefore=4*mm, spaceAfter=2*mm,
)

styles["body"] = ParagraphStyle(
    "body", fontName="ChineseFont", fontSize=10, leading=16,
    textColor=C_TEXT, alignment=TA_JUSTIFY, spaceAfter=2*mm,
)

styles["bullet"] = ParagraphStyle(
    "bullet", fontName="ChineseFont", fontSize=10, leading=16,
    textColor=C_TEXT, leftIndent=12*mm, bulletIndent=6*mm,
    spaceAfter=1.5*mm,
)

styles["bullet_sub"] = ParagraphStyle(
    "bullet_sub", fontName="ChineseFont", fontSize=9.5, leading=15,
    textColor=C_SUBTEXT, leftIndent=20*mm, bulletIndent=14*mm,
    spaceAfter=1*mm,
)

styles["info_label"] = ParagraphStyle(
    "info_label", fontName="ChineseFontBold", fontSize=9.5, leading=14,
    textColor=C_SUBTEXT,
)

styles["info_value"] = ParagraphStyle(
    "info_value", fontName="ChineseFont", fontSize=9.5, leading=14,
    textColor=C_TEXT,
)

styles["consensus"] = ParagraphStyle(
    "consensus", fontName="ChineseFont", fontSize=10, leading=16,
    textColor=C_SUCCESS, leftIndent=12*mm, bulletIndent=6*mm,
    spaceAfter=1.5*mm,
)

styles["warning"] = ParagraphStyle(
    "warning", fontName="ChineseFont", fontSize=10, leading=16,
    textColor=C_WARNING, leftIndent=12*mm, bulletIndent=6*mm,
    spaceAfter=1.5*mm,
)

styles["footer"] = ParagraphStyle(
    "footer", fontName="ChineseFont", fontSize=8, leading=10,
    textColor=C_SUBTEXT, alignment=TA_CENTER,
)


# ══════════════════════════════════════════════
# 自定义 Flowable 组件
# ══════════════════════════════════════════════
class SectionHeader(Flowable):
    """带色块的章节标题栏（圆角色底 + 白色文字）"""
    def __init__(self, text, color=C_PRIMARY, width=170*mm, height=9*mm):
        super().__init__()
        self.text = text
        self.color = color
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        return self.width, self.height + 2*mm

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.roundRect(0, 0, self.width, self.height, 2*mm, fill=1, stroke=0)
        self.canv.setFillColor(white)
        self.canv.setFont("ChineseFontBold", 12)
        self.canv.drawString(4*mm, 2.5*mm, self.text)


class InfoBox(Flowable):
    """信息卡片（浅蓝底 + 边框，用于展示基本信息）"""
    def __init__(self, data, width=170*mm):
        super().__init__()
        self.data = data  # list of (label, value)
        self.w = width
        self.row_h = 8*mm
        self.h = len(data) * self.row_h + 4*mm

    def wrap(self, availWidth, availHeight):
        return self.w, self.h

    def draw(self):
        c = self.canv
        c.setFillColor(C_LIGHT_BG)
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(0.5)
        c.roundRect(0, 0, self.w, self.h, 3*mm, fill=1, stroke=1)

        y = self.h - 6*mm
        for label, value in self.data:
            c.setFont("ChineseFontBold", 9.5)
            c.setFillColor(C_SUBTEXT)
            c.drawString(5*mm, y, label)
            c.setFont("ChineseFont", 9.5)
            c.setFillColor(C_TEXT)
            c.drawString(32*mm, y, value)
            y -= self.row_h


class DividerLine(Flowable):
    """分隔线"""
    def __init__(self, width=170*mm, color=C_BORDER):
        super().__init__()
        self.w = width
        self.color = color

    def wrap(self, availWidth, availHeight):
        return self.w, 1*mm

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(0.3)
        self.canv.line(0, 0, self.w, 0)


# ══════════════════════════════════════════════
# 辅助函数
# ══════════════════════════════════════════════
def make_header_footer(project_name, company_name, confidential_label="CONFIDENTIAL 机密"):
    """
    创建页眉页脚回调函数。

    参数:
        project_name:       页眉左侧显示的项目名称
        company_name:       页脚左侧显示的公司名称
        confidential_label: 页眉右侧标签（可选，设为 None 不显示）
    """
    def _header_footer(canvas, doc):
        canvas.saveState()
        w, h = A4

        # 页眉
        canvas.setStrokeColor(C_PRIMARY)
        canvas.setLineWidth(2)
        canvas.line(20*mm, h - 12*mm, w - 20*mm, h - 12*mm)
        canvas.setFont("ChineseFont", 7.5)
        canvas.setFillColor(C_SUBTEXT)
        canvas.drawString(20*mm, h - 11*mm, project_name)
        if confidential_label:
            canvas.drawRightString(w - 20*mm, h - 11*mm, confidential_label)

        # 页脚
        canvas.setStrokeColor(C_BORDER)
        canvas.setLineWidth(0.5)
        canvas.line(20*mm, 14*mm, w - 20*mm, 14*mm)
        canvas.setFont("ChineseFont", 8)
        canvas.setFillColor(C_SUBTEXT)
        canvas.drawString(20*mm, 9*mm, company_name)
        canvas.drawRightString(w - 20*mm, 9*mm, f"第 {doc.page} 页")

        canvas.restoreState()

    return _header_footer


def make_key_value_table(data, col_widths=None):
    """
    创建左侧标签 + 右侧值的表格（适用于交互方式、参数等）。

    参数:
        data:       list of [label, value] 字符串
        col_widths: [标签列宽, 值列宽]，默认 [30mm, 135mm]
    """
    if col_widths is None:
        col_widths = [30*mm, 135*mm]

    t_data = [[
        Paragraph(f"<b>{row[0]}</b>", ParagraphStyle("tc", fontName="ChineseFontBold", fontSize=9.5, textColor=C_PRIMARY, leading=14)),
        Paragraph(row[1], ParagraphStyle("tv", fontName="ChineseFont", fontSize=9.5, textColor=C_TEXT, leading=14)),
    ] for row in data]

    t = Table(t_data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), C_LIGHT_BG),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3*mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3*mm),
        ("LEFTPADDING", (0, 0), (-1, -1), 3*mm),
        ("GRID", (0, 0), (-1, -1), 0.4, C_BORDER),
        ("ROUNDEDCORNERS", [2, 2, 2, 2]),
    ]))
    return t


def make_action_table(rows):
    """
    创建行动计划表格。

    参数:
        rows: list of [责任方, 行动项(可含<br/>), 时间节点]
    """
    cell_style = ParagraphStyle("cs", fontName="ChineseFont", fontSize=9.5, textColor=C_TEXT, leading=15)
    label_style = ParagraphStyle("ls", fontName="ChineseFontBold", fontSize=9.5, textColor=C_PRIMARY, leading=15, alignment=TA_CENTER)
    time_style = ParagraphStyle("ts", fontName="ChineseFont", fontSize=9.5, textColor=C_TEXT, leading=15, alignment=TA_CENTER)

    headers = [
        Paragraph("<b>责任方</b>", ParagraphStyle("ah", fontName="ChineseFontBold", fontSize=9.5, textColor=white, leading=14, alignment=TA_CENTER)),
        Paragraph("<b>行动项</b>", ParagraphStyle("ah2", fontName="ChineseFontBold", fontSize=9.5, textColor=white, leading=14, alignment=TA_CENTER)),
        Paragraph("<b>时间节点</b>", ParagraphStyle("ah3", fontName="ChineseFontBold", fontSize=9.5, textColor=white, leading=14, alignment=TA_CENTER)),
    ]

    t_rows = [headers]
    for row in rows:
        t_rows.append([
            Paragraph(row[0], label_style),
            Paragraph(row[1], cell_style),
            Paragraph(row[2], time_style),
        ])

    t = Table(t_rows, colWidths=[30*mm, 110*mm, 25*mm])
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), C_PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("BACKGROUND", (0, 1), (0, -1), C_LIGHT_BG),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3*mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3*mm),
        ("LEFTPADDING", (0, 0), (-1, -1), 3*mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3*mm),
        ("GRID", (0, 0), (-1, -1), 0.5, C_BORDER),
    ]
    # 交替行色
    for i in range(2, len(t_rows), 2):
        style_cmds.append(("BACKGROUND", (1, i), (-1, i), C_LIGHT_GRAY))

    t.setStyle(TableStyle(style_cmds))
    return t


def make_conclusion_box(text):
    """创建结论高亮框"""
    box = Table(
        [[Paragraph(
            text,
            ParagraphStyle("cf", fontName="ChineseFont", fontSize=11, textColor=C_PRIMARY, leading=18)
        )]],
        colWidths=[165*mm],
    )
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_LIGHT_BG),
        ("TOPPADDING", (0, 0), (-1, -1), 5*mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5*mm),
        ("LEFTPADDING", (0, 0), (-1, -1), 6*mm),
        ("BOX", (0, 0), (-1, -1), 1.5, C_PRIMARY),
    ]))
    return box


def make_flow_table(steps):
    """
    创建流程步骤表格。

    参数:
        steps: list of [序号, 角色, 操作说明]
    """
    flow_data = [[
        Paragraph(f"<b>{r[0]}</b>", ParagraphStyle("fn", fontName="ChineseFontBold", fontSize=10, textColor=C_ACCENT, leading=14, alignment=TA_CENTER)),
        Paragraph(f"<b>{r[1]}</b>", ParagraphStyle("fr", fontName="ChineseFontBold", fontSize=9.5, textColor=C_PRIMARY, leading=14, alignment=TA_CENTER)),
        Paragraph(r[2], ParagraphStyle("fd", fontName="ChineseFont", fontSize=9.5, textColor=C_TEXT, leading=14)),
    ] for r in steps]

    t = Table(flow_data, colWidths=[12*mm, 30*mm, 123*mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5*mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5*mm),
        ("LEFTPADDING", (0, 0), (-1, -1), 2*mm),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, C_BORDER),
        ("BACKGROUND", (0, 0), (0, -1), C_LIGHT_BG),
        ("BACKGROUND", (1, 0), (1, -1), C_LIGHT_BG),
    ]))
    return t


# ══════════════════════════════════════════════
# 构建 PDF 文档（示例：替换为实际会议内容）
# ══════════════════════════════════════════════
def build_pdf():
    # ── 配置区 ──
    filename = "会议纪要.pdf"
    project_name = "项目名 · 会议纪要"
    company_name = "公司名称"
    confidential = "CONFIDENTIAL 机密"  # 设为 None 不显示

    hf = make_header_footer(project_name, company_name, confidential)

    doc = SimpleDocTemplate(
        filename, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=18*mm, bottomMargin=20*mm,
    )

    story = []
    S = styles

    # ══════ 封面区域 ══════
    story.append(Spacer(1, 15*mm))
    story.append(Paragraph("会 议 纪 要", S["title"]))
    story.append(Paragraph("会议主题副标题", S["subtitle"]))
    story.append(Spacer(1, 4*mm))

    # 基本信息卡片
    story.append(InfoBox([
        ("会议主题:", "XXXXXX"),
        ("参 会 方:", "XXXXXX"),
        ("核心目标:", "XXXXXX"),
        ("会议日期:", "XXXX-XX-XX"),
    ]))
    story.append(Spacer(1, 8*mm))
    story.append(DividerLine())
    story.append(Spacer(1, 4*mm))

    # ══════ 一、会议核心内容 ══════
    story.append(SectionHeader("一、会议核心内容"))
    story.append(Spacer(1, 4*mm))

    # 议题 1
    story.append(Paragraph("1. 议题标题", S["h2"]))
    for text in [
        "要点一",
        "要点二",
        "要点三",
    ]:
        story.append(Paragraph(f"• {text}", S["bullet"]))

    # 议题 2（带键值表格的示例）
    story.append(Paragraph("2. 议题标题", S["h2"]))
    story.append(make_key_value_table([
        ["标签A", "值A"],
        ["标签B", "值B"],
    ]))

    # ══════ 二、达成共识 ══════
    story.append(Spacer(1, 4*mm))
    story.append(SectionHeader("二、达成共识", color=C_SUCCESS))
    story.append(Spacer(1, 4*mm))

    for i, text in enumerate([
        "共识项 1",
        "共识项 2",
    ], 1):
        story.append(Paragraph(f"✅  {i}. {text}", S["consensus"]))

    # ══════ 三、待确认 / 待澄清项 ══════
    story.append(Spacer(1, 4*mm))
    story.append(SectionHeader("三、待确认 / 待澄清项", color=C_WARNING))
    story.append(Spacer(1, 4*mm))

    for i, text in enumerate([
        "待确认项 1",
        "待确认项 2",
    ], 1):
        story.append(Paragraph(f"⚠️  {i}. {text}", S["warning"]))

    # ══════ 四、后续行动计划 ══════
    story.append(Spacer(1, 4*mm))
    story.append(SectionHeader("四、后续行动计划", color=C_SECONDARY))
    story.append(Spacer(1, 4*mm))

    story.append(make_action_table([
        ["责任方A", "• 行动项 1<br/>• 行动项 2", "时间节点"],
        ["责任方B", "• 行动项 3", "时间节点"],
    ]))

    # ══════ 五、会议结论 ══════
    story.append(Spacer(1, 6*mm))
    story.append(SectionHeader("五、会议结论", color=C_PRIMARY))
    story.append(Spacer(1, 4*mm))
    story.append(make_conclusion_box("会议结论总结内容。"))

    # ══════ 附录（可选） ══════
    story.append(Spacer(1, 8*mm))
    story.append(DividerLine())
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("附录：流程概览", S["h2"]))

    story.append(make_flow_table([
        ["①", "角色A", "步骤描述 1"],
        ["②", "角色B", "步骤描述 2"],
        ["③", "角色C", "步骤描述 3"],
    ]))

    # ══════ 构建 ══════
    doc.build(story, onFirstPage=hf, onLaterPages=hf)
    print(f"✅ PDF 已生成: {filename}")


if __name__ == "__main__":
    build_pdf()
