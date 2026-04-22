import math
import re
from datetime import datetime

import pandas as pd
import xlsxwriter

from sst.strategy2.logic.docs.excel_convert import ExcelConvert


class ColorMap:
    # 常用填充颜色
    FillTan = '#FDE9D9'
    FillBlue = '#0070C0'
    FillGreen = '#00B050'
    FillGrey = '#D9D9D9'
    # 常用字体颜色
    White = '#FFFFFF'
    Black = '#000000'
    # 数据条颜色
    DataYellow = '#FFB628'
    DataGreen = '#63C384'
    DataBlue = '#638EC6'
    DataBlue2 = '#008AEF'
    # 3色阶颜色
    Color3Red = '#F8696B'
    Color3Yellow = '#FFEB84'
    Color3Green = '#63BE7B'


class NumerFmt:
    # 字符串文本
    text = '@'
    # 百分比
    pct0 = '0.0%'
    # 百分比: 保留两位小数
    pct00 = '0.00%'
    # 整数
    num = '0'
    # 浮点数
    fnum = '0.00'
    # 时间格式
    dtime = 'yyyy-mm-dd hh:mm:ss'


class AlignPosition:
    left = 'left'
    center = 'center'
    right = 'right'
    justify = 'justify'
    center_across = 'center_across'
    distributed = 'distributed'


class VAlignPosition:
    top = 'top'
    vcenter = 'vcenter'
    bottom = 'bottom'
    vjustify = 'vjustify'
    vdistributed = 'vdistributed'


class ConditionFmt:
    Color3 = 'color3'
    Color3R = 'color3r'
    DataBar = 'databar'


