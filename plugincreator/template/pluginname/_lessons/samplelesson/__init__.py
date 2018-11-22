# -*- coding: utf-8 -*-

from lessons.lesson import Step, Lesson
from lessons import utils
from qgis.utils import iface

lesson = Lesson("Sample lesson")
lesson.addStep("New Project", "New Project", iface.newProject)
