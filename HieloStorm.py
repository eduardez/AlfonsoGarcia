#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
import os
import IceStorm


def getTopicManager(app):
    key = 'IceStorm.TopicManager.Proxy'
    proxy = app.communicator().propertyToProxy(key)
    if proxy is None:
        print("property {} not set".format(key))
        return None

    print("Using IceStorm in: '%s'" % key)
    return IceStorm.TopicManagerPrx.checkedCast(proxy)


def getTopic(topic_name, topic_manager):
    topic = None
    try:
        topic = topic_manager.retrieve(topic_name)
    except IceStorm.NoSuchTopic:
        print("no such topic found, creating")
        topic = topic_manager.create(topic_name)
    return topic


def getPublisher(topic):
    return topic.getPublisher()