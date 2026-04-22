import os

import fitz
import requests


class ExcelConvert:
    url = 'https://strategy.starshinetechs.com/xlsx2img/api/v1/upload_file'

    @classmethod
    def _write_to_sheet(cls, wb, sheet_name, df, i=1, j=1):
        ws = wb[sheet_name]
        m, n = df.shape
        values = df.values
        for row in range(m):
            for col in range(n):
                value = values[row, col]
                ws.cell(row + i, col + j, value)
        return wb

    @classmethod
    def _get_save_info(cls, src_file_path, save_path=None):
        base_name = os.path.basename(src_file_path).split('.')[0]
        if len(base_name) > 30:
            base_name = 'result'
        if save_path is None:
            save_path = '.'
        else:
            if not os.path.exists(save_path):
                os.makedirs(save_path)
        return save_path, base_name

    @classmethod
    def _get_file_content(cls, file_path):
        if 'http' in file_path:
            content = requests.get(file_path).content
        else:
            with open(file_path, 'rb') as f:
                content = f.read()
        return content

    @classmethod
    def excel_2_pdf(cls, excel_path, save_path=None):
        """
        :param excel_path: 需要执行转换的excel路径或者url
        :param save_path: pdf存储路径的，默认是当前文件文件夹，传入 data, 将在当前目录新增data目录存储
        """
        save_path, base_name = cls._get_save_info(excel_path, save_path)
        content = requests.post(cls.url, files={'file': (f'{base_name}.xlsx', cls._get_file_content(excel_path))}).content
        output_path = os.path.join(save_path, f"{base_name}.pdf")
        with open(output_path, 'wb') as f:
            f.write(content)
        return output_path

    @classmethod
    def excel_2_img(cls, excel_path, save_path=None, scale=1.3, color_mode='rgb'):
        """
        :param excel_path: 需要执行转换的excel路径或者url
        :param save_path: 图片存储路径的，默认是当前文件文件夹，传入 data, 将在当前目录新增data目录存储。每个sheet生成一张图片
        :param scale: 图片放大倍数。默认1.3，该值越大图片越清晰，图片存储越大。
        :param color_mode: rgb, 图片默认使用rgb色彩空间存储。
        """
        save_path, base_name = cls._get_save_info(excel_path, save_path)
        content = requests.post(cls.url, files={'file': (f'{base_name}.xlsx', cls._get_file_content(excel_path))}).content
        pdf_document = fitz.open(stream=content)
        images_names = []
        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]
            mat = fitz.Matrix(scale, scale)
            pix = page.get_pixmap(matrix=mat, alpha=False, colorspace=color_mode)
            output_path = os.path.join(save_path, f"{base_name}_{page_number + 1}.png")
            pix.save(output_path)
            images_names.append(output_path)
        pdf_document.close()
        return images_names


if __name__ == "__main__":
    ExcelConvert.excel_2_pdf('hello.xlsx')
    ExcelConvert.excel_2_img('hello.xlsx')
