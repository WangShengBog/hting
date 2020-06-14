# -*-coding: UTF-8 -*-

import logging
import os
import sys
import datetime
import time
import uuid
import random
import urllib.request
import mimetypes

__author__ = 'bog'


logger = logging.getLogger(__name__)


def init(base_url, base_dir):
    """初始化"""
    global http_base, path_base
    http_base = base_url
    path_base = base_dir


def save_file(file, save_db=None, user=None):
    """
    保存文件, 返回文件路径
    :param file:
    :param save_db:
    :param user:
    :return:
    """
    try:
        extension = get_file_ext(file.filename)
        if extension not in ['jpg', 'png', 'jpeg', 'gif', 'aac', 'mpe', 'amr']:
            return 403, "文件格式不合法, 请上传正确的文件格式", None

        filename = rebuild_file_name(extension)
        date_str = time.strftime("%Y%d")
        base_path = os.path.join(path_base, "static", "mr", date_str)
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        file_path = os.path.join(base_path, filename)
        file.save(file_path)
        if save_db:
            data = {
                "http_base": http_base,
                "file_base": path_base,
                "file_name": file.filename,
                "file_path": "/static/mr/{date_str}/{filename}".format(date_str=date_str, filename=filename),
                "file_type": get_file_ext(file.filename),
                "mime_type": mimetypes.guess_type(file.filename)[0],  # 媒体类型
                "file_size": get_file_size(file_path),
                "file_size_str": get_file_size_str(file_path)
            }
            return save_db(data, user)
        image_url = "{}/static/mr/{}/{}".format(http_base, date_str, file_path)
        return 200, "", image_url
    except Exception as e:
        logger.error(e)
        return 500, "保存图片失败", None


def save_image(body):
    """
    保存文件返回文件url
    :param body: 文件内容字典,包括url, md5, ext, size等信息
    :return: url
    """
    url = body.get("url", "")
    ext = body.get("ext", "")
    filename = rebuild_file_name(ext)
    if url:
        date_str = time.strftime("%Y%m%d")
        base_path = os.path.join(path_base, "static", "im", date_str)
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        file_path = os.path.join(base_path, filename)
        try:
            urllib.request.urlretrieve(url, file_path)
            url = "{}/static/im/{}/{}".format(http_base, date_str, filename)
        except Exception as e:
            logger.error(e)
    return url


def get_file_ext(filename):
    """获取文件扩展名"""
    if "." in filename:
        return filename.rsplit(".", 1)[1].lower()
    return None


def rebuild_file_name(extension):
    """重新生成文件名"""
    filename = time.strftime("%H%M%S") + str(random.random())[-6:]
    return "{}.{}".format(filename, extension)


def get_file_size(file_path):
    """获取文件大小"""
    file_size = os.path.getsize(file_path)
    return file_size


def get_file_size_str(file_path):
    """获取文件大小字符串"""
    file_size = get_file_size(file_path)

    def str_of_size(integer, remainder, level):
        if integer >= 1024:
            remainder = integer % 1024
            integer //= 1024
            level += 1
            return str_of_size(integer, remainder, level)
        else:
            return integer, remainder, level

    units = ["B", "KB", "MB", "GB", "TB", "TB", "PB"]
    size, remain, lv = str_of_size(file_size, 0, 0)
    if lv + 1 > len(units):
        lv -= 1

    return "{}.{:>03d} {}".format(size, remain, units[lv])


if __name__ == '__main__':
    logging.warning("{}".format(rebuild_file_name("jpg")))
