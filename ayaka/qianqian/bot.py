import nonebot
from nonebot_adapter_gocq import Bot as GoHTTPBot
import ayaka.qianqian.koi.tools.tag_manage as t
import ayaka.qianqian.koi.tools.pic_init as p_i

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter("gohttp", GoHTTPBot)
nonebot.load_builtin_plugins()
nonebot.load_plugin('nonebot_plugin_picsearcher.main')
nonebot.load_plugins('koi')
p_i.rename();t.tag_init()

if __name__ == "__main__":
    nonebot.run()