import base64
import hashlib
import logging

import pytest
from nonebot.adapters.onebot.v11.message import MessageSegment
from nonebug.app import App


@pytest.fixture
def ms_list():
    msg_segments: list[MessageSegment] = []
    msg_segments.append(MessageSegment.text("【Zc】每早合约日替攻略！"))
    msg_segments.append(
        MessageSegment.image(
            file="http://i0.hdslb.com/bfs/live/new_room_cover/cf7d4d3b2f336c6dba299644c3af952c5db82612.jpg",
            cache=0,
        )
    )
    msg_segments.append(MessageSegment.text("来源: Bilibili直播 魔法Zc目录"))
    msg_segments.append(MessageSegment.text("详情: https://live.bilibili.com/3044248"))

    return msg_segments


@pytest.fixture
def pic_hash():
    return "58723fdc24b473b6dbd8ec8cbc3b7e46160c83df"


@pytest.fixture
def expect_md():
    return "【Zc】每早合约日替攻略！<br>![Image](http://i0.hdslb.com/bfs/live/new_room_cover/cf7d4d3b2f336c6dba299644c3af952c5db82612.jpg)\n来源: Bilibili直播 魔法Zc目录\n\n详情: https://live.bilibili.com/3044248\n"


def test_gene_md(app: App, expect_md, ms_list):
    from nonebot_bison.post.custom_post import CustomPost

    cp = CustomPost(message_segments=ms_list)
    cp_md = cp._generate_md()
    assert cp_md == expect_md


@pytest.mark.asyncio
async def test_gene_pic(app: App, ms_list, pic_hash):
    from nonebot_bison.post.custom_post import CustomPost

    cp = CustomPost(message_segments=ms_list)
    cp_pic_bytes: list[MessageSegment] = await cp.generate_pic_messages()

    pure_b64 = base64.b64decode(
        cp_pic_bytes[0].data.get("file").replace("base64://", "")
    )
    sha1obj = hashlib.sha1()
    sha1obj.update(pure_b64)
    sha1hash = sha1obj.hexdigest()
    assert sha1hash == pic_hash
