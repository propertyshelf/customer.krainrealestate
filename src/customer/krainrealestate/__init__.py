# -*- coding: utf-8 -*-
from zope.i18nmessageid import MessageFactory
_ = MessageFactory("customer.krainrealestate")


def initialize(context):
    from Products.PlonePAS import config
    config.MEMBER_IMAGE_SCALE = (250, 500)
