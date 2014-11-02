from plone.z3cform import layout

from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from my315ok.wechat.interfaces import IwechatSettings
from my315ok.wechat import MessageFactory as _
from z3c.form import form

class ControlPanelForm(RegistryEditForm):
    schema = IwechatSettings
    form.extends(RegistryEditForm)
    
#    label = _(u"Wechat control panel")
    
WechatControlPanelView = layout.wrap_form(ControlPanelForm, ControlPanelFormWrapper)
WechatControlPanelView.label = _(u"Wechat control panel")
