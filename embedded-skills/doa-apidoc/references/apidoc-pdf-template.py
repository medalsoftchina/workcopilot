# -*- coding: utf-8 -*-
"""
接口说明文档 PDF 生成模板
========================
使用方法：
  1. pip install reportlab
  2. 修改 build_pdf() 中的接口内容数据
  3. python apidoc-pdf-template.py

此模板提供完整的基础设施（字体、颜色、样式、组件），
只需替换 build_pdf() 中的实际接口数据即可生成专业 PDF。
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.flowables import Flowable
from reportlab.lib.utils import simpleSplit
import platform, os


# ══════════════════════════════════════════════
# 字体注册（跨平台自动适配）
# ══════════════════════════════════════════════
def register_fonts():
    """注册中文字体，按优先级尝试 Windows / macOS / Linux"""
    font_paths = {
        "windows": [
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
    key = {"windows": "windows", "darwin": "darwin"}.get(system, "linux")

    search_order = [key] + [k for k in font_paths if k != key]
    for k in search_order:
        for regular, bold in font_paths.get(k, []):
            try:
                pdfmetrics.registerFont(TTFont("CF", regular))
                pdfmetrics.registerFont(TTFont("CFB", bold))
                return True
            except Exception:
                continue

    print("⚠️  未找到中文字体，中文可能显示异常")
    return False

register_fonts()


# ══════════════════════════════════════════════
# 颜色体系（商务蓝主题）
# ══════════════════════════════════════════════
C = {
    "pri":    HexColor("#1A365D"),
    "sec":    HexColor("#2B6CB0"),
    "acc":    HexColor("#3182CE"),
    "lbg":    HexColor("#EBF4FF"),
    "lgray":  HexColor("#F7FAFC"),
    "border": HexColor("#CBD5E0"),
    "txt":    HexColor("#2D3748"),
    "sub":    HexColor("#718096"),
    "green":  HexColor("#276749"),
    "gbg":    HexColor("#F0FFF4"),
    "orange": HexColor("#C05621"),
    "obg":    HexColor("#FFFAF0"),
    "red":    HexColor("#C53030"),
}


# ══════════════════════════════════════════════
# 段落样式工厂
# ══════════════════════════════════════════════
def _s(name, font="CF", size=10, leading=16, color=None, align=TA_LEFT,
       sb=0, sa=0, li=0, bold=False):
    return ParagraphStyle(
        name,
        fontName="CFB" if bold else font,
        fontSize=size, leading=leading,
        textColor=color or C["txt"],
        alignment=align,
        spaceBefore=sb, spaceAfter=sa,
        leftIndent=li,
    )

S = {
    "title":    _s("title",    bold=True, size=22, leading=30, color=C["pri"], align=TA_CENTER, sa=3*mm),
    "subtitle": _s("subtitle", size=11,   leading=17, color=C["sub"], align=TA_CENTER, sa=8*mm),
    "h1":       _s("h1",       bold=True, size=15, leading=22, color=C["pri"], sb=8*mm, sa=4*mm),
    "h2":       _s("h2",       bold=True, size=13, leading=20, color=C["sec"], sb=6*mm, sa=3*mm),
    "h3":       _s("h3",       bold=True, size=11, leading=17, color=C["acc"], sb=4*mm, sa=2*mm),
    "body":     _s("body",     size=10,   leading=16, sa=2*mm, align=TA_JUSTIFY),
    "note":     _s("note",     size=9,    leading=14, color=C["sub"], li=4*mm, sa=2*mm),
    "warn":     _s("warn",     size=9.5,  leading=15, color=C["orange"], li=4*mm),
    "ok":       _s("ok",       size=9.5,  leading=15, color=C["green"], li=4*mm),
    # 表格内
    "tH":  _s("tH",  bold=True, size=9,  leading=13, color=white,   align=TA_CENTER),
    "tC":  _s("tC",  size=9,  leading=13, color=C["txt"]),
    "tCC": _s("tCC", size=9,  leading=13, color=C["txt"], align=TA_CENTER),
    "tL":  _s("tL",  bold=True, size=9,  leading=13, color=C["pri"]),
    "tR":  _s("tR",  size=9,  leading=13, color=C["txt"], align=TA_RIGHT),
}


# ══════════════════════════════════════════════
# 自定义 Flowable 组件
# ══════════════════════════════════════════════
class SectionBar(Flowable):
    """带颜色的章节标题栏（圆角色底 + 白色文字）"""
    def __init__(self, text, color=None, w=170*mm, h=9*mm):
        super().__init__()
        self.text = text
        self.color = color or C["pri"]
        self.width = w; self.height = h

    def wrap(self, aw, ah):
        return self.width, self.height + 3*mm

    def draw(self):
        c = self.canv
        c.setFillColor(self.color)
        c.roundRect(0, 0, self.width, self.height, 2*mm, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("CFB", 12)
        c.drawString(4*mm, 2.5*mm, self.text)


class InfoCard(Flowable):
    """浅蓝信息卡片（用于封面元信息展示）"""
    def __init__(self, rows, w=170*mm, rh=7.5*mm):
        super().__init__()
        self.rows = rows; self.w = w; self.rh = rh
        self.h = len(rows) * rh + 5*mm

    def wrap(self, aw, ah):
        return self.w, self.h

    def draw(self):
        c = self.canv
        c.setFillColor(C["lbg"])
        c.setStrokeColor(C["border"]); c.setLineWidth(0.5)
        c.roundRect(0, 0, self.w, self.h, 3*mm, fill=1, stroke=1)
        y = self.h - 6*mm
        for label, value in self.rows:
            c.setFont("CFB", 9.5); c.setFillColor(C["sub"])
            c.drawString(5*mm, y, label)
            c.setFont("CF", 9.5); c.setFillColor(C["txt"])
            c.drawString(32*mm, y, value)
            y -= self.rh


class Divider(Flowable):
    """分隔线"""
    def __init__(self, w=170*mm):
        super().__init__(); self.w = w
    def wrap(self, aw, ah):
        return self.w, 1*mm
    def draw(self):
        self.canv.setStrokeColor(C["border"]); self.canv.setLineWidth(0.3)
        self.canv.line(0, 0, self.w, 0)


class ColorBox(Flowable):
    """带边框的强调色块（用于调用场景说明）"""
    def __init__(self, text, bg=None, bc=None, w=170*mm, fs=10.5):
        super().__init__()
        self.text = text; self.bg = bg or C["lbg"]
        self.bc = bc or C["acc"]; self.w = w; self.fs = fs
        self.padding_x = 5 * mm
        self.padding_y = 3.5 * mm
        self.line_height = 5.5 * mm
        self.box_height = 18 * mm
        self.lines = [text]

    def wrap(self, aw, ah):
        text_width = self.w - self.padding_x * 2
        self.lines = simpleSplit(self.text, "CFB", self.fs, text_width) or [self.text]
        content_height = self.padding_y * 2 + len(self.lines) * self.line_height
        self.box_height = max(18 * mm, content_height)
        return self.w, self.box_height + 2 * mm

    def draw(self):
        c = self.canv
        c.setFillColor(self.bg); c.setStrokeColor(self.bc); c.setLineWidth(1)
        c.roundRect(0, 0, self.w, self.box_height, 2*mm, fill=1, stroke=1)
        c.setFillColor(C["pri"]); c.setFont("CFB", self.fs)
        current_y = self.box_height - self.padding_y - self.line_height + 1 * mm
        for line in self.lines:
            c.drawString(self.padding_x, current_y, line)
            current_y -= self.line_height


# ══════════════════════════════════════════════
# 表格工具函数
# ══════════════════════════════════════════════
def make_table(headers, rows, col_widths, hc=None):
    """标准数据表格（深蓝表头 + 交替行色）"""
    hc = hc or C["pri"]
    data = [[Paragraph(h, S["tH"]) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(cell), S["tCC"] if i == 0 else S["tC"]) for i, cell in enumerate(row)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    cmds = [
        ("BACKGROUND",    (0, 0), (-1, 0), hc),
        ("TEXTCOLOR",     (0, 0), (-1, 0), white),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 2.5*mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5*mm),
        ("LEFTPADDING",   (0, 0), (-1, -1), 2.5*mm),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 2.5*mm),
        ("GRID",          (0, 0), (-1, -1), 0.4, C["border"]),
    ]
    for i in range(2, len(data), 2):
        cmds.append(("BACKGROUND", (0, i), (-1, i), C["lgray"]))
    t.setStyle(TableStyle(cmds))
    return t


def make_kv_table(rows, cw=None):
    """键值表格（左列浅蓝底粗体 + 右列正文）"""
    cw = cw or [38*mm, 132*mm]
    data = [[Paragraph(str(r[0]), S["tL"]), Paragraph(str(r[1]), S["tC"])] for r in rows]
    t = Table(data, colWidths=cw)
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (0, -1), C["lbg"]),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",   (0, 0), (-1, -1), 2.5*mm),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 2.5*mm),
        ("LEFTPADDING",  (0, 0), (-1, -1), 3*mm),
        ("GRID",         (0, 0), (-1, -1), 0.3, C["border"]),
    ]))
    return t


def code_block(text):
    """代码块（浅灰底 + 蓝色等宽字体）"""
    lines = text.strip().split("\n")
    data = [[Paragraph(
        line.replace(" ", "&nbsp;").replace("<", "&lt;").replace(">", "&gt;"),
        _s("_cb", size=7.8, leading=11.5, color=C["sec"])
    )] for line in lines]
    t = Table(data, colWidths=[166*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), HexColor("#F8F9FA")),
        ("TOPPADDING",   (0, 0), (-1, -1), 0.8*mm),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 0.8*mm),
        ("LEFTPADDING",  (0, 0), (-1, -1), 3*mm),
        ("BOX",          (0, 0), (-1, -1), 0.5, C["border"]),
    ]))
    return t


# ══════════════════════════════════════════════
# 页眉页脚工厂
# ══════════════════════════════════════════════
def make_header_footer(header_left, header_right="CONFIDENTIAL 机密",
                       footer_left="公司名称", footer_right_tpl="第 {page} 页"):
    """创建页眉页脚回调函数"""
    def _hf(canvas, doc):
        canvas.saveState()
        w, h = A4
        # 页眉
        canvas.setStrokeColor(C["pri"]); canvas.setLineWidth(2)
        canvas.line(20*mm, h - 12*mm, w - 20*mm, h - 12*mm)
        canvas.setFont("CF", 7.5); canvas.setFillColor(C["sub"])
        canvas.drawString(20*mm, h - 11*mm, header_left)
        if header_right:
            canvas.drawRightString(w - 20*mm, h - 11*mm, header_right)
        # 页脚
        canvas.setStrokeColor(C["border"]); canvas.setLineWidth(0.5)
        canvas.line(20*mm, 14*mm, w - 20*mm, 14*mm)
        canvas.setFont("CF", 8); canvas.setFillColor(C["sub"])
        canvas.drawString(20*mm, 9*mm, footer_left)
        canvas.drawRightString(w - 20*mm, 9*mm, footer_right_tpl.format(page=doc.page))
        canvas.restoreState()
    return _hf


# ══════════════════════════════════════════════
# 构建 PDF（示例：替换为实际接口内容）
# ══════════════════════════════════════════════
def build_pdf():
    # ── 配置区 ──
    filename = "接口说明文档.pdf"
    hf = make_header_footer(
        header_left="项目名 · 接口说明文档",
        footer_left="公司名称",
    )

    doc = SimpleDocTemplate(
        filename, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=18*mm, bottomMargin=20*mm,
    )

    F = []

    # ══════ 封面 ══════
    F.append(Spacer(1, 22*mm))
    F.append(Paragraph("接 口 说 明 文 档", S["title"]))
    F.append(Paragraph("项目名 — API Interface Specification", S["subtitle"]))
    F.append(InfoCard([
        ("文档版本:",  "V1.0"),
        ("编制方:",   "XXXXXX"),
        ("接收方:",   "XXXXXX"),
        ("编制日期:",  "XXXX-XX-XX"),
        ("文档状态:",  "初版发布"),
    ]))
    F.append(Spacer(1, 6*mm))
    F.append(Divider())

    # ══════ 一、接口总览 ══════
    F.append(SectionBar("一、接口总览"))
    F.append(Spacer(1, 3*mm))

    F.append(Paragraph("1.1 接口清单", S["h3"]))
    F.append(make_table(
        ["#", "接口名称", "Method", "Path", "描述"],
        [
            ["1", "示例接口", "GET", "/v1/example", "示例描述"],
        ],
        [8*mm, 26*mm, 14*mm, 64*mm, 54*mm],
    ))

    F.append(Paragraph("1.2 调用链路", S["h3"]))
    F.append(code_block(
"""Client                          Server
  │                                │
  │  ① GET /v1/example             │
  │────────────────────────────────▶│
  │◀────────────────────────────────│
  │  {data: ...}                    │"""
    ))

    # ══════ 二、公共约定 ══════
    F.append(SectionBar("二、公共约定"))
    F.append(Spacer(1, 3*mm))

    F.append(Paragraph("2.1 基础信息", S["h3"]))
    F.append(make_kv_table([
        ["协议",     "HTTPS"],
        ["Base URL", "https://api.example.com/v1"],
        ["鉴权方式",  "Bearer Token"],
        ["数据格式",  "JSON（Content-Type: application/json; charset=utf-8）"],
    ]))

    F.append(Paragraph("2.2 公共响应结构", S["h3"]))
    F.append(code_block(
"""{
  "code":      200,
  "message":   "success",
  "data":      { ... },
  "timestamp": "2025-01-01T00:00:00+08:00"
}"""
    ))

    F.append(Paragraph("2.3 错误码", S["h3"]))
    F.append(make_table(
        ["code", "含义", "说明"],
        [
            ["200", "成功",        "请求处理成功"],
            ["400", "参数错误",     "请求参数缺失或格式非法"],
            ["401", "认证失败",     "Token 无效或过期"],
            ["404", "资源不存在",   "请求的资源不存在"],
            ["500", "服务内部错误", "服务端内部异常"],
        ],
        [18*mm, 30*mm, 118*mm],
    ))

    # ══════ 三、接口详细定义 ══════
    F.append(PageBreak())
    F.append(SectionBar("三、接口详细定义"))
    F.append(Spacer(1, 3*mm))

    # 接口 1 示例
    F.append(Paragraph("3.1  GET /v1/example — 示例接口", S["h2"]))
    F.append(ColorBox("调用场景：示例调用场景说明。"))
    F.append(Spacer(1, 2*mm))

    F.append(Paragraph("<b>入参（Query Parameter）</b>", S["h3"]))
    F.append(make_table(
        ["参数", "类型", "必填", "说明"],
        [
            ["id", "string", "✅", "资源唯一标识"],
        ],
        [30*mm, 16*mm, 12*mm, 108*mm],
    ))

    F.append(Paragraph("<b>出参（Response data）</b>", S["h3"]))
    F.append(make_table(
        ["参数", "类型", "说明"],
        [
            ["id",   "string", "资源ID"],
            ["name", "string", "资源名称"],
        ],
        [30*mm, 18*mm, 118*mm],
    ))

    F.append(Paragraph("<b>出参示例</b>", S["h3"]))
    F.append(code_block(
"""{
  "code": 200,
  "message": "success",
  "data": {
    "id": "RES-001",
    "name": "示例资源"
  }
}"""
    ))

    # ══════ 四、调用时序总结 ══════
    F.append(Spacer(1, 6*mm))
    F.append(SectionBar("四、调用时序总结"))
    F.append(Spacer(1, 3*mm))

    F.append(make_table(
        ["步骤", "调用方", "接口", "触发条件", "备注"],
        [
            ["1", "Client → Server", "GET /v1/example", "用户触发", "返回资源详情"],
        ],
        [12*mm, 24*mm, 52*mm, 38*mm, 40*mm],
    ))

    # ══════ 生成 ══════
    doc.build(F, onFirstPage=hf, onLaterPages=hf)
    print(f"✅ PDF 已生成: {filename}")


if __name__ == "__main__":
    build_pdf()