class ExcelBaseWriter:
    SHEET_COLUMN_WIDTH = 8.47
    SHEET_ROW_HEIGHT = 13.5

    def __init__(self, filename, default_sheet_name='Sheet1'):
        self.filename = filename
        self.workbook = xlsxwriter.Workbook(filename)
        # 存储所有创建的sheet，sheet_name:sheet
        self.sheets = {}
        # 记录初始写入位置
        self.col_idx = 0
        self.row_idx = 1
        self.active_sheet = self.add_sheet(default_sheet_name)
        # ==================文本常用格式================
        # 14-黑-粗-左-白底-无框-字符
        self.fmt_title1 = self.get_format(align=AlignPosition.left, bold=True, size=14, border=0)
        # 10-黑-粗-左-白底-无框-字符
        self.fmt_title2 = self.get_format(align=AlignPosition.left, bold=True, border=0)
        # 10-黑-细-左-白底-无框-字符
        self.fmt_text = self.get_format(align=AlignPosition.left, border=0)
        # 10-黑-细-左-白底-无框-时间
        self.fmt_time = self.get_format(align=AlignPosition.left, num_format=NumerFmt.dtime, border=0)
        # 10-黑-细-右-白底-无框-整数
        self.fmt_num = self.get_format(align=AlignPosition.right, num_format=NumerFmt.num, border=0)
        # 10-黑-细-右-白底-无框-浮点数
        self.fmt_fnum = self.get_format(align=AlignPosition.right, num_format=NumerFmt.fnum, border=0)
        # 10-黑-细-右-白底-无框-百分比
        self.fmt_pct = self.get_format(align=AlignPosition.right, num_format=NumerFmt.pct0, border=0)
        # ==================df常用格式和预设================
        # 10-白-粗-中-蓝底-细框-字符
        self.fmt_df_title1 = self.get_format(color=ColorMap.White, bold=True, fill=ColorMap.FillBlue)
        # 10-白-粗-中-绿底-细框-字符
        self.fmt_df_title2 = self.get_format(color=ColorMap.White, bold=True, fill=ColorMap.FillGreen)
        # 10-黑-粗-中-蛋黄底-细框-字符
        self.fmt_df_title3 = self.get_format(bold=True, fill=ColorMap.FillTan, align=AlignPosition.left)
        # 10-黑-细-中-白底-细框-字符
        self.fmt_df_text1 = self.get_format()
        # 10-黑-细-中-白底-细框-字符-换行
        self.fmt_df_text2 = self.get_format(text_wrap=True)
        # 10-黑-细-中白底-细框-整数
        self.fmt_df_num = self.get_format(num_format=NumerFmt.num)
        # 10-黑-细-中-白底-细框-浮点数
        self.fmt_df_fnum = self.get_format(num_format=NumerFmt.fnum)
        # 10-黑-细-中-白底-细框-百分比
        self.fmt_df_pct = self.get_format(num_format=NumerFmt.pct0)
        # 10-黑-细-中-白底-细框-时间
        self.fmt_df_time = self.get_format(num_format=NumerFmt.dtime)

    def close(self, to_img=False):
        self.workbook.close()
        print("成功保存:", self.filename)
        if to_img:
            img_path = ExcelConvert.excel_2_img(self.filename)
            print("成功转化图片:", img_path)

    # 在工作簿中创建一个sheet
    def add_sheet(self, name=None, hide_gridlines=True):
        worksheet = self.workbook.add_worksheet(name)
        # 1.设置整体列宽为8.47，行高不用设置用默认的13.5即可
        worksheet.set_column(0, 16383, self.SHEET_COLUMN_WIDTH)
        # 2.设置第一列的列宽为2.87
        worksheet.set_column(0 ,0, 2.87)
        # 3.存储到字典
        self.sheets[worksheet.name] = worksheet
        # 4.设置网格
        if hide_gridlines:
            worksheet.hide_gridlines(2)
        return worksheet

    # 获取某个已经创建的sheet
    def get_sheet(self, name=None):
        if name is None:
            return self.active_sheet
        elif isinstance(name, str):
            return self.sheets[name]
        return name

    # 设置某个sheet为当前工作sheet，不存在就创建一个
    def set_active_sheet(self, name=None):
        if name in self.sheets:
            self.active_sheet = self.sheets[name]
        else:
            self.active_sheet = self.add_sheet(name)
        self.col_idx = 0
        self.row_idx = 1
        print("当前active_sheet为：", name)

    # 获取行高:被设置过的存储在row_sizes字典中，没设置过是默认行高
    def get_row_height(self, row):
        if row in self.active_sheet.row_sizes:
            return self.active_sheet.row_sizes[row][0]
        return self.SHEET_ROW_HEIGHT

    # 条件格式：设置数据条
    def set_databar_format(self, *cells, color=ColorMap.DataBlue):
        # excel2007格式
        # min_type
        # max_type
        # min_value
        # max_value
        # bar_color
        # bar_only
        # excel2010额外格式
        # bar_solid
        # bar_negative_color
        # bar_border_color
        # bar_negative_border_color
        # bar_negative_color_same
        # bar_negative_border_color_same
        # bar_no_border
        # bar_direction
        # bar_axis_position
        # bar_axis_color
        # data_bar_2010
        self.active_sheet.conditional_format(*cells, {'type': 'data_bar', 'data_bar_2010': True, 'bar_color': color})


    # 条件格式：设置3色阶格式，红黄绿
    def set_3color_format(self, *cells, min_type='min', mid_type='percent', max_type='max', min_value=None, mid_value=50,
                          max_value=None, min_color=ColorMap.Color3Red, mid_color=ColorMap.Color3Yellow,
                          max_color=ColorMap.Color3Green):
        self.active_sheet.conditional_format(*cells, {'type': '3_color_scale', 'min_type': min_type, 'mid_type': mid_type, 'max_type': max_type,
                                             'min_value': min_value, 'mid_value': mid_value, 'max_value': max_value,
                                             'min_color': min_color, 'mid_color': mid_color, 'max_color': max_color})

    # 条件格式：设置3色阶格式，绿黄红
    def set_3color_format_reverse(self, *cells):
        return self.set_3color_format(*cells, min_color=ColorMap.Color3Green, max_color=ColorMap.Color3Red)


    # 获取单元格格式
    def get_format(self, color=ColorMap.Black, bold=False, size=10, indent=0, text_wrap=False, align=AlignPosition.center,
                   valign=VAlignPosition.vcenter, border=1, fill=ColorMap.White, num_format=NumerFmt.text):
        cell_format = self.workbook.add_format()
        # 设置字体
        cell_format.set_font_name('微软雅黑')
        # 字体大小
        cell_format.set_font_size(size)
        # 字体颜色
        cell_format.set_font_color(color)
        # 字体加粗
        cell_format.set_bold(bold)
        # 设置缩进
        cell_format.set_indent(indent)
        # 设置文字自动换行(根据列宽)
        cell_format.set_text_wrap(text_wrap)
        # 设置水平居中
        cell_format.set_align(align)
        # 设置垂直居中
        cell_format.set_align(valign)
        # 设置边框
        cell_format.set_border(border)
        # 设置背景填充
        cell_format.set_bg_color(fill)
        # 设置值格式, 百分比为：'0.00%'
        cell_format.set_num_format(num_format)
        return cell_format


