# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
from lessons.lesson import Step
from lessons import utils
from qgis.utils import iface

lesson = Lesson("Sample lesson")
lesson.addStep("New Project", "New Project", iface.newProject)
