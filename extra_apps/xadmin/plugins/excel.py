# _*_ encoding: utf-8 _*_

"""
@athor: frank
@time: 2017/4/16 13:08
"""
from django.template import loader
from xadmin.views import BaseAdminPlugin, ListAdminView
import xadmin


# excel 导入
class ListImportExcelPlugin(BaseAdminPlugin):
    import_excel = False

    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)

    def block_top_toolbar(self, context, nodes):
        nodes.append(loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html', context_instance=context))


xadmin.site.register_plugin(ListImportExcelPlugin, ListAdminView)