class ExcelDocWriter(ExcelBaseWriter):
    # 当一个单元格内容太多，水平方向最多合并的单元格个数
    MAX_MERGE_CELL_CNT = 6
    # 单行最大拉伸倍数(相对于默认行高), 文本多行时拉伸(行数+1)倍
    MAX_ROW_GROW_RATE = 6
    # 百分比判断正则
    PCT_REGEX = r"^-?\d+[\\.\d]*%$"

    # 判断是否是百分比字符串
    @classmethod
    def value_is_pct(cls, value):
        return isinstance(value, str) and bool(re.search(cls.PCT_REGEX, value))

    @classmethod
    def values_is_pct(cls, values):
        is_pct = True
        try:
            for value in values:
                # None 跳过
                if pd.isnull(value):
                    continue
                # 非百分比数值
                elif not(isinstance(value, str) and bool(re.search(cls.PCT_REGEX, value))):
                    is_pct = False
                    break
        except Exception as e:
            print(e)
            is_pct = False
        return is_pct

    # 判断是否是空值
    @classmethod
    def value_is_none(cls, value):
        return pd.isna(value)

    # 百分比字符串转化浮点小数
    @classmethod
    def pct_str_2_float(cls, value):
        try:
            return float(value[:-1]) / 100
        except:
            return None

    # 转换python int对象
    @classmethod
    def int_2_pyint(cls, value):
        try:
            return int(value)
        except:
            return None

    # 转换python float对象
    @classmethod
    def float_2_pyfloat(cls, value):
        try:
            if pd.isna(value):
                return None
            return float(value)
        except:
            return None

    # 转换python datetime对象
    @classmethod
    def time_2_pydatetime(cls, value):
        try:
            return pd.Timestamp(value).to_pydatetime()
        except:
            return None

    # 把序列中相邻相等的值:合并计数
    @classmethod
    def sorted_value_cnt(cls, values):
        values = list(values)
        if len(values) == 0:
            return []
        res = [[values[0], 1]]
        for value in values[1:]:
            if res[-1][0] == value:
                res[-1][1] += 1
            else:
                res.append([value, 1])
        return res

    @classmethod
    def calculate_text_width_yahei(cls, text, font_size=0):
        """
        计算微软雅黑字体下文本在 Excel 中的宽度
        :param text: 文本内容
        :param font_size: 字体大小，默认为 11
        :return: 文本宽度（Excel 列宽单位）
        """
        # 定义字符宽度映射（基于微软雅黑字体）
        char_widths = {
            'default': 1,  # 默认英文字符宽度
            'wide_chars': {'W': 1.3, 'M': 1.3},  # 宽字符
            'narrow_chars': {'i': 0.7, 'l': 0.7, ' ': 0.5},  # 窄字符
            'chinese_char': 2.0  # 中文字符宽度
        }
        # 计算文本宽度
        total_width = 0
        for char in text:
            if '\u4e00' <= char <= '\u9fff':  # 判断是否为中文字符
                total_width += char_widths['chinese_char']
            elif char in char_widths['wide_chars']:
                total_width += char_widths['wide_chars'][char]
            elif char in char_widths['narrow_chars']:
                total_width += char_widths['narrow_chars'][char]
            else:
                total_width += char_widths['default']

        # 根据字体大小调整宽度
        width_scale = font_size / 11  # 默认字体大小为 11
        total_width *= width_scale
        return total_width

    def __init__(self, filename, max_merge_cell_cnt=None, max_row_grow_rate=None, row_grow_add=1, default_sheet_name='Sheet1'):
        super().__init__(filename, default_sheet_name=default_sheet_name)
        # 配置
        # 配置单元格内容换行时，纵向行高最大拉伸倍数
        self.max_row_grow_rate = max_row_grow_rate or self.MAX_ROW_GROW_RATE
        # 配置单元格内容换行时，纵向拉升后追加的行高
        self.row_grow_add = row_grow_add
        # 3.数据条数据条颜色自增id，用于设置相邻数据条颜色不同
        self.data_bar_idx = 0
        # 4.记录数据色阶位置矩形。每个矩形有两个坐标，左上点，右下点。
        self.data_color_scale = []
        # ==================df常用预设=================
        # 基础预设
        self.fmt_df = {
            "blue_title": self.fmt_df_title1,
            "green_title": self.fmt_df_title2,
            "num_value": self.fmt_df_num,
            "fnum_value": self.fmt_df_fnum,
            "pct_value": self.fmt_df_pct,
            "time_value": self.fmt_df_time,
            "databar_cols": [],
            # 写索引
            "write_index": True,
            # df写完后：row和col需要空的行和列数
            "finish_wrap": 1,
            # 配置单元格内容过长时，横向最大可合并的单元格数
            "max_merge_cell_cnt": max_merge_cell_cnt or self.MAX_MERGE_CELL_CNT,
            # 索引列合并单元格数
            "index_merge_cell_cnt": None

        }
        # 1.字符串右对齐, 百分比列使用数据条
        self.fmt_df1 = {
            **self.fmt_df,
            "text_value": self.fmt_df_text1,
            "condition_fmt": ConditionFmt.DataBar
        }
        # 2.字符串右对齐, 百分比列使用色阶3
        self.fmt_df2 = {
            **self.fmt_df,
            "text_value": self.fmt_df_text1,
            "condition_fmt": ConditionFmt.Color3
        }
        # 3.字符串右对齐, 百分比列使用色阶3
        self.fmt_df3 = {
            **self.fmt_df,
            "text_value": self.fmt_df_text1,
            "condition_fmt": ConditionFmt.Color3R
        }
        # 4.字符串居中对齐换行, 百分比列使用数据条
        self.fmt_df4 = {
            **self.fmt_df,
            "text_value": self.fmt_df_text2,
            "condition_fmt": ConditionFmt.DataBar
        }
        # 5.不使用百分比列
        self.fmt_df5 = {
            **self.fmt_df,
            "text_value": self.fmt_df_text1,
            "condition_fmt": None
        }

    # 重置索引
    def set_active_sheet(self, name=None):
        super().set_active_sheet(name)

    # 根据写入内容类型返回：数据，格式，是否df
    def get_fmt(self, item):
        """
        :param item: 数据 或者 (数据，格式)。 (1)当只有数据时：根据数据类型自动选择格式 (2)当为元组时，使用元组第二个元素来指定格式
        """
        if not isinstance(item, tuple):
            data = item
            is_df = isinstance(data, pd.DataFrame)
            if is_df:
                fmt = self.fmt_df1
            else:
                # 空数据时，写入None,显示上相当于跳过次单元格
                if self.value_is_none(item):
                    data = None
                    fmt = self.fmt_text
                # 处理百分比的字符串：右起的百分比
                elif self.value_is_pct(item):
                    data = self.pct_str_2_float(data)
                    fmt = self.fmt_pct
                # 整数使用 右起的数值
                elif isinstance(data, int):
                    fmt = self.fmt_num
                # float使用 右起的float
                elif isinstance(data, float):
                    fmt = self.fmt_fnum
                # float使用 左起的时间字符串
                elif isinstance(data, datetime):
                    fmt = self.fmt_time
                # 普通文本: 左起
                else:
                    data = str(data)
                    fmt = self.fmt_text
        else:
            assert len(item) == 2, "目前只支持长度为2的tuple"
            data, fmt = item
            is_df = isinstance(data, pd.DataFrame)
            if isinstance(fmt, str):
                fmt = getattr(self, 'fmt_' + fmt)
        if not (isinstance(data, (pd.DataFrame, int, float, str)) or data is None):
            raise Exception("只支持写入pd.DataFrame, int, float, str, None等数据类型...")
        return data, fmt, is_df

    # 获取df某列的值序列和数据类型
    def get_df_series_fmt(self, s, fmt_dict, is_index=False):
        dtype = str(s.dtype)
        if s.shape[0] == 0:
            return [], fmt_dict['text_value']
        # 复合类型：interval([float, right])
        elif ',' in dtype:
            data = [str(v) for v in s]
            return data, fmt_dict['text_value']
        elif 'int' in dtype:
            data = [self.int_2_pyint(v) for v in s]
            return data, fmt_dict['num_value']
        elif 'float' in dtype:
            data = [self.float_2_pyfloat(v) for v in s]
            return data, fmt_dict['fnum_value']
        elif 'time' in dtype.lower():
            data = [self.time_2_pydatetime(v) for v in s]
            return data, fmt_dict['time_value']
        elif 'object' == dtype:
            if (not is_index) and self.values_is_pct(s):
                data = [self.pct_str_2_float(v) for v in s]
                return data, fmt_dict['pct_value']
            else:
                data = [str(v) for v in s]
                return data, fmt_dict['text_value']
        else:
            data = [str(v) for v in s]
            return data, fmt_dict['text_value']

    # 获取该序列写入excel时，需要占的横向单元格个数(即需要合并几个单元格)
    def get_cell_cnt_flat(self, values, fmt_dict, font_size=10):
        cell_cnt_lst = []
        for value in values:
            if isinstance(value, str):
                # 判断文本相当于多少个11原文的标准字符大小，自动适配中文/英文
                text_len = self.calculate_text_width_yahei(value, font_size=font_size)
                # 获取文本长度占几个单元格
                cell_cnt_lst.append(math.ceil(text_len/self.SHEET_COLUMN_WIDTH))
            # 时间类型默认占两个单元格
            elif isinstance(value, datetime):
                cell_cnt_lst.append(3)
            # 其他类型默认占一个
            else:
                cell_cnt_lst.append(1)
        # 默认占最多6个单元格
        return min(max(cell_cnt_lst), fmt_dict['max_merge_cell_cnt'])

    # 按顺序获取数据条颜色，每次获取的颜色都不同
    def get_databar_color(self):
        colors = [ColorMap.DataBlue, ColorMap.DataGreen, ColorMap.DataYellow]
        color = colors[self.data_bar_idx%len(colors)]
        self.data_bar_idx += 1
        return color

    # 给某列写入条件格式
    def write_df_condition_fmt(self, values, fmt_dict, cell_cnt_flat, index, column_name):
        """
        :param values: 序列所有值的列表
        :param fmt_dict: 格式配置字典
        :param cell_cnt_flat: 当前序列所合并的单元格数
        :param index: df的索引值，最后一个值为`合计`时不应用条件格式
        :param column_name: 当前列名
        """
        last_value_row = self.row_idx + len(values) - 1
        last_value_col = self.col_idx + cell_cnt_flat - 1
        # 最后一行索引若为合计，不写入数据条|色阶
        if values and index[-1] == '合计':
            last_value_row = last_value_row - 1
        # 1.写指定列的数据条
        if column_name in fmt_dict['databar_cols']:
            color = ColorMap.DataBlue2 if '合计' in column_name else self.get_databar_color()
            self.set_databar_format(self.row_idx, self.col_idx, last_value_row, last_value_col, color=color)
        # 2.写数据条：数据条不涉及跨列
        elif fmt_dict['condition_fmt'] == ConditionFmt.DataBar:
            self.set_databar_format(self.row_idx, self.col_idx, last_value_row, last_value_col, color=self.get_databar_color())
        # 2.写色阶，因为涉及跨列，先记录位置，最后才写
        elif fmt_dict['condition_fmt'] in [ConditionFmt.Color3, ConditionFmt.Color3R]:
            position = [self.row_idx, self.col_idx, last_value_row, last_value_col]
            if self.data_color_scale:
                pre_position = self.data_color_scale[-1]
                scale_start_row, scale_start_col, scale_end_row, scale_end_col = pre_position[0], pre_position[1], pre_position[2], pre_position[3]
                # 判断色阶条可否合并一起
                if (scale_start_row==self.row_idx) and (scale_end_row == last_value_row) and (scale_end_col+1 == last_value_col):
                    self.data_color_scale[-1] = [scale_start_row, scale_start_col, last_value_row, last_value_col]
                else:
                    self.data_color_scale.append(position)
            else:
                self.data_color_scale.append(position)

    # 给多列写入条件格式：色阶
    def write_df_condition_fmt_multi(self, fmt_dict):
        for position in self.data_color_scale:
            if fmt_dict['condition_fmt'] == ConditionFmt.Color3:
                self.set_3color_format(*position)
            elif fmt_dict['condition_fmt'] == ConditionFmt.Color3R:
                self.set_3color_format_reverse(*position)

    # 写入值到单元格，或者合并单元格写入，根据文本是否换行来放大行高
    def write_value(self, row_start, col_start, value, fmt, row_end=None, col_end=None):
        # 1.写入到单元格
        if row_end is None or (row_start==row_end and col_start==col_end):
            self.active_sheet.write(row_start, col_start, value, fmt)
        # 2.合并单元格写入
        else:
            self.active_sheet.merge_range(row_start, col_start, row_end, col_end, value, fmt)
        # 3.当fmt设置了自动换行，value为字符串，竖直方向没有合并单元格时。自动放大行高，最大6倍
        if fmt.text_wrap and isinstance(value, str) and row_start == row_end:
            # 换行符行数
            sep_line_cnt = value.count('\n')+1
            # 当前写入位置合并的单元格数
            cell_cnt_flat = col_end - col_start + 1
            # 获取文本一共所需的单元格
            need_cell_cnt = self.calculate_text_width_yahei(value, font_size=fmt.font_size)/self.SHEET_COLUMN_WIDTH
            # 自动换行行数
            auto_line_cnt = math.ceil(need_cell_cnt/cell_cnt_flat)
            # 实际行放大倍数：max(换行符行数,自动换行行数)+self.row_grow_add， +self.row_grow_add是为了美观
            grow_rate = max(sep_line_cnt, auto_line_cnt) + self.row_grow_add
            # 最大行放大倍数不超过：MAX_ROW_LINE_CNT
            grow_rate = min(grow_rate, self.max_row_grow_rate)
            grow_height = self.SHEET_ROW_HEIGHT*grow_rate
            # 对当前行进行进行行高拉伸，禁止收缩
            if self.get_row_height(row_start) < grow_height:
                self.active_sheet.set_row(row_start, grow_height)

    # 写dataframe的索引：写完后 游标移动到索引右上角的右一格
    def write_df_index(self, df, fmt_dict, col_level, start_row_idx):
        # 1.获取索引层数和索引名
        idx_level = df.index.nlevels
        idx_names = [str(name) for name in df.index.names]
        # 2.写索引
        for level in range(idx_level):
            idx_name = idx_names[level]
            # 2.1 获取索引格式化后的值，和对应列格式
            values, value_fmt = self.get_df_series_fmt(df.index.get_level_values(level), fmt_dict, is_index=True)
            # 2.2 索引列所占横向单元格个数
            cell_cnt_flat = fmt_dict.get('index_merge_cell_cnt')
            if not cell_cnt_flat:
                cell_cnt_flat = self.get_cell_cnt_flat([str(idx_name), *values], fmt_dict, font_size=value_fmt.font_size)
            # 2.3 写入索引表头：需要在行/列方向进行单元格合并。内容超出会在行方向合并，有多层col时会在列方向合并
            self.write_value(self.row_idx, self.col_idx, idx_name, fmt_dict['blue_title'], self.row_idx+col_level-1, self.col_idx+cell_cnt_flat-1)
            self.row_idx += col_level
            # 2.4 写入具体索引值：需要在行/列方向进行单元格合并。承接上面的行合并，相同索引值在列方向合并。
            for value, cnt in self.sorted_value_cnt(values):
                self.write_value(self.row_idx, self.col_idx, value, value_fmt, self.row_idx+cnt-1, self.col_idx + cell_cnt_flat - 1)
                self.row_idx += cnt
            # 2.5 游标切换： 移动到索引右上角的右一格，为写col和value做准备
            self.row_idx = start_row_idx
            self.col_idx += cell_cnt_flat

    # 写dataframe的columns和value: 写完后 游标移动到DataFrame右上角的右二格
    def write_df_value(self, df, fmt_dict, col_level):
        # 记录开始写df表头游标位置
        start_row_idx, start_columns_col_idx = self.row_idx, self.col_idx
        self.row_idx = start_row_idx + col_level-1
        columns_col_list = []
        for column_name, series in df.items():
            columns_col_list.append(self.col_idx)
            # 最内层的索引名
            lst_column_name = column_name[-1] if isinstance(column_name, tuple) else column_name
            # 获取该列的值序列和对应格式
            values, value_fmt = self.get_df_series_fmt(series.values, fmt_dict, is_index=False)
            # 获取最内层索引和当前列值所需要合并的单元格个数
            cell_cnt_flat = self.get_cell_cnt_flat([str(lst_column_name), *values], fmt_dict, font_size=value_fmt.font_size)
            # 写最内层表头: 必须字符串
            self.write_value(self.row_idx, self.col_idx, str(lst_column_name), fmt_dict['blue_title'], self.row_idx, self.col_idx+cell_cnt_flat-1)
            self.row_idx += 1
            # 给百分格式的列写入条件格式
            if values and value_fmt is self.fmt_df_pct:
                self.write_df_condition_fmt(values, fmt_dict, cell_cnt_flat, df.index, column_name)
            # 写入value
            for value in values:
                self.write_value(self.row_idx, self.col_idx, value, value_fmt, self.row_idx, self.col_idx + cell_cnt_flat - 1)
                self.row_idx += 1
            # 切换游标位置
            self.row_idx = (start_row_idx + col_level-1)
            self.col_idx += cell_cnt_flat
        # 写入跨列的色阶格式
        self.write_df_condition_fmt_multi(fmt_dict)
        # 记录最后一列的终止位置
        columns_col_list.append(self.col_idx)

        # 写外层的columns
        # 需要在合并单元格的列上再次考虑合并单元格
        if col_level > 1:
            self.row_idx, self.col_idx = start_row_idx, start_columns_col_idx
            for level in range(col_level-1):
                idx_values = df.columns.get_level_values(level)
                cnt_sum = 0
                for value, cnt in self.sorted_value_cnt(idx_values):
                    cnt_sum += cnt
                    self.write_value(self.row_idx, self.col_idx, str(value), fmt_dict['blue_title'], self.row_idx, columns_col_list[cnt_sum]-1)
                    self.col_idx = columns_col_list[cnt_sum]
                self.row_idx += 1
                self.col_idx = start_columns_col_idx

        # 移动游标位置： 游标移动到DataFrame右上角的右二格
        self.col_idx = columns_col_list[-1] + fmt_dict['finish_wrap']
        self.row_idx = start_row_idx

    # 写dataframe
    # flat=False 竖直方向写df： 写完游标row_idx移动到df下下一行，col_idx置零
    # flat=Ture 水平方向写df： 写完游标移动col_idx到df下下一列, row_idx等于df的第一行
    # 无论横向写还是竖直写，都返回下下一行的row_idx
    def write_df(self, df, fmt_dict, flat=False):
        """
        :param df: DataFrame
        :param fmt_dict: 格式字典，参考self.fmt_df
        :param flat: True右移，False下移动
        """
        if df.shape[0] == 0:
            print("当前dataframe数据为空，跳过写入。。。")
            return self.row_idx
        if  self.col_idx == 0:
            self.col_idx = 1
        # 0.重置df数据条开始颜色,色阶条位置
        self.data_bar_idx = 0
        self.data_color_scale.clear()
        # 1.记录开始时的游标位置
        start_row_idx, start_col_idx = self.row_idx, self.col_idx
        # 2.获取df的columns层数
        col_level = df.columns.nlevels
        # 3.写索引
        if fmt_dict['write_index']:
            self.write_df_index(df, fmt_dict, col_level, start_row_idx)
        # 4.写最内层columns和值
        self.write_df_value(df, fmt_dict, col_level)
        # 5.游标移动到下一个需要写的位置
        bottom_row_idx = start_row_idx + df.shape[0] + col_level + fmt_dict['finish_wrap']
        if flat:
            # 游标不下移置零
            pass
        else:
            self.col_idx = 0
            self.row_idx = bottom_row_idx
        return bottom_row_idx

    # 写单元格
    # flat=False 竖直方向写单元格： 写完后游标row_idx移动到下一行，col_idx置零
    # flat=Ture 水平方向写单元格： 写完后游标col_idx右移到下一列, row_idx不动
    # 无论横向写还是竖直写，都返回下一行的row_idx
    def write_cell(self, data, fmt, flat=False):
        """
        :param data: 数据
        :param fmt: 格式
        :param flat: True右移，False下移动
        """
        # 标题1从第二列开始写
        if fmt is self.fmt_title1 and self.col_idx == 0:
            self.col_idx = 1
        self.write_value(self.row_idx, self.col_idx, data, fmt)
        # 写完后游标col_idx右移到下一列, row_idx不动
        self.col_idx += 1
        if flat:
            # 游标不下移置零
            pass
        else:
            self.row_idx += 1
            self.col_idx = 0
        return self.row_idx+1

    # 水平方向写内容 内容写完后:
    # row_idx: 移动到竖直内容最高列的下一行
    # col_idx: 置零
    def write_row_items(self, items):
        # 用于记录 这一行内容中 最底下的row_idx
        end_row_idx = self.row_idx
        for item in items:
            data, fmt, is_df = self.get_fmt(item)
            if is_df:
                below_row_idx = self.write_df(data, fmt, flat=True)
            else:
                below_row_idx = self.write_cell(data, fmt, flat=True)
            if below_row_idx > end_row_idx:
                end_row_idx = below_row_idx
        self.row_idx = end_row_idx
        self.col_idx = 0

    # 写内容到excel中
    # 垂直方向写内容 内容写完后:
    # row_idx: 自动移动游标到内容下一行
    # col_idx: 置零
    def write_items(self, items):
        for item in items:
            if not isinstance(item, list):
                data, fmt, is_df = self.get_fmt(item)
                if is_df:
                    self.write_df(data, fmt, flat=False)
                else:
                    self.write_cell(data, fmt, flat=False)
            else:
                self.write_row_items(item)

    @classmethod
    def save(cls, items, filename=None, to_img=False, max_merge_cell_cnt=None, max_row_grow_rate=None, row_grow_add=1):
        """
        :param items: 内容列表, 比如[("【标题1】", 'title1'), ("  1.标题2", 'title2')]
        :param filename: excel存储的文件名，不传使用当前时间命名
        :param to_img: True|False, 默认False。是否追加返回excel的图片
        :param max_merge_cell_cnt
        :param max_row_grow_rate
        :param row_grow_add
        """
        if filename is None:
            filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.xlsx'
        obj = cls(filename, max_merge_cell_cnt=max_merge_cell_cnt, max_row_grow_rate=max_row_grow_rate, row_grow_add=row_grow_add)
        obj.write_items(items)
        obj.close(to_img=to_img)
