# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""手写文字识别数据类"""
import proto
from typing import List, Optional
from pydantic import BaseModel, Field

class HandwriteOCRRequest(BaseModel):
    """ 手写文字识别组件请求参数
    属性:
        image (str):
            可选。图像内容的base64编码。
        url (str):
            可选。图像的URL地址，经过base64编码。
            图像大小必须小于4MB，图像的最短边长大于15像素，最长边长大于4096像素。
        pdf_file (str):
            可选。PDF文件内容的base64编码。
        pdf_file_num (str):
            可选。PDF文件的页数。
        ofd_file (str):
            可选。OFD（Open Format Document）文件内容的base64编码。
        ofd_file_num (str):
            可选。OFD文件的页数。
        recognize_granularity(str):
            可选，识别粒度：
            可能的取值包括：
            - "big": 不定位单字符位置
            - "small": 定位单字符位置。
        probability (str):
            可选。是否输出置信度。默认为"false"。
            可能的取值包括：
            - "true": 返回识别结果中每行的置信度。
            - "false": 不返回置信度。
        detect_direction (str):
            可选。是否检测文本方向。默认为"false"。
            可能的取值包括：
            - "true": 检测文本方向。
            - "false": 不检测文本方向。
        detect_alteration（str）：
             可选，是否检测涂改痕迹，适用于手写作文场景，默认不检测
             可选值包括：
             - "true"：检测，涂改痕迹部分用“☰”返回；
             - "false"：不检测
    """
    image: str = Field(None, description="图像内容的base64编码")
    url: str = Field(None, description="图像的URL地址，经过base64编码")
    pdf_file: str = Field(None, description="PDF文件内容的base64编码")
    pdf_file_num: str = Field(None, description="PDF文件的页数")
    ofd_file: str = Field(None, description="OFD（Open Format Document）文件内容的base64编码")
    ofd_file_num: str = Field(None, description="OFD文件的页数")
    recognize_granularity: str = Field("small", description="识别粒度")
    probability: str = Field("false", description="是否输出置信度")
    detect_direction: str = Field("false", description="是否检测文本方向")
    detect_alteration: str = Field("false", description="是否检测涂改痕迹")

class HandwriteLocation(BaseModel):
    """ 手写体位置信息.

        属性:
            left (int): 表示定位位置的长方形左上顶点的水平坐标
            top (int): 表示定位位置的长方形左上顶点的垂直坐标
            width (int): 表示定位位置的长方形的宽度
            height (int): 表示定位位置的长方形的高度
         """
    left: Optional[int] = Field(None, description="表示定位位置的长方形左上顶点的水平坐标")
    top: Optional[int] = Field(None, description="表示定位位置的长方形左上顶点的垂直坐   标")
    width: Optional[int] = Field(None, description="表示定位位置的长方形的宽度")
    height: Optional[int] = Field(None, description="表示定位位置的长方形的高度")


class HandwriteWordResult(BaseModel):
    """ 手写文字识别结果

        属性:
            words (str): 识别出的文本
            location (Location): 文本位置信息
     """
    words: str = Field(None, description="识别出的文本")
    location: Optional[HandwriteLocation] = Field(None, description="文本位置信息")


class HandwriteProbability(BaseModel):
    """手写体置信度

       属性:
            average (float): 每行的平均置信度
            variance (float): 每行置信度的方差
            min (float)：每行的最小置信度
    """
    average: Optional[float] = Field(None, description="每行的平均置信度")
    variance: Optional[float] = Field(None, description="每行置信度的方差")
    min: Optional[float] = Field(None, description="每行的最小置信度")


class HandwriteOCRResponse(BaseModel):
    """手写文字识别结果

        属性:
            request_id(str): 请求ID
            log_id (int): 用于问题跟踪的唯一日志ID
            words_result_num (int): 必填。识别结果的数量
            words_result (List[WordResult]): 识别结果的数组
            probability（Probability）：当probability=true 时返回该字段，表示识别结果中每一行的置信度值
            direction (int): 当
            detect_direction=true返回改字段，1（未定义）、
            0（正向）、1（逆时针90度）、2（逆时针180度）、3（逆时针270度）
            pdf_file_size (str): 输入PDF文件的总页数。当pdf_file参数有效时返回
    """
    request_id: str = Field(None, description="请求ID")
    log_id: int = Field(None, description="用于问题跟踪的唯一日志ID")
    words_result_num: int = Field(None, description="必填。识别结果的数量")
    words_result: List[HandwriteWordResult] = Field(None, description="识别结果的数组")
    probability: Optional[HandwriteProbability] = Field(None, description="当probability=true 时返回该字段，表示识别结果中每一行的置信度值")
    direction: int = Field(None, description="当detect_direction=true返回改字段，1(未定义）、0（正向）、1（逆时针90度）、2（逆时针180度）、3（逆时针270度）")
    pdf_file_size: str = Field(None, description="输入PDF文件的总页数。当pdf_file参数有效时返回")


class HandwriteOCRInMsg(BaseModel):
    """ 手写体文字识别输入消息

        属性:
            raw_image(bytes): 图像原始内容
            url(str): 图像下载链接
    """
    raw_image: bytes = b''  # 原始图片byte数组
    url: str = ""  # 图片可下载链接


class Position(BaseModel):
    """位置信息

       属性：
            left (int): 表示定位位置的长方形左上顶点的水平坐标
            top (int): 表示定位位置的长方形左上顶点的垂直坐标
            width (int): 表示定位位置的长方形的宽度
            height (int): 表示定位位置的长方形的高度
    """

    left: int
    top: int
    width: int
    height: int


class Content(BaseModel):
    """ 识别文字

        属性：
            content(str):文字内容
            position(Position): 文字内容的位置信息
    """
    text: str
    position: Optional[Position] = None


class HandwriteOCROutMsg(BaseModel):
    """ 识别文字结果列表

        属性：
            contents(list[Content]): 手写体文字识别结果列表
            direction(int): 图像旋转角度，0（正向），- 1（逆时针90度），- 2（逆时针180度），- 3（逆时针270度）
    """
    contents: List[Content] = list()
    direction: int = 0
