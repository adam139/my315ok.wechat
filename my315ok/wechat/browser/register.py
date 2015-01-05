#-*- coding: UTF-8 -*-
from five import grok
from dexterity.membrane.content.member import IMember
from dexterity.membrane.content.memberfolder import IMemberfolder
from plone.formwidget.captcha import CaptchaFieldWidget
from plone.formwidget.captcha.validator import CaptchaValidator
from plone.dexterity.utils import createContentInContainer
#from plone.directives import form,button
from plone.directives import form
from z3c.form import field, button, interfaces
from z3c.form.interfaces import IEditForm
from plone.app.textfield import RichText
from zope.component.hooks import getSite
from zope.globalrequest import getRequest
from zope import schema
from z3c.form.error import ErrorViewSnippet

from Products.CMFPlone.utils import _createObjectByType
from Products.CMFCore.utils import getToolByName

from Products.statusmessages.interfaces import IStatusMessage
from dexterity.membrane import _
from Products.CMFPlone import PloneMessageFactory as _p


defaultvalue2 = u"""
<h3 class="text-center">WeChat中国会员注册协议</h3>
<p>注册成为WeChat中国会员，并遵守本协议条款，可以享受WeChat中国提供的服务。如果不接受本协议条款，请勿注册。接受本声明，您将遵守本协议。</p>
<p><ol>
    <li>用户信息：
        <ol>
        <li>用户应自行诚信向本站提供注册资料，用户同意其提供的注册资料真实、准确、完整、合法有效，用户注册资料如有变动的，应及时更新其注册资料。如果用户提供的注册资料不合法、不真实、不准确、不详尽的，用户需承担因此引起的相应责任及后果。</li>
            <li>涉及用户真实姓名/名称、通信地址、联系电话、电子邮箱等隐私信息的，本站将予以严格保密，除非得到用户的授权或法律另有规定，本站不会向外界披露用户隐私信息。</li>
        <li>用户注册成功后，将产生用户名和密码等账户信息，您可以根据本站规定改变您的密码。用户应谨慎合理的保存、使用其用户名和密码。用户若发现任何非法使用用户账号或存在安全漏洞的情况，请立即通知本站并向公安机关报案。</li>
        <li>用户同意，WeChat中国拥有通过邮件、短信电话等形式，向注册用户发送最新活动通知的权利。</li>
        <li>用户不得将在本站注册获得的账户借给他人使用，否则用户应承担由此产生的全部责任，并与实际使用人承担连带责任。</li>                                    
    </ol>
        </li>
    <li>用户义务：<br />
        <span>用户应遵守中华人民共和国有关法律、法规和本网站有关规定。</span>
        </li>
    <li>用户权利：<br />
        <span>用户可以获取WeChat最新资源；免费参与WeChat组织的各种沙龙、会议；获取WeChat会议演讲资源；每年免费参与WeChat组织的在线培训。</span>
        </li>        
</ol></p>
"""
class IRegistrationForm(IMember):

    privacy = RichText(
            title=_(u"privacy"),
            default=defaultvalue2,
        )       
    agree = schema.Bool(
            title=_(u"Agree this?"),
            default = True,
            required=False)
    
    form.widget(captcha=CaptchaFieldWidget)
    captcha = schema.TextLine(title=u"",
                            required=True)

    form.omitted('color','description','homepage','research_domain',
                 'country','address','qq_number','photo','need_sponsorship',
                 'roomshare','is_vegetarian','comment','tshirt_size','bonus')

    form.no_omit(IEditForm, 'color','description','homepage','research_domain',
                 'country','address','qq_number','photo','need_sponsorship',
                 'roomshare','is_vegetarian','comment','tshirt_size','bonus')
  

@form.validator(field=IRegistrationForm['captcha'])
def validateCaptca(value):
    site = getSite()
    request = getRequest()
    if request.getURL().endswith('kss_z3cform_inline_validation'):
        return

    captcha = CaptchaValidator(site, request, None,
            IRegistrationForm['captcha'], None)
    captcha.validate(value)

grok.templatedir('register_templates')
from wechat.policy.browser.interfaces import IThemeSpecific  
class RegistrationForm(form.SchemaForm):
    grok.name('register')
    grok.context(IMemberfolder)
#    grok.template('registrationform')
    grok.require("zope.Public")
    grok.layer(IThemeSpecific)    
#    fields = field.Fields(IRegistrationForm)
    schema = IRegistrationForm    
    ignoreContext = True
    label = _(u"Register for site member")
     

    def update(self):
        self.request.set('disable_border', True)
        return super(RegistrationForm, self).update()
    
    def updateWidgets(self):
        super(RegistrationForm, self).updateWidgets()

        self.widgets['privacy'].label = u''        
        self.widgets['privacy'].mode = 'display'
        self.widgets['privacy'].autoresize = True
        self.widgets['agree'].addClass("checkbox")
    
    def updateActions(self):

        super(RegistrationForm, self).updateActions()
        self.actions['submit'].addClass("bn-lg btn-primary")
        self.actions['cancel'].addClass("bn-lg btn-default")        
    
    @button.buttonAndHandler(_(u"submit"))
    def submit(self, action):        
        data, errors = self.extractData() 

        if not(data['agree']):
            self.status = "must agree this private policy"
            return       
        inc = str(int(getattr(self.context, 'registrant_increment', '999999')) + 1)
        data['id'] = '%s' % inc
        self.context.registrant_increment = inc
        obj = _createObjectByType("dexterity.membrane.member", 
                self.context, data['id'])

        del data['agree']        

        for k, v in data.items():
            setattr(obj, k, v)
        
        urltool = getToolByName(self.context, 'portal_url')
        portal = urltool.getPortalObject()
        self.request.response.redirect(portal.absolute_url())
        email = data.get('email', '')
        IStatusMessage(self.request).addStatusMessage(
                        _p(u'create_membrane_account_succesful_pending_audit',
                          default=u"Your account:${address} has been created,Please wait for audit",
                          mapping={u'address': email}),
                        type='info')
        return
    
    @button.buttonAndHandler(_(u"cancel"))
    def cancel(self, action):
        urltool = getToolByName(self.context, 'portal_url')
        portal = urltool.getPortalObject()
        self.request.response.redirect(portal.absolute_url())
        return