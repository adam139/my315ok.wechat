from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from my315ok.wechat.interfaces import IwechatSettings
from my315ok.wechat import MessageFactory as _


class ControlPanelForm(RegistryEditForm):
    
    schema = IwechatSettings
    label =_(u"Wechat control panel") 
    description = _(u"Wechat control panel")
    
    def updateFields(self):
        super(ControlPanelForm, self).updateFields()

    
class WechatControlPanel(ControlPanelFormWrapper):
    form = ControlPanelForm


