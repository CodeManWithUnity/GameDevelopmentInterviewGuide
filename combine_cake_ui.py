# -*- coding:utf-8 -*-

from common import ui
from common.utils import Functor
from gcommon.ui.message import show_message
from send_protocol.rpc_protocol import rpc_call_server


# 2024中秋活动合成月饼
class CombineCakeUi(ui.UIBase):
    def init(self):
        super(CombineCakeUi, self).init()
        self.create_from_template("2024zhong_qiu_he_cheng_yue_bing")
        self.init_data()
        self.init_event()
        self.init_ui()

    def init_data(self):
        self.linqu_times = 0
        self.show_tips_texts = [
            "每日24:00自动回收未使用的材料。",
            "今日食用月饼已达上限，多余食材仍可交换。",
        ]
        # self.img_icon_texture = "res2d/item/item120/{}.png"
        self.material_tips = "制作月饼的食材之一。#r天气炎热，请尽快使用哦~"
        for i in range(3):
            img = getattr(self, "img_icon_{}".format(i + 1))
            img.tips = self.material_tips

    def init_event(self):
        self.widget.onRightClick = lambda _: self.destroy()
        self.btn_close.onClick = lambda _: self.destroy()
        self.btn_yuebing_create.onClick = Functor(self.on_yuebing_create)
        self.img_icon_1.enableTouch(True)
        self.img_icon_1.onMouseMoveIn = lambda _: self.img_icon_1.show_tips()
        self.img_icon_2.enableTouch(True)
        self.img_icon_2.onMouseMoveIn = lambda _: self.img_icon_2.show_tips()
        self.img_icon_3.enableTouch(True)
        self.img_icon_3.onMouseMoveIn = lambda _: self.img_icon_3.show_tips()
        self.btn_help.onClick = self.on_click_help

    def init_ui(self):
        self.btn_yuebing_create.tips = "合成月饼可获得奖励(每日3次)"
        # self.img_icon_1.texture = self.img_icon_texture.format(39292)
        # self.img_icon_2.texture = self.img_icon_texture.format(39294)
        # self.img_icon_3.texture = self.img_icon_texture.format(39293)

    def set_data(self, card_list, combine_times, max_times, linqu_times):
        if card_list and len(card_list) > 2:
            mianfen_cnt = (
                str(card_list[0])
                if card_list[0] > 0
                else "#R{}#n".format(card_list[0])
            )
            self.txt_mianfen_num.text = "面粉：{}".format(mianfen_cnt)
            xianliao_cnt = (
                str(card_list[1])
                if card_list[1] > 0
                else "#R{}#n".format(card_list[1])
            )
            self.txt_xianliao_num.text = "馅料：{}".format(xianliao_cnt)
            tangjiang_cnt = (
                str(card_list[2])
                if card_list[2] > 0
                else "#R{}#n".format(card_list[2])
            )
            self.txt_tangjiang_num.text = "糖浆：{}".format(tangjiang_cnt)
        if combine_times < max_times:
            self.txt_today_num.text = "今日已合成：#G{}/{}#n".format(
                combine_times, max_times
            )
        else:
            self.txt_today_num.text = "今日已合成：#R{}/{}#n".format(
                combine_times, max_times
            )
        self.linqu_times = linqu_times
        self.btn_mianfen_add.onClick = Functor(self.on_item_add, 1)
        self.btn_xianliao_add.onClick = Functor(self.on_item_add, 2)
        self.btn_tangjiang_add.onClick = Functor(self.on_item_add, 3)
        if (
            card_list[0] > 0
            and card_list[1] > 0
            and card_list[2] > 0
            and combine_times < max_times
        ):
            self.btn_yuebing_create.enable()
        else:
            self.btn_yuebing_create.disable()
        if combine_times < max_times:
            self.txt_tips_2.text = self.show_tips_texts[0]
        else:
            self.txt_tips_2.text = self.show_tips_texts[1]

        if card_list[0] > 0 or combine_times >= max_times:
            self.btn_mianfen_add.hide()
        if card_list[1] > 0 or combine_times >= max_times:
            self.btn_xianliao_add.hide()
        if card_list[2] > 0 or combine_times >= max_times:
            self.btn_tangjiang_add.hide()

    def on_item_add(self, index, btn):
        if self.linqu_times == 0:
            show_message("少侠有未领取的食材，先去领取后再来吧！")
            return
        pos_x, pos_y = btn.position
        temp_obj = self.an_niu_lie_biao.clone()
        temp_obj.position = (pos_x - 72, pos_y + 2)
        self.addChild(temp_obj, 300)
        temp_obj.set_background_mask(
            on_click_callback=lambda _: temp_obj.hide(), opacity=0
        )
        temp_obj.btn_swap.onClick = Functor(
            self.on_open_exchange_dlg, index, temp_obj
        )
        temp_obj.btn_buy.onClick = Functor(
            self.on_open_buy_material, index, temp_obj
        )

    def on_open_exchange_dlg(self, index, temp_obj, btn):
        rpc_call_server("zq_2024_open_exchange_dlg", index)
        temp_obj.hide()

    def on_open_buy_material(self, index, temp_obj, btn):
        rpc_call_server("zq_2024_buy_material", index)
        temp_obj.hide()

    def on_yuebing_create(self, btn):
        rpc_call_server("zq_2024_make_mooncake")
        self.destroy()

    def on_click_help(self, uobj):
        # 显示通用帮助界面
        from gcommon.ui.common_help_dlg import show_common_help_small_dlg

        show_common_help_small_dlg("2024年中秋月团品中秋制作月饼界面")

    # finish typehint
    def gen_typehint(self):
        # WARN: 请不要在函数头和注释`# finish typehint...`之间编写内容！！！
        # WARN: 本函数自动生成，请不要修改本函数(包括函数结尾的注释)！！！
        """Reference UI configuration file: data/uiconf/pcconf/2024zhong_qiu_he_cheng_yue_bing.py"""
        from common.ui_template import TemplateItemFromConfig
        from common.uielem.gbutton import GButton
        from common.uielem.gtexture import GTextureWithKey
        from common.uielem.gtextwithbg import GTextWithBg

        self.img_bg: GTextureWithKey
        self.txt_tips_1: GTextWithBg
        self.txt_today_num: GTextWithBg
        self.img_icon_di_1: GTextureWithKey
        self.img_icon_di_2: GTextureWithKey
        self.img_icon_di_3: GTextureWithKey
        self.img_icon_1: GTextureWithKey
        self.img_icon_2: GTextureWithKey
        self.img_icon_3: GTextureWithKey
        self.img_wenzi_di_1: GTextureWithKey
        self.img_wenzi_di_2: GTextureWithKey
        self.img_wenzi_di_3: GTextureWithKey
        self.txt_mianfen_num: GTextWithBg
        self.txt_xianliao_num: GTextWithBg
        self.txt_tangjiang_num: GTextWithBg
        self.btn_mianfen_add: GButton
        self.btn_xianliao_add: GButton
        self.btn_tangjiang_add: GButton
        self.btn_close: GButton
        self.btn_yuebing_create: GButton
        self.txt_tips_2: GTextWithBg
        self.btn_help: GButton
        self.an_niu_lie_biao: TemplateItemFromConfig
        # end typehint func